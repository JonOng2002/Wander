from flask import Blueprint, jsonify, request
import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import requests

# Blueprint definition
itinerary_blueprint = Blueprint('itinerary_blueprint', __name__)

# Load environment variables from .env
load_dotenv()

COUNTRY_CODE_TO_NAME = {
    "US": ["United States", "USA", "United States of America", "America"],
    "GB": ["United Kingdom", "UK", "Great Britain", "England", "Scotland", "Wales", "Northern Ireland"],
    "CA": ["Canada", "CA"],
    "AU": ["Australia", "AU", "Commonwealth of Australia"],
    "CN": ["China", "CN", "People's Republic of China"],
    "IN": ["India", "IN", "Republic of India", "Bharat"],
    "DE": ["Germany", "DE", "Deutschland", "Federal Republic of Germany"],
    "FR": ["France", "FR", "French Republic", "République Française"],
    "JP": ["Japan", "JP", "Nippon", "日本"],
    "SG": ["Singapore", "SG", "Republic of Singapore"],
    "KR": ["South Korea", "KR", "Republic of Korea", "Korea"],
    "ES": ["Spain", "ES", "España", "Kingdom of Spain"],
    "MX": ["Mexico", "MX", "México"],
    "BR": ["Brazil", "BR", "Brasil", "Federative Republic of Brazil"],
    "AR": ["Argentina", "AR", "Argentine Republic", "República Argentina"],
    "CO": ["Colombia", "CO"],
    "VE": ["Venezuela", "VE", "Bolivarian Republic of Venezuela"],
    "CL": ["Chile", "CL"],
    "PE": ["Peru", "PE", "Perú"],
    "CU": ["Cuba", "CU"],
    "JM": ["Jamaica", "JM"],
    "PR": ["Puerto Rico", "PR"],
    "DO": ["Dominican Republic", "DR", "República Dominicana"],
    "GT": ["Guatemala", "GT"],
    "HN": ["Honduras", "HN"],
    "NI": ["Nicaragua", "NI"],
    "PA": ["Panama", "PA", "Panamá"],
    "CR": ["Costa Rica", "CR"],
    "SV": ["El Salvador", "SV"],
    "HT": ["Haiti", "HT", "République d'Haïti", "Ayiti"],
    "BS": ["Bahamas", "BS", "The Bahamas"],
    "BB": ["Barbados", "BB"],
    "TT": ["Trinidad and Tobago", "TT"],
    "BZ": ["Belize", "BZ"],
    "GY": ["Guyana", "GY", "Co-operative Republic of Guyana"],
    "SR": ["Suriname", "SR"],
    "EC": ["Ecuador", "EC"],
    "BO": ["Bolivia", "BO", "Plurinational State of Bolivia"],
    "PY": ["Paraguay", "PY"],
    "UY": ["Uruguay", "UY", "República Oriental del Uruguay"],
    "GF": ["French Guiana", "GF", "Guyane française"],
    "FK": ["Falkland Islands", "FK", "Islas Malvinas"],
    "VG": ["British Virgin Islands", "VG"],
    "VI": ["US Virgin Islands", "VI"],
    "AI": ["Anguilla", "AI"],
    "AG": ["Antigua and Barbuda", "AG"],
    "GD": ["Grenada", "GD"],
    "LC": ["Saint Lucia", "LC"],
    "KN": ["Saint Kitts and Nevis", "KN"],
    "DM": ["Dominica", "DM"],
    "MS": ["Montserrat", "MS"],
    "TC": ["Turks and Caicos Islands", "TC"],
    "KY": ["Cayman Islands", "KY"],
    "PM": ["Saint Pierre and Miquelon", "PM"],
    "NZ": ["New Zealand", "NZ", "Aotearoa"],
    "IE": ["Ireland", "IE", "Éire", "Republic of Ireland"],
    "ZA": ["South Africa", "ZA", "Republic of South Africa"],
    "RU": ["Russia", "RU", "Russian Federation", "Россия"],
    "IT": ["Italy", "IT", "Italia", "Repubblica Italiana"],
    "NL": ["Netherlands", "NL", "Holland", "Nederland"],
    "SE": ["Sweden", "SE", "Sverige"],
    "NO": ["Norway", "NO", "Norge"],
    "FI": ["Finland", "FI", "Suomi"],
    "DK": ["Denmark", "DK", "Danmark"],
    "IS": ["Iceland", "IS", "Ísland"],
    "BE": ["Belgium", "BE", "Belgique", "België"],
    "PL": ["Poland", "PL", "Polska"],
    "PT": ["Portugal", "PT", "República Portuguesa"],
    "GR": ["Greece", "GR", "Hellenic Republic", "Ελλάδα"],
    "IL": ["Israel", "IL", "State of Israel", "ישראל"],
    "SA": ["Saudi Arabia", "SA", "Kingdom of Saudi Arabia", "KSA"],
    "AE": ["United Arab Emirates", "AE", "UAE"],
    "TH": ["Thailand", "TH", "ราชอาณาจักรไทย"],
    "MY": ["Malaysia", "MY"],
    "ID": ["Indonesia", "ID", "Republic of Indonesia", "Republik Indonesia"],
    "PH": ["Philippines", "PH", "Republic of the Philippines", "Republika ng Pilipinas"],
    "EG": ["Egypt", "EG", "جمهورية مصر العربية"],
    "TR": ["Turkey", "TR", "Türkiye", "Republic of Turkey"]
}



# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

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

                    Please provide day-by-day itineraries from start to end date with a maximum of 4 activities per day with regards to the tags for context. Each activity should include location details such as specific name, city, coordinates, place ID, times, and summaries. Retain the image URL and place ID for user-input locations; for generated locations, only leave an empty string for place ID and image URL if they’re unavailable.
                    """
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {'name': 'itinerary_schema',
                "schema": {
                    "type": "object",
                    "properties": {
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
                    "required": ["itinerary_summary", "day_by_day_itineraries"]
                }
            }
        }
        )
        
        # Process the response from OpenAI and return it
        openai_response = response.choices[0].message.content
        itinerary_data = json.loads(openai_response)
        with open("open_ai_itinerary.json", "w") as f:
            json.dump(itinerary_data, f, indent=2)

        # Fetch coordinates, place ID, and photo URL for each location in the itinerary
        for day in itinerary_data["day_by_day_itineraries"]:
            for activity in day["activities"]:
                place_name = activity["location"]["name"]
                city = activity["location"].get("city", "San Francisco")
                
                # Check if the location is part of the original itinerary and has an image and place ID
                matching_place = next((place for place in itinerary if place["name"] == place_name), None)

                if matching_place and "image" in matching_place and "place_id" in matching_place:
                    # Retain the original image URL and place ID from the input data
                    activity["location"]["photo_url"] = matching_place["image"]
                    activity["location"]["place_id"] = matching_place["place_id"]
                    print(f"Retained photo URL and place ID for {place_name}")
                else:
                    # Fetch coordinates and place ID if it's a generated location
                    location_data = fetch_coordinates_and_place_id(place_name, city, country_code)
                    if location_data:
                        activity["location"]["coordinates"] = {
                            'latitude': location_data['latitude'],
                            'longitude': location_data['longitude']
                        }
                        activity["location"]["place_id"] = location_data['place_id']
                        
                        # Fetch the photo URL using the place ID
                        photo_url = fetch_place_photo_url(location_data['place_id'])
                        if photo_url:
                            activity["location"]["photo_url"] = photo_url
                            print(f"Fetched photo URL for {place_name}")
                        else:
                            # Fallback image URL if no photo is found
                            activity["location"]["photo_url"] = "https://i.postimg.cc/8zLP2XNf/Image-16-10-24-at-2-27"
                            print(f"No photo available for {place_name}, using fallback.")
                    else:
                        print(f"Skipping {place_name} due to being outside country.")
        
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
    

    