from flask import Blueprint, Response, jsonify, request
import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Blueprint definition
itinerary_blueprint = Blueprint('itinerary_blueprint', __name__)

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Function to generate the itinerary using OpenAI
async def generate_openai_itinerary(start_date, end_date, trip_type, itinerary, tags):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": f"""
                    Generate a detailed itinerary based on:
                    - Start Date: {start_date}
                    - End Date: {end_date}
                    - Trip Type: {trip_type}
                    - Locations: {json.dumps(itinerary, indent=2)}
                    - Interests/Tags: {', '.join(tags)}

                    Please provide day-by-day itineraries from start to end date with maximum of 4 activities per day, respective locations, times, and summary for each, following the JSON format.
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
                                                        }
                                                    },
                                                    "required": ["name", "coordinates"]
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
        with open("itinerary_response.json", "w") as f:
            f.write(openai_response)
        return json.loads(openai_response)
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

    # Log incoming request data
    print("Received Data:", data)

    # Validate required fields
    if not start_date or not end_date or not trip_type or not itinerary:
        return jsonify({"error": "Missing required data"}), 400

    try:
        # Create a new event loop and run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_data = loop.run_until_complete(
            generate_openai_itinerary(start_date, end_date, trip_type, itinerary, tags)
        )
        return jsonify(response_data), 200
    except Exception as e:
        print(f"Error processing itinerary: {e}")
        return jsonify({"error": str(e)}), 500