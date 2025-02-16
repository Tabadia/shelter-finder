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
import re


load_dotenv()
#API_KEY = os.getenv("RADAR_API_KEY")
API_KEY = "prj_live_sk_506c0a2d887f426db7651fea81875fb015d20bd6"

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
        #print(data)
        return data[0]["lat"], data[0]["lon"]

    
def convert_duration_to_minutes(duration_text):
    # Define conversion factors
    day_to_minutes = 1440  # 1 day = 1440 minutes
    hour_to_minutes = 60   # 1 hour = 60 minutes

    # Extract numerical values using regex
    days = re.search(r"(\d+) day", duration_text)
    hours = re.search(r"(\d+) hr", duration_text)
    minutes = re.search(r"(\d+) min", duration_text)

    # Convert extracted values to integers (default to 0 if not found)
    total_minutes = 0
    if days:
        total_minutes += int(days.group(1)) * day_to_minutes
    if hours:
        total_minutes += int(hours.group(1)) * hour_to_minutes
    if minutes:
        total_minutes += int(minutes.group(1))

    return total_minutes

def get_radar_time(user_lat, user_lon, shelter_address):
    shelter_lat, shelter_lon = geocode(shelter_address)

    if shelter_lat is None or shelter_lon is None:
        return "Error: Could not geocode shelter address."

    API_URL = "https://api.radar.io/v1/route/distance"  # Correct endpoint for distance calculations
    params = {
        "origin": f"{user_lat},{user_lon}",
        "destination": f"{shelter_lat},{shelter_lon}",
        "modes": "car",  # Corrected parameter name
        "units": "metric"  # Optional but ensures consistent results
    }

    #headers = {"Authorization": f"Bearer {API_KEY}"}
    headers = {"Authorization": API_KEY}

    #print(f"Requesting: {API_URL} with params {params}")  # Debugging

    response = requests.get(API_URL, headers=headers, params=params)
    #print(response.status_code, response.text)
    #print(response.text)

    if response.status_code == 400:
        return f"Error 400: Bad Request. Check parameters. Response: {response.text}"

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()

    try:
        # Extract travel time in minutes
        travel_time = data["routes"]["car"]["duration"]["text"]
        return convert_duration_to_minutes(travel_time)
    except KeyError:
        return "Error: No route data found in response."
