# Google Maps Distance Matrix API
from geopy.geocoders import nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.location import Location
import requests
import os
import googlemaps
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
API_KEY = os.getenv("RADAR_API_KEY")

if not API_KEY:
   raise ValueError("API_KEY not found")

def geocode(address):
    url = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json'

    headers = {
        "User-Agent": "YourAppName/1.0 (your@email.com)"  # Replace with your app info
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200 or response.text.strip() == "":
        print(f"Error: API request failed with status {response.status_code}")
        print("Response Text:", response.text)
    else:
        data = response.json()
        return data[0]["lat"],  data[0]["lon"]



def get_radar_time(user_lat, user_lon, shelter_address):
    shelter_lat, shelter_lon = geocode(shelter_address)

    if shelter_lat is None or shelter_lon is None:
        return "Error: Could not geocode shelter address."

    # Construct Radar.io API request
    API_URL = "https://api.radar.io/v1/route/match"
    request_url = f"{API_URL}?origin={user_lat},{user_lon}&destination={shelter_lat},{shelter_lon}&mode=car"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(request_url, headers=headers)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()

    try:
        # Extract travel time (seconds) and convert to minutes
        travel_time_seconds = data["distance"]["value"] / 25  # Approximate car speed 25 m/s
        travel_time_minutes = round(travel_time_seconds / 60)

        return f"Estimated travel time: {travel_time_minutes} minutes"

    except KeyError:
        return "Error: No route data found in response."