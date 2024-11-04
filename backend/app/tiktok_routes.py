# tiktok_routes.py

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
import logging

# Blueprint definition
tiktok_blueprint = Blueprint('tiktok_blueprint', __name__)
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs will be output to the console
    ]
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=os.environ.get("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"),
)

# Google Places API configurations
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_API_KEY")
PLACE_DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PLACE_PHOTO_API_URL = "https://maps.googleapis.com/maps/api/place/photo"

# Function to interact with OpenAI API to generate structured response
async def generate_openai_response(video_info, comments):
    logger.debug("Generating OpenAI response with video_info and comments.")
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure this model name is correct
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
        logger.debug("OpenAI API call successful.")
        openai_response = response.choices[0].message.content
        try:
            openai_response_json = json.loads(openai_response)
            logger.debug(f"OpenAI response JSON: {openai_response_json}")
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decoding failed: {json_err}")
            return {"error": "Invalid JSON format in OpenAI response."}

        # Enrich the OpenAI response with Google Places data
        # For main location
        main_place_name = openai_response_json['location_info']['place_name']
        logger.info(f"Fetching details for main place: {main_place_name}")
        
        # Store OpenAI's original coordinates
        openai_main_coordinates = openai_response_json['location_info'].get('coordinates', {})
        
        vicinity, google_main_coordinates = get_place_details_google(
            main_place_name, 
            openai_response_json['location_info'].get('city', ''), 
            openai_response_json['location_info'].get('country', '')
        )
        logger.debug(f"Main place vicinity from Google Places: {vicinity}")
        logger.debug(f"Main place coordinates from Google Places: {google_main_coordinates}")

        # Determine which coordinates to use
        if google_main_coordinates['latitude'] != 0 or google_main_coordinates['longitude'] != 0:
            # Use Google Places API coordinates
            openai_response_json['location_info']['coordinates'] = google_main_coordinates
            openai_response_json['location_info']['vicinity'] = vicinity
            logger.debug(f"Overridden main place coordinates with Google Places data: {google_main_coordinates}")
        else:
            # Google Places API failed to provide coordinates
            if openai_main_coordinates and (openai_main_coordinates.get('latitude') != 0 or openai_main_coordinates.get('longitude') != 0):
                # Use OpenAI's coordinates
                logger.debug(f"Using OpenAI's main place coordinates: {openai_main_coordinates}")
                # Coordinates remain as provided by OpenAI
            else:
                # Set to (0, 0)
                openai_response_json['location_info']['coordinates'] = {'latitude': 0, 'longitude': 0}
                logger.debug("Set main place coordinates to (0, 0) due to lack of data.")

        # Fetch image using Google Places Photos API for main place
        place_id = get_place_id_google(main_place_name)
        if place_id:
            logger.info(f"Fetching photo for main place: {main_place_name}")
            image_url = get_place_photo_google(place_id)
            if image_url:
                logger.debug(f"Image URL fetched from Google Places: {image_url}")
                openai_response_json['location_info']['place_png'] = image_url
            else:
                logger.warning(f"No image found for {main_place_name} from Google Places. Falling back to Unsplash.")
                image_url = fetch_image_from_unsplash(main_place_name)
                if image_url:
                    openai_response_json['location_info']['place_png'] = image_url
                else:
                    openai_response_json['location_info']['place_png'] = "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"  # Fallback image URL
        else:
            logger.warning(f"No place_id found for {main_place_name}. Falling back to Unsplash.")
            image_url = fetch_image_from_unsplash(main_place_name)
            if image_url:
                openai_response_json['location_info']['place_png'] = image_url
            else:
                openai_response_json['location_info']['place_png'] = "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"  # Fallback image URL

        # For related places
        for place in openai_response_json['related_places']:
            place_name = place['place_name']
            logger.info(f"Fetching details for related place: {place_name}")
            
            # Store OpenAI's original coordinates for the related place
            openai_related_coordinates = place.get('coordinates', {})
            
            vicinity, google_related_coordinates = get_place_details_google(
                place_name, 
                place.get('city', ''), 
                place.get('country', '')
            )
            logger.debug(f"Related place vicinity from Google Places: {vicinity}")
            logger.debug(f"Related place coordinates from Google Places: {google_related_coordinates}")

            # Determine which coordinates to use
            if google_related_coordinates['latitude'] != 0 or google_related_coordinates['longitude'] != 0:
                # Use Google Places API coordinates
                place['coordinates'] = google_related_coordinates
                place['vicinity'] = vicinity
                logger.debug(f"Overridden related place coordinates with Google Places data: {google_related_coordinates}")
            else:
                # Google Places API failed to provide coordinates
                if openai_related_coordinates and (openai_related_coordinates.get('latitude') != 0 or openai_related_coordinates.get('longitude') != 0):
                    # Use OpenAI's coordinates
                    logger.debug(f"Using OpenAI's related place coordinates: {openai_related_coordinates}")
                    # Coordinates remain as provided by OpenAI
                else:
                    # Set to (0, 0)
                    place['coordinates'] = {'latitude': 0, 'longitude': 0}
                    logger.debug(f"Set related place '{place_name}' coordinates to (0, 0) due to lack of data.")

            # Fetch image using Google Places Photos API for related place
            place_id = get_place_id_google(place_name)
            if place_id:
                logger.info(f"Fetching photo for related place: {place_name}")
                image_url = get_place_photo_google(place_id)
                if image_url:
                    logger.debug(f"Image URL fetched from Google Places: {image_url}")
                    place['place_png'] = image_url
                else:
                    logger.warning(f"No image found for {place_name} from Google Places. Falling back to Unsplash.")
                    image_url = fetch_image_from_unsplash(place_name)
                    if image_url:
                        place['place_png'] = image_url
                    else:
                        place['place_png'] = "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"  # Fallback image URL
            else:
                logger.warning(f"No place_id found for {place_name}. Falling back to Unsplash.")
                image_url = fetch_image_from_unsplash(place_name)
                if image_url:
                    place['place_png'] = image_url
                else:
                    place['place_png'] = "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"  # Fallback image URL

        # Enrich response with images only if necessary
        openai_response_with_images = update_openai_response_with_images(openai_response_json)
        logger.debug("Response enriched with images.")
        return openai_response_with_images
    except Exception as E:
        logger.error(f"Error with OpenAI API: {E}", exc_info=True)
        return {"error": "Error generating response from OpenAI."}

def get_place_id_google(place_name):
    """
    Fetches the place_id for a given place_name using Google Places API.
    """
    logger.debug(f"Fetching place_id for: {place_name}")
    params = {
        'input': place_name,
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': GOOGLE_PLACES_API_KEY
    }
    try:
        response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params=params)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Google Places API findplacefromtext response: {data}")
        if data.get('candidates'):
            place_id = data['candidates'][0]['place_id']
            logger.info(f"Found place_id for {place_name}: {place_id}")
            return place_id
        else:
            logger.warning(f"No candidates found for {place_name}.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching place_id for {place_name}: {e}", exc_info=True)
        return None

def get_place_details_google(place_name, city, country):
    """
    Fetches the vicinity and coordinates for a given place_name using Google Places API.
    If no location is found, replaces vicinity with "city, country".
    """
    logger.debug(f"Fetching place details for: {place_name}")
    place_id = get_place_id_google(place_name)
    if not place_id:
        logger.warning(f"No place_id found for {place_name}. Setting vicinity to 'city, country'.")
        vicinity = f"{city}, {country}" if city and country else 'Unknown vicinity'
        return vicinity, {'latitude': 0, 'longitude': 0}

    params = {
        'place_id': place_id,
        'fields': 'vicinity,geometry',
        'key': GOOGLE_PLACES_API_KEY
    }
    try:
        response = requests.get(PLACE_DETAILS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Google Places API place details response: {data}")
        if 'result' in data:
            vicinity = data['result'].get('vicinity', f"{city}, {country}" if city and country else 'Unknown vicinity')
            location = data['result']['geometry']['location']
            coordinates = {
                'latitude': location['lat'],
                'longitude': location['lng']
            }
            logger.info(f"Fetched details for {place_name}: Vicinity - {vicinity}, Coordinates - {coordinates}")
            return vicinity, coordinates
        else:
            logger.warning(f"No result found in place details for {place_name}. Setting vicinity to 'city, country'.")
            vicinity = f"{city}, {country}" if city and country else 'Unknown vicinity'
            return vicinity, {'latitude': 0, 'longitude': 0}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching place details for {place_name}: {e}", exc_info=True)
        vicinity = f"{city}, {country}" if city and country else 'Unknown vicinity'
        return vicinity, {'latitude': 0, 'longitude': 0}

def get_photo_reference_google(place_id):
    """
    Retrieves the photo_reference for a given place_id using Google Places API.
    """
    logger.debug(f"Fetching photo_reference for place_id: {place_id}")
    params = {
        'place_id': place_id,
        'fields': 'photos',
        'key': GOOGLE_PLACES_API_KEY
    }
    try:
        response = requests.get(PLACE_DETAILS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Google Places API photos response: {data}")
        if 'result' in data and 'photos' in data['result']:
            photo_reference = data['result']['photos'][0]['photo_reference']
            logger.info(f"Found photo_reference for place_id {place_id}: {photo_reference}")
            return photo_reference
        else:
            logger.warning(f"No photos found for place_id {place_id}.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching photo_reference for place_id {place_id}: {e}", exc_info=True)
        return None

def get_place_photo_google(place_id):
    """
    Fetches the photo URL for a given place_id using Google Places Photos API.
    """
    logger.debug(f"Fetching photo URL for place_id: {place_id}")
    photo_reference = get_photo_reference_google(place_id)
    if not photo_reference:
        logger.warning(f"No photo_reference found for place_id {place_id}.")
        return None

    params = {
        'maxwidth': 800,
        'photoreference': photo_reference,
        'key': GOOGLE_PLACES_API_KEY
    }
    try:
        # Google Places Photos API returns a redirect to the image URL
        response = requests.get(PLACE_PHOTO_API_URL, params=params, allow_redirects=False)
        logger.debug(f"Google Places Photos API response status: {response.status_code}")
        if response.status_code == 302:
            photo_url = response.headers['Location']
            logger.info(f"Fetched photo URL for place_id {place_id}: {photo_url}")
            return photo_url
        else:
            logger.warning(f"Unexpected status code {response.status_code} when fetching photo for place_id {place_id}.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching photo for place_id {place_id}: {e}", exc_info=True)
        return None

async def get_video_info_comments_related(url):
    logger.debug(f"Processing TikTok URL: {url}")
    # Resolve TikTok URL if necessary
    if "vt.tiktok.com" in url:
        logger.debug("URL is a shortened TikTok URL. Resolving redirect.")
        resolved_url = resolve_redirect(url)
        if not resolved_url:
            logger.error("Unable to resolve TikTok URL.")
            return {"error": "Unable to resolve URL"}, 400
        logger.debug(f"Resolved TikTok URL: {resolved_url}")
    else:
        resolved_url = url
        logger.debug("URL is a direct TikTok URL.")

    # Initialize TikTokApi and fetch video info
    try:
        async with TikTokApi() as api:
            logger.debug("Creating TikTokApi sessions.")
            await api.create_sessions(num_sessions=1, sleep_after=3)
            logger.debug("Fetching TikTok video object.")
            video = api.video(url=resolved_url)

            logger.debug("Fetching video info.")
            video_info = await video.info()
            logger.debug(f"Video info fetched: {video_info}")

            video_details = {
                "id": video_info.get('id'),
                "title": video_info.get('desc'),
                "author": video_info.get('author', {}).get('nickname'),
                "play_count": video_info.get('stats', {}).get('playCount'),
                "likes": video_info.get('stats', {}).get('diggCount'),
                "comments_count": video_info.get('stats', {}).get('commentCount')
            }
            logger.debug(f"Video details: {video_details}")

            comments = []
            try:
                logger.debug("Fetching video comments.")
                async for comment in video.comments(count=5):
                    comments.append({"text": comment.text})
                logger.debug(f"Fetched comments: {comments}")
            except Exception as e:
                logger.error(f"Error fetching comments: {e}", exc_info=True)

            # Generate OpenAI response with enriched data
            logger.debug("Generating OpenAI response.")
            response = await generate_openai_response(video_details, comments)

            # Optionally, save the response to a file for debugging
            with open('out.json', 'w') as f:
                json.dump(response, f, ensure_ascii=False, indent=2)
            logger.debug("Saved OpenAI response to out.json.")

            return {"openai_response": response}
    except Exception as e:
        logger.error(f"Error processing TikTok URL {url}: {e}", exc_info=True)
        return {"error": "Error processing TikTok URL."}, 500

# Flask route handling
@tiktok_blueprint.route("/video-info-comments", methods=["GET"])
def fetch_video_info_comments_related():
    url = request.args.get('url')
    if not url:
        logger.warning("URL parameter is missing in the request.")
        return jsonify({"error": "URL parameter is missing"}), 400

    logger.info(f"Received request to fetch video info and comments for URL: {url}")

    try:
        # Create a new event loop for each request to handle async
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        logger.debug("Created a new event loop for async processing.")
        response_data = loop.run_until_complete(get_video_info_comments_related(url))
        logger.info("Successfully processed the request.")
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Unhandled exception in route handler: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500