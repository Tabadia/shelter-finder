# Google Maps Distance Matrix API
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.location import Location
import requests
import os
import googlemaps
import json

def reverse_geocode(latitude: float, longitude: float, max_retries: int = 3) -> str | None:
    geolocator = Nominatim(user_agent="reverse_geocoding")

    for attempt in range(max_retries):
        try:
            location: Location | None = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True, timeout=10)
            if location:
                return location.address
            else:
                return None
        except (GeocoderTimedOut, GeocoderUnavailable):
            if attempt < max_retries - 1:
                continue  # Retry if not the last attempt
            else:
                return None  # Return None if max retries reached
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

def get_travel_time_matrix(api_url, api_key, origin, destinations, travel_time=10800):
    """
    Fetches travel time and distance from the Travel Time Distance Matrix API.

    Parameters:
    - api_url (str): The API endpoint.
    - api_key (str): The API key for authentication.
    - origin (tuple): Latitude and longitude of the origin (lat, lng).
    - destinations (list): List of tuples containing lat, lng for each destination.
    - travel_time (int): Maximum travel time in seconds (default 10800 seconds).

    Returns:
    - dict: The API response containing travel times and distances.
    """

    # Build the request payload
    request_payload = {
        "arrival_searches": {
            "one_to_many": [
                {
                    "id": "Example Search",
                    "departure_location_id": "Origin",
                    "arrival_location_ids": [f"Destination {i+1}" for i in range(len(destinations))],
                    "transportation": {"type": "driving"},
                    "travel_time": travel_time,
                    "arrival_time_period": "weekday_morning",
                    "properties": ["travel_time", "distance"]
                }
            ]
        },
        "locations": [
            {
                "id": "Origin",
                "coords": {"lat": origin[0], "lng": origin[1]}
            }
        ] + [
            {
                "id": f"Destination {i+1}",
                "coords": {"lat": dest[0], "lng": dest[1]}
            } for i, dest in enumerate(destinations)
        ]
    }

    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    # Send the request
    response = requests.post(api_url, headers=headers, data=json.dumps(request_payload))

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

    return response.json()

# Example usage
if __name__ == "__main__":
    API_URL = "https://api.traveltime.com/v4/time-distance"  # Replace with actual API URL
    API_KEY = "your_api_key_here"  # Replace with your actual API key
    origin_coords = (54.238911, -0.397567)
    destination_coords = [
        (54.24424722, -0.407544543),
        (54.35384, -0.434984),
        (53.99283, -0.519234)
    ]

    result = get_travel_time_matrix(API_URL, API_KEY, origin_coords, destination_coords)
    print(json.dumps(result, indent=2))


"""
def get_driving_time(origin, destination):
    api_key = os.getenv('GMA_KEY')
    gmaps = googlemaps.Client(key=api_key)

    if not api_key:
        return "Error: GOOGLE_MAPS_API_KEY environment variable not set!"

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"  # Correct Distance Matrix API URL
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": "driving",
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        element = data["rows"][0]["elements"][0]
        if element["status"] == "OK":
            duration_seconds = element["duration"]["value"]
            duration_minutes = duration_seconds / 60
            return f"Estimated driving time: {duration_minutes:.2f} minutes"
        else:
            return f"Error fetching driving time: {element['status']}"
    else:
        print(f"Error response: {data}")  # Debugging response
        return f"Error fetching data: {data.get('error_message', data['status'])}"

if __name__ == "__main__":
    origin_address = "1600 Amphitheatre Parkway, Mountain View, CA"
    destination_address = "1 Infinite Loop, Cupertino, CA"

    print("Fetching driving time...")
    driving_time = get_driving_time(origin_address, destination_address)
    print(driving_time)#Google Maps Distance Matrix API
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.location import Location
import ssl
import certifi
import requests
import os

def reverse_geocode(latitude: float, longitude: float, max_retries: int = 3) -> str | None:
    geolocator = Nominatim(user_agent="reverse_geocoding")

    for attempt in range(max_retries):
        try:
            location: Location | None = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True, timeout=10)
            if location:
                return location.address
            else:
                return None
        except (GeocoderTimedOut, GeocoderUnavailable):
            if attempt < max_retries - 1:
                continue  # Retry if not the last attempt
            else:
                 return None # Return None if max retries reached

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

def get_driving_time(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "key": os.getenv('GOOGLE_MAPS_API_KEY')
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        duration_seconds = data["routes"][0]["legs"][0]["duration"]["value"]
        duration_minutes = duration_seconds / 60
        return f"Estimated driving time: {duration_minutes:.2f} minutes"
    else:
        return f"Error fetching directions: {data['status']}"

if __name__ == "__main__":
    origin_address = "1600 Amphitheatre Parkway, Mountain View, CA"
    destination_address = "1 Infinite Loop, Cupertino, CA"
    
    print("x")
    driving_time = get_driving_time(origin_address, destination_address)
    print(driving_time)
"""