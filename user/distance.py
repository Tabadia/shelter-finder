#Google Maps Distance Matrix API

import geopy

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


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

latitude = 34.0522  # Example latitude
longitude = -118.2437  # Example longitude

address = reverse_geocode(latitude, longitude)

if address:
    print(f"The address for coordinates ({latitude}, {longitude}) is: {address}")
else:
    print(f"Could not find address for coordinates ({latitude}, {longitude})")
