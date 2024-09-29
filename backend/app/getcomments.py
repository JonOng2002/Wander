from flask import Flask, Blueprint, jsonify
from TikTokApi import TikTokApi
import asyncio
import json

# Create a Flask Blueprint
main = Blueprint("main", __name__)

# Function to get comments from TikTok using TikTokApi
async def get_comments(video_id):
    async with TikTokApi() as api:
        # Create a Playwright session
        await api.create_sessions(num_sessions=1, sleep_after=3)

        # Retrieve cookies and extract msToken
        session = api.sessions[0]
        cookies = await api.get_session_cookies(session)
        ms_token = cookies.get("msToken")

        if not ms_token:
            raise ValueError("Failed to retrieve msToken from the session cookies")

        try:
            # Fetch video and comments using the video ID
            video = api.video(id=video_id)
            comments = []
            async for comment in video.comments(count=20):
                comments.append(comment.as_dict)

            # Write the comments to a JSON file (optional)
            with open("out.json", "w") as f:
                json.dump(comments, f)

            # Return the comments for the Flask response
            return comments

        except Exception as e:
            print(f"Error fetching comments: {e}")
            return {"error": str(e)}

# Define Flask route for "/hello"
@main.route("/comments/<video_id>", methods=["GET"])
def fetch_comments(video_id):
    # Run the asynchronous function in an event loop
    comments = asyncio.run(get_comments(video_id))
    return jsonify(comments), 200

