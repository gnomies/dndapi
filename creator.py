import os
import random
import requests
import openai
from dotenv import load_dotenv
import sqlite3

# Load .env file
load_dotenv()

# Base URL for the DnD API
API_URL = "https://www.dnd5eapi.co"

# Get OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('db/characters.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS characters
    (name TEXT, race TEXT, class TEXT, equipment TEXT, backstory TEXT)
    ''')

def get_random_race():
    response = requests.get(f"{API_URL}/api/races")
    races = response.json()['results']
    return random.choice(races)['index']

def get_random_class():
    response = requests.get(f"{API_URL}/api/classes")
    classes = response.json()['results']
    return random.choice(classes)['index']

def get_random_equipment():
    response = requests.get(f"{API_URL}/api/equipment")
    equipment = response.json()['results']
    return random.choice(equipment)['index']

def generate_character_name():
    response = openai.Completion.create(engine="text-davinci-003", prompt="Generate a unique name for a fantasy character", max_tokens=30)
    return response.choices[0].text.strip()

def generate_character():
    name = generate_character_name()
    race = get_random_race()
    _class = get_random_class()
    equipment = get_random_equipment()
    character = {
        "name": name,
        "race": race,
        "class": _class,
        "equipment": equipment,
    }
    return character

def generate_backstory(character):
    prompt = f"Generate a backstory for a {character['race']} {character['class']} named {character['name']} who carries a {character['equipment']}"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
    return response.choices[0].text.strip()

def output_to_database(character, backstory):
    c.execute("INSERT INTO characters (name, race, class, equipment, backstory) VALUES (?, ?, ?, ?, ?)",
              (character['name'], character['race'], character['class'], character['equipment'], backstory))
    conn.commit()

if __name__ == "__main__":
    character = generate_character()
    print(character)
    backstory = generate_backstory(character)
    print("Backstory:")
    print(backstory)
    output_to_database(character, backstory)