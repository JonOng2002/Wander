from flask import Blueprint, jsonify, request
from TikTokApi import TikTokApi
import asyncio
from openai import AsyncOpenAI
from .urlFix import resolve_redirect
import os
import json
from dotenv import load_dotenv
from .unsplashAPI import update_openai_response_with_images
import requests

tiktok_blueprint = Blueprint('tiktok_blueprint', __name__)
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Google Places API configurations
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
PLACE_DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PLACE_PHOTO_API_URL = "https://maps.googleapis.com/maps/api/place/photo"

# Function to interact with OpenAI API to generate structured response
async def generate_openai_response(video_info, comments):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Use appropriate model
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

                    Based on the metadata and comments section provided, please summarize this information and provide the details of this travel location with 1 to 3 similar places to it. For each place, provide a summary sentence about it and a query that can be used by GoogleAPI first then UnsplashAPI if failed. Try your best and please strictly follow the JSON schema provided.
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
                                    "place_png": { "type": "string", "format": "uri", "description": "Image URL from Google Places or other image sources" },
                                    "coordinates": {
                                        "type": "object",
                                        "properties": {
                                            "latitude": { "type": "number" },
                                            "longitude": { "type": "number" }
                                        },
                                        "required": ["latitude", "longitude"]
                                    },
                                    "activities": { "type": "array", "items": { "type": "string" } },
                                    "location_summary": { "type": "string" },
                                    "vicinity": { "type": "string" }
                                },
                                "required": ["place_name", "country", "city", "place_png", "coordinates", "activities", "location_summary", "vicinity"]
                            },
                            "related_places": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "place_name": { "type": "string" },
                                        "country": { "type": "string" },
                                        "city": { "type": "string" },
                                        "place_png": { "type": "string", "format": "uri", "description": "Image URL from Google Places or other image sources" },
                                        "coordinates": {
                                            "type": "object",
                                            "properties": {
                                                "latitude": { "type": "number" },
                                                "longitude": { "type": "number" }
                                            },
                                            "required": ["latitude", "longitude"]
                                        },
                                        "activities": { "type": "array", "items": { "type": "string" } },
                                        "location_summary": { "type": "string" },
                                        "vicinity": { "type": "string" }
                                    },
                                    "required": ["place_name", "country", "city", "place_png", "coordinates", "activities", "location_summary", "vicinity"]
                                }
                            }
                        },
                        "required": ["location_info", "related_places"]
                    }
                }
            }
        )
        openai_response = response.choices[0].message.content
        openai_response_json = json.loads(openai_response)

        # Enrich the OpenAI response with Google Places data
        # For main location
        main_place_name = openai_response_json['location_info']['place_name']
        vicinity, coordinates = get_place_details_google(main_place_name)
        openai_response_json['location_info']['vicinity'] = vicinity
        openai_response_json['location_info']['coordinates'] = coordinates

        # Fetch image using Google Places Photos API
        place_id = get_place_id_google(main_place_name)
        image_url = get_place_photo_google(place_id)
        if not image_url:
            # Fallback to Unsplash or a default image
            image_url = get_unsplash_image(main_place_name)
        openai_response_json['location_info']['place_png'] = image_url

        # For related places
        for place in openai_response_json['related_places']:
            place_name = place['place_name']
            vicinity, coordinates = get_place_details_google(place_name)
            place['vicinity'] = vicinity
            place['coordinates'] = coordinates

            # Fetch image using Google Places Photos API
            place_id = get_place_id_google(place_name)
            image_url = get_place_photo_google(place_id)
            if not image_url:
                # Fallback to Unsplash or a default image
                image_url = get_unsplash_image(place_name)
            place['place_png'] = image_url

        openai_response_with_images = update_openai_response_with_images(openai_response_json)

        return openai_response_with_images
    except Exception as E:
        print(f"Error with OpenAI API: {E}")
        return {"error": "Error generating response from OpenAI."}

def get_place_id_google(place_name):
    """
    Fetches the place_id for a given place_name using Google Places API.
    """
    params = {
        'input': place_name,
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': GOOGLE_PLACES_API_KEY
    }
    response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params=params)
    data = response.json()
    if data.get('candidates'):
        return data['candidates'][0]['place_id']
    return None

def get_place_details_google(place_name):
    """
    Fetches the vicinity and coordinates for a given place_name using Google Places API.
    """
    place_id = get_place_id_google(place_name)
    if not place_id:
        return 'Unknown vicinity', {'latitude': 0, 'longitude': 0}

    params = {
        'place_id': place_id,
        'fields': 'vicinity,geometry',
        'key': GOOGLE_PLACES_API_KEY
    }
    response = requests.get(PLACE_DETAILS_API_URL, params=params)
    data = response.json()
    if 'result' in data:
        vicinity = data['result'].get('vicinity', 'Unknown vicinity')
        location = data['result']['geometry']['location']
        coordinates = {
            'latitude': location['lat'],
            'longitude': location['lng']
        }
        return vicinity, coordinates
    return 'Unknown vicinity', {'latitude': 0, 'longitude': 0}

def get_photo_reference_google(place_id):
    """
    Retrieves the photo_reference for a given place_id using Google Places API.
    """
    params = {
        'place_id': place_id,
        'fields': 'photos',
        'key': GOOGLE_PLACES_API_KEY
    }
    response = requests.get(PLACE_DETAILS_API_URL, params=params)
    data = response.json()
    if 'result' in data and 'photos' in data['result']:
        return data['result']['photos'][0]['photo_reference']
    return None

def get_place_photo_google(place_id):
    """
    Fetches the photo URL for a given place_id using Google Places Photos API.
    """
    photo_reference = get_photo_reference_google(place_id)
    if not photo_reference:
        return None

    params = {
        'maxwidth': 800,
        'photoreference': photo_reference,
        'key': GOOGLE_PLACES_API_KEY
    }
    # Google Places Photos API returns a redirect to the image URL
    response = requests.get(PLACE_PHOTO_API_URL, params=params, allow_redirects=False)
    if response.status_code == 302:
        photo_url = response.headers['Location']
        return photo_url
    return None

def get_unsplash_image(query):
    """
    Fallback function to fetch an image from Unsplash if Google Places API doesn't provide one.
    """
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    url = "https://api.unsplash.com/photos/random"
    params = {
        'query': query,
        'client_id': access_key,
        'orientation': 'landscape'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'urls' in data:
        return data['urls']['regular']
    return 'https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg'  # Fallback image

async def get_video_info_comments_related(url):
    # Resolve TikTok URL if necessary
    if "vt.tiktok.com" in url:
        resolved_url = resolve_redirect(url)
        if not resolved_url:
            return {"error": "Unable to resolve URL"}, 400
    else:
        resolved_url = url

    # Initialize TikTokApi and fetch video info
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

        # Generate OpenAI response with enriched data
        response = await generate_openai_response(video_details, comments)

        # Optionally, save the response to a file for debugging
        with open('out.json', 'w') as f:
            json.dump(response, f, ensure_ascii=False)

        return {"openai_response": response}

# Flask route handling
@tiktok_blueprint.route("/video-info-comments", methods=["GET"])
def fetch_video_info_comments_related():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        # Create a new event loop for each request to handle async
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_data = loop.run_until_complete(get_video_info_comments_related(url))
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500