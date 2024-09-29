from flask import Blueprint, jsonify
from TikTokApi import TikTokApi
import asyncio
import json
import asyncio
from playwright.async_api import async_playwright

async def get_ms_token():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set headless=True to run without UI
        context = await browser.new_context()

        # Open a new page and navigate to TikTok's homepage
        page = await context.new_page()
        await page.goto("https://www.tiktok.com")

        # Optionally, you can automate login if needed:
        # For manual login, wait for the user to log in.
        # Comment out if already logged in or don't need login.
        print("Please log in to TikTok...")
        await page.wait_for_timeout(30000)  # Wait 30 seconds for manual login

        # After login or page load, retrieve the cookies
        cookies = await context.cookies()

        # Extract the msToken from the cookies
        ms_token = None
        for cookie in cookies:
            if cookie["name"] == "msToken":
                ms_token = cookie["value"]
                break

        if ms_token:
            print(f"Extracted msToken: {ms_token}")
        else:
            print("msToken not found in cookies")

        # Close the browser
        await browser.close()

        return ms_token

# Run the asynchronous function
asyncio.run(fetch_tiktok_data())
main = Blueprint("main", __name__)


@main.route("/pfp", methods=["GET"])
async def pfp():
    # Run get_comments asynchronously
    pfp = await get_pfp()
    return jsonify(pfp), 200
