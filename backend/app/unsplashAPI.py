import requests

# Your Unsplash Access Key
UNSPLASH_ACCESS_KEY = "6ejkgR7fSorrfHBU-fQK4kimB-S3R3F18EgWc-kxf0Q"

# Fetch image from Unsplash dynamically based on place name
def fetch_image_from_unsplash(place_name):
    url = f"https://api.unsplash.com/photos/random?query={place_name}&orientation=landscape"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"  # Use the variable directly
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            image_data = response.json()
            print("Fetched image URL:", image_data["urls"]["regular"])
            return image_data["urls"]["regular"]
        else:
            print(f"Error fetching image from Unsplash: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred while fetching image from Unsplash: {e}")
        return None

# Update the OpenAI response with image URLs fetched from Unsplash
def update_openai_response_with_images(openai_response):
    # For the main location
    location_name = openai_response['location_info']['place_name']
    image_url = fetch_image_from_unsplash(location_name)
    
    if image_url:
        openai_response['location_info']['place_png'] = image_url
    else:
        openai_response['location_info']['place_png'] = "default_image_url"  # Fallback image URL
    
    # For related places
    for place in openai_response['related_places']:
        place_name = place['place_name']
        image_url = fetch_image_from_unsplash(place_name)
        
        if image_url:
            place['place_png'] = image_url
        else:
            place['place_png'] = "default_image_url"  # Fallback image URL
    
    return openai_response