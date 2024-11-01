# unsplashAPI.py

import requests
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Logging for this module
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Your Unsplash Access Key (Ensure this is set in your .env file)
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def fetch_image_from_unsplash(place_name):
    if not UNSPLASH_ACCESS_KEY:
        logger.error("Unsplash Access Key is not set in environment variables.")
        return None

    url = f"https://api.unsplash.com/photos/random?query={place_name}&orientation=landscape"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            image_data = response.json()
            image_url = image_data.get("urls", {}).get("regular")
            if image_url:
                logger.debug(f"Fetched image URL from Unsplash for '{place_name}': {image_url}")
                return image_url
            else:
                logger.warning(f"No 'regular' URL found in Unsplash response for '{place_name}'.")
                return None
        else:
            logger.error(f"Error fetching image from Unsplash for '{place_name}': {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Exception occurred while fetching image from Unsplash for '{place_name}': {e}")
        return None

def is_valid_image_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return True
        return False
    except requests.RequestException:
        return False

def update_openai_response_with_images(openai_response):
    """
    Enriches the OpenAI response with images.
    Only fetches from Unsplash if 'place_png' is missing or invalid.
    """
    logger.debug("Updating OpenAI response with images from Unsplash where necessary.")

    # Helper function to update a single place
    def update_place_image(place):
        place_name = place.get('place_name')
        current_image = place.get('place_png')

        if not is_valid_image_url(current_image):
            logger.info(f"'place_png' missing or invalid for '{place_name}'. Fetching from Unsplash.")
            image_url = fetch_image_from_unsplash(place_name)
            if image_url:
                place['place_png'] = image_url
            else:
                logger.warning(f"Failed to fetch image from Unsplash for '{place_name}'. Using fallback image.")
                place['place_png'] = "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"  # Fallback image URL
        else:
            logger.debug(f"'place_png' already set and valid for '{place_name}'. Skipping Unsplash fetch.")

    # Update main location
    logger.debug("Checking main location for image update.")
    location_info = openai_response.get('location_info', {})
    update_place_image(location_info)

    # Update related places
    related_places = openai_response.get('related_places', [])
    for related_place in related_places:
        logger.debug(f"Checking related place '{related_place.get('place_name')}' for image update.")
        update_place_image(related_place)

    logger.debug("Completed updating OpenAI response with images.")
    return openai_response