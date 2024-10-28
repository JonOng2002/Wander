from flask import Blueprint, jsonify, request
from TikTokApi import TikTokApi
import asyncio
from openai import AsyncOpenAI
from .urlFix import resolve_redirect
import os
import json
from dotenv import load_dotenv
from .unsplashAPI import update_openai_response_with_images



tiktok_blueprint = Blueprint('tiktok_blueprint', __name__)
load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function to interact with OpenAI API to generate structured response
async def generate_openai_response(video_info, comments):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that processes TikTok video metadata and provides structured data and recommendations for travel itinerary/places of interest for the user."
                },
                {
                    "role": "user",
                    "content": f"""
                    Here is TikTok video data:
                    Video Info: {video_info}
                    Comments: {comments}

                    Base on the metadata and comments section provided, please summarize this information and provide the details of this travel location with 1 to 3 similar places to it. For each place, provide a summary sentence about it and a query that can be used by Unsplash API. Try your best and please strictly follow the JSON schema provided.
                    """
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "wander_output_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "location_info": {
                                "type": "object",
                                "properties": {
                                    "place_name": { "type": "string" },
                                    "country": { "type": "string" },
                                    "city": { "type": "string" },
                                    "place_png": { "type": "string", "format": "uri", "description": "Image URL from Unsplash or other image sources" },
                                    "coordinates": {
                                        "type": "object",
                                        "properties": {
                                            "latitude": { "type": "number" },
                                            "longitude": { "type": "number" }
                                        },
                                        "required": ["latitude", "longitude"]
                                    },
                                    "activities": { "type": "array", "items": { "type": "string" } },
                                    "location_summary": { "type": "string" }
                                },
                                "required": ["place_name", "country", "city", "place_png", "coordinates", "activities", "location_summary"]
                            },
                            "related_places": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "place_name": { "type": "string" },
                                        "country": { "type": "string" },
                                        "city": { "type": "string" },
                                        "place_png": { "type": "string", "format": "uri", "description": "Image URL from Unsplash or other image sources" },
                                        "coordinates": {
                                            "type": "object",
                                            "properties": {
                                                "latitude": { "type": "number" },
                                                "longitude": { "type": "number" }
                                            },
                                            "required": ["latitude", "longitude"]
                                        },
                                        "activities": { "type": "array", "items": { "type": "string" } },
                                        "location_summary": { "type": "string" }
                                    },
                                    "required": ["place_name", "country", "city", "place_png", "coordinates", "activities", "location_summary"]
                                }
                            }
                        },
                        "required": ["location_info", "related_places"]
                    }
                }
            }
        )
        openai_response = response.choices[0].message.content
        openai_response_with_images = update_openai_response_with_images(json.loads(openai_response))
        
        return openai_response_with_images
    except Exception as E:
        print(f"Error with OpenAI API: {E}")
        return {"error": "Error generating response from OpenAI."}

async def get_video_info_comments_related(url):
    if "vt.tiktok.com" in url:
        resolved_url = resolve_redirect(url)
        if not resolved_url:
            return {"error": "Unable to resolve URL"}, 400
    else:
        resolved_url = url

    async with TikTokApi() as api:
        await api.create_sessions(num_sessions=1, sleep_after=3)
        video = api.video(url=resolved_url)

        video_info = await video.info()
        video_details = {
            "id": video_info.get('id'),
            "title": video_info.get('desc'),
            "author": video_info.get('author', {}).get('nickname'),
            "play_count": video_info.get('stats', {}).get('playCount'),
            "likes": video_info.get('stats', {}).get('diggCount'),
            "comments_count": video_info.get('stats', {}).get('commentCount')
        }

        comments = []
        try:
            video_info = await video.info()
            if not video_info:
                raise ValueError("Video not found or has been removed.")

            async for comment in video.comments(count=5):
                comments.append({"text": comment.text})
        except Exception as e:
            print(f"Error fetching comments: {e}")

        response = await generate_openai_response(video_details, comments)
        with open('out.json', 'w') as f:
            json.dump(response, f, ensure_ascii=False)

        return {"openai_response": response}

# Adjusting for Flask's sync nature using asyncio event loop
@tiktok_blueprint.route("/video-info-comments", methods=["GET"])
def fetch_video_info_comments_related():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_data = loop.run_until_complete(get_video_info_comments_related(url))
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500