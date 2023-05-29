import os
import random
import requests
import openai
from dotenv import load_dotenv
import sqlite3
import datetime
import dnd_utils
import time

def exponential_backoff(func, max_retries=5):
    wait_time = 1
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:  # If this was the last attempt
                raise  # Propagate the exception
            else:
                print(f"Request failed with {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  # Double the wait time for the next attempt
                wait_time += random.uniform(0, 1)  # Add a random component

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

def create_table(table_name, fields):
    try:
        # Join fields with commas to create the fields string for the SQL command
        fields_str = ", ".join(fields)
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({fields_str})
        ''')
        conn.commit()
    except sqlite3.Error as e:  # This catches any SQLite-related exception
        print(f"Error creating table {table_name}: {e}")

if __name__ == "__main__":
    # Define the fields for each table as lists of strings
    character_fields = ["id INTEGER PRIMARY KEY", "name TEXT", "race TEXT", "_class TEXT", "equipment TEXT", "backstory TEXT", "stats TEXT"]
    race_fields = ["id INTEGER PRIMARY KEY", "race TEXT"]
    class_fields = ["id INTEGER PRIMARY KEY", "class TEXT"]
    equipment_fields = ["id INTEGER PRIMARY KEY", "equipment TEXT"]
    character_stats_fields = ["character_id INTEGER, strength INTEGER, dexterity INTEGER, constitution INTEGER, intelligence INTEGER, wisdom INTEGER, charisma INTEGER,  FOREIGN KEY(character_id) REFERENCES characters(id)"]
    update_fields = ["id INTEGER PRIMARY KEY", "table_name TEXT", "last_update TEXT"]

    # Create the tables
    create_table("characters", character_fields)
    create_table("races", race_fields)
    create_table("classes", class_fields)
    create_table("equipment", equipment_fields)
    create_table("updates", update_fields)

def insert_into_table(table_name, fields, values):
    try:
        # Prepare the placeholders for the INSERT command
        placeholders = ', '.join('?' * len(values))

        # Prepare the SQL command
        sql_command = f"INSERT OR REPLACE INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"

        # Execute the SQL command
        c.execute(sql_command, values)

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting into table {table_name}: {e}")

def select_from_table(table_name, fields, condition=None):
    try:
        # Prepare the SQL command
        sql_command = f"SELECT {', '.join(fields)} FROM {table_name}"
        if condition is not None:
            sql_command += f" WHERE {condition}"

        # Execute the SQL command
        c.execute(sql_command)

        # Fetch the results
        return c.fetchall()
    except sqlite3.Error as e:
        print(f"Error selecting from table {table_name}: {e}")

def delete_from_table(table_name):
    try:
        # Prepare the SQL command
        sql_command = f"DELETE FROM {table_name}"

        # Execute the SQL command
        c.execute(sql_command)

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting from table {table_name}: {e}")

# Create a function to fetch and store data from the DnD API once every 60 days
def fetch_and_store_data():
    
    # Initialize last_update time
    insert_into_table('updates', ['id', 'table_name', 'last_update'], [1, 'races', '2000-01-01'])
    insert_into_table('updates', ['id', 'table_name', 'last_update'], [2, 'classes', '2000-01-01'])
    insert_into_table('updates', ['id', 'table_name', 'last_update'], [3, 'equipment', '2000-01-01'])
    
    # Check last update time
    last_update = select_from_table('updates', ['last_update'], "table_name = 'races'")
    # last_update = c.fetchone()
    if last_update is None or (datetime.datetime.now() - datetime.datetime.strptime(last_update[0][0], "%Y-%m-%d")).days > 60:
        # Fetch and store races
        response = requests.get(f"{API_URL}/api/races")
        races = response.json()['results']
        # Clear table
        delete_from_table('races')
        for race in races:
            insert_into_table('races', ['race'], [race['index']])
        # Update last update time
        insert_into_table('updates', ['id', 'table_name', 'last_update'], [1, 'races', datetime.datetime.now().strftime("%Y-%m-%d")])

    # Do the same for classes 
    last_update = select_from_table('updates', ['last_update'], "table_name = 'classes'")
    # last_update = c.fetchone()
    if last_update is None or (datetime.datetime.now() - datetime.datetime.strptime(last_update[0][0], "%Y-%m-%d")).days > 60:
        # Fetch and store classes
        response = requests.get(f"{API_URL}/api/classes")
        classes = response.json()['results']
        # Clear table
        delete_from_table('classes')
        for _class in classes:
            insert_into_table('classes', ['class'], [_class['index']])
        # Update last update time
        insert_into_table('updates', ['id', 'table_name', 'last_update'], [2, 'classes', datetime.datetime.now().strftime("%Y-%m-%d"),])

    # Do the same for equipment
    last_update = select_from_table('updates', ['last_update'], "table_name = 'equipment'")
    # last_update = c.fetchone()
    if last_update is None or (datetime.datetime.now() - datetime.datetime.strptime(last_update[0][0], "%Y-%m-%d")).days > 60:
        # Fetch and store equipment
        response = requests.get(f"{API_URL}/api/equipment")
        equipment_list = response.json()['results']
        # Clear table
        delete_from_table('equipment')
        for equipment in equipment_list:
            insert_into_table('equipment', ['equipment'], [equipment['index']])
        # Update last update time
        insert_into_table('updates', ['id', 'table_name', 'last_update'], [3, 'equipment', datetime.datetime.now().strftime("%Y-%m-%d")])

    # Commit the changes
    conn.commit()

def get_random_race():
    return dnd_utils.get_random_from_api("/api/races")

def get_random_class():
    return dnd_utils.get_random_from_api("/api/classes")

def get_random_equipment():
    return dnd_utils.get_random_from_api("/api/equipment")

def roll_ability_score():
    roll = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(roll)[1:])  # Discard the lowest roll

def generate_character_name(race):
    response = exponential_backoff(lambda: openai.Completion.create(engine="text-davinci-003", prompt= f"Generate a unique name for a {race} fantasy character ", max_tokens=30))
    return response.choices[0].text.strip()

def generate_character():
    race = get_random_race()
    _class = get_random_class()
    equipment = get_random_equipment()
    name = generate_character_name(race)
    stats = roll_character_stats()
    character = {
        "name": name,
        "race": race,
        "class": _class,
        "equipment": equipment,
        "stats": stats,
    }
    return character

def roll_character_stats():
    abilities = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    stats = {ability: roll_ability_score() for ability in abilities}
    return stats

def generate_backstory(character):
    # Themes for the backstory chosen at random
    themes = ["heroic", "dark", "tragic", "magical"]
    theme = random.choice(themes)
    prompt = f"Generate a {theme} backstory for a {character['race']} {character['class']} named {character['name']} who carries a {character['equipment']}, including their motivations and fears that led them to become an adventurer."
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
    return response.choices[0].text.strip()

def output_to_database(character, backstory):
    insert_into_table(
        'characters', ['name', 'race', '_class', 'equipment', 'backstory'],
        [character['name'], character['race'], character['class'], character['equipment'], backstory]
        )

if __name__ == "__main__":
    fetch_and_store_data()
    character = generate_character()
    print(character)
    backstory = generate_backstory(character)
    print("Backstory:")
    print(backstory)
    output_to_database(character, backstory)

conn.close()