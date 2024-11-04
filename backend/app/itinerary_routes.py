from flask import Blueprint, jsonify, request
import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.country_code_alt import country_code_to_name
import requests

# Blueprint definition
itinerary_blueprint = Blueprint('itinerary_blueprint', __name__)

# Load environment variables from .env
load_dotenv()

COUNTRY_CODE_TO_NAME  = country_code_to_name()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.environ.get("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"))
GOOGLE_API_KEY = os.environ.get("AIzaSyAlRNUntEwMM5zLz3LaPQiJF68cw9uL4rE")

# GOOGLE COORDINATES AND PLACE ID FUNCTION
def fetch_coordinates_and_place_id(place_name, city, country_code):
    try:
        # Add city context to the search query
        search_query = f"{place_name}, {city}"
        
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={search_query}&inputtype=textquery&fields=geometry,place_id,formatted_address&key={GOOGLE_API_KEY}'
        response = requests.get(url)
        data = response.json()

        print(f"Google API Response: {data}")  # Debugging print

        if data['candidates']:
            location = data['candidates'][0]['geometry']['location']
            place_id = data['candidates'][0]['place_id']
            formatted_address = data['candidates'][0].get('formatted_address', '')

            print(f"Formatted Address: {formatted_address}")
            print(f"Country Code: {country_code}")

            # Get all possible names/variations for the country from the dictionary
            country_names = COUNTRY_CODE_TO_NAME.get(country_code, [])

            # Check if the formatted address contains any of the valid country names/abbreviations
            if any(name in formatted_address for name in country_names):
                return {
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'place_id': place_id,
                    'formatted_address': formatted_address
                }
            else:
                print(f"Location {place_name} is outside the expected country ({country_code})")
                return None
        else:
            print(f"No candidates found for {place_name}")
            return None
    except Exception as e:
        print(f"Error fetching coordinates for {place_name}: {e}")
        return None

# FETCH PHOTO USING PLACE ID
def fetch_place_photo_url(place_id):
    try:
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photos&key={GOOGLE_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if 'result' in data and 'photos' in data['result'] and len(data['result']['photos']) > 0:
            photo_reference = data['result']['photos'][0]['photo_reference']
            photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}'
            return photo_url
        return None
    except Exception as e:
        print(f"Error fetching photo for place_id {place_id}: {e}")
        return None

# Function to generate the itinerary using OpenAI
async def generate_openai_itinerary(start_date, end_date, country_code, trip_type, itinerary, tags):
    try:
        # Send the request to OpenAI
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel itinerary planner."},
                {
                    "role": "user",
                    "content": f"""
                    Generate a detailed itinerary based on:
                    - Start Date: {start_date}
                    - End Date: {end_date}
                    - Trip Type: {trip_type}
                    - Locations: {json.dumps(itinerary, indent=2)}
                    - Interests/Tags: {', '.join(tags)}

                    Please generate a day-by-day itinerary from the specified start to end dates, with exactly 4 unique, specific activities per day based on the provided tags. Each activity must reference a well-known, Google-searchable location, such as popular landmarks, renowned restaurants, or significant points of interest that can be found easily via Google Places API.

                    Ensure each activity name is precise and detailed, including the full name of the place (e.g., “Louvre Museum, Paris” or “Tsukiji Outer Market, Tokyo”), rather than a generic description (e.g., avoid “local museum” or “breakfast at a cafe”). Each activity should ideally include specific, recognizable spots associated with the destination, such as famous landmarks, culturally significant sites, or popular eateries with unique offerings.

                    For generated locations by YOU, leave coordinates, place_id, and photo_url fields empty. For any user-specified locations, retain their coordinates, place_id, and photo_url.
                    """
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {'name': 'itinerary_schema',
                "schema": {
                    "type": "object",
                    "properties": {
                        "country": {
                            "type": "string",
                            "description": "The country of the trip."
                        },
                        "itinerary_summary": {
                            "type": "string",
                            "description": "A high-level summary of the trip as a whole."
                        },
                        "day_by_day_itineraries": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "day": {
                                        "type": "integer",
                                        "description": "The number of the day in the itinerary."
                                    },
                                    "date": {
                                        "type": "string",
                                        "format": "date",
                                        "description": "The date for this day's itinerary."
                                    },
                                    "summary": {
                                        "type": "string",
                                        "description": "Summary of the day and expected experiences."
                                    },
                                    "activities": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "time": {
                                                    "type": "string",
                                                    "format": "time",
                                                    "description": "The time of the activity."
                                                },
                                                "activity_name": {
                                                    "type": "string",
                                                    "description": "The name or title of the activity."
                                                },
                                                "location": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {
                                                            "type": "string",
                                                            "description": "The name of the location for the activity."
                                                        },
                                                        "city": {
                                                            "type": "string",
                                                            "description": "The city in which the location is situated."
                                                        },
                                                        "coordinates": {
                                                            "type": "object",
                                                            "properties": {
                                                                "latitude": {
                                                                    "type": "number",
                                                                    "description": "The latitude of the location."
                                                                },
                                                                "longitude": {
                                                                    "type": "number",
                                                                    "description": "The longitude of the location."
                                                                }
                                                            },
                                                            "required": ["latitude", "longitude"]
                                                        },
                                                        "place_id": {
                                                            "type": "string",
                                                            "description": "The Google Place ID for the location, leave empty if generated."
                                                        },
                                                        "photo_url": {
                                                            "type": "string",
                                                            "description": "The image URL of the location, leave empty if generated."
                                                        }
                                                    },
                                                    "required": ["name", "city", "coordinates", "place_id", "photo_url"]
                                                },
                                                "description": {
                                                    "type": "string",
                                                    "description": "A brief description of the activity."
                                                }
                                            },
                                            "required": ["time", "activity_name", "location"]
                                        }
                                    }
                                },
                                "required": ["day", "date", "summary", "activities"]
                            }
                        }
                    },
                    "required": ["country", "itinerary_summary", "day_by_day_itineraries"]
                }
            }
        }
        )
        
        # Process the response from OpenAI and return it
        openai_response = response.choices[0].message.content
        itinerary_data = json.loads(openai_response)
        with open("open_ai_itinerary.json", "w") as f:
            json.dump(itinerary_data, f, indent=2)

        # Iterate through each day in the itinerary and each activity for fetching/updating location data
        # Iterate through each day in the itinerary and each activity for fetching/updating location data
        for day in itinerary_data["day_by_day_itineraries"]:
            for activity in day["activities"]:
                location = activity.get("location", {})
                if not location or not isinstance(location, dict):
                    print(f"Warning: 'location' is missing or invalid for activity: {activity.get('activity_name', 'Unnamed Activity')}")
                    continue 
                place_name = location.get("name", "")
                city = location.get("city")  # default to Bangkok if city is missing
                
                # Check if any essential details are missing
                details_needed = not all([location.get("place_id"), location.get("coordinates"),location.get("photo_url")])
                
                if details_needed:
                    print(f"Fetching data for {place_name} due to missing details.")
                    
                    # Fetch complete location data if any essential detail is missing
                    location_data = fetch_coordinates_and_place_id(place_name, city, country_code)
                    
                    if location_data:
                        # Assign coordinates individually to avoid missing structure
                        location["coordinates"] = {
                            'latitude': location_data['latitude'],
                            'longitude': location_data['longitude']
                        }
                        # Assign place_id if missing
                        location["place_id"] = location_data.get("place_id", "")
                        
                        # Fetch and assign photo URL only if missing
                        if not location.get("photo_url"):
                            location["photo_url"] = fetch_place_photo_url(location["place_id"]) or "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27-PM.jpg"
                            print(f"Photo URL fetched or fallback used for {place_name}")
                    else:
                        print(f"Could not retrieve data for {place_name}. Skipping.")

                # Additional safeguard: Retain existing photo URL and place_id if already provided in the original itinerary
                matching_place = next((place for place in itinerary if place["name"] == place_name), None)
                if matching_place:
                    location["photo_url"] = location.get("photo_url") or matching_place.get("image")
                    location["place_id"] = location.get("place_id") or matching_place.get("place_id")
                    print(f"Retained original place_id and photo URL for {place_name} if present.") 

                # Debugging: Print the updated activity to verify it
                print(f"Updated activity for {place_name}: {json.dumps(activity, indent=2)}")

        # Log the final enriched itinerary
        with open("itinerary_response.json", "w") as f:
            json.dump(itinerary_data, f, indent=2)
                
        return itinerary_data
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return {"error": "Error generating itinerary."}

# Route to handle itinerary generation
@itinerary_blueprint.route("/generate-itinerary", methods=["POST"])
def generate_itinerary():
    data = request.get_json()

    # Extract data from the request
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    trip_type = data.get('tripType')
    itinerary = data.get('itinerary')
    tags = data.get('tags')
    country_code = data.get('countryCode')

    # Log incoming request data
    print("Received Data:", json.dumps(data, indent=2))

    # Validate required fields
    if not start_date or not end_date or not trip_type or not itinerary:
        return jsonify({"error": "Missing required data"}), 400

    try:
        # Create a new event loop and run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_data = loop.run_until_complete(
            generate_openai_itinerary(start_date, end_date, country_code, trip_type, itinerary, tags)
        )
        return jsonify(response_data), 200
    except Exception as e:
        print(f"Error processing itinerary: {e}")
        return jsonify({"error": str(e)}), 500
    

    