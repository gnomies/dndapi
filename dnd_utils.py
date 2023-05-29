import requests
import random

API_URL = "https://www.dnd5eapi.co"

def get_random_from_api(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None
    return random.choice(data['results'])['index']
