import os
import random
import requests
import openai
from dotenv import load_dotenv
import sqlite3
import datetime
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
    character_fields = ["id INTEGER PRIMARY KEY", "name TEXT", "race TEXT", "_class TEXT", "equipment TEXT", "backstory TEXT", "strength INTEGER", "dexterity INTEGER", "constitution INTEGER", "intelligence INTEGER", "wisdom INTEGER", "charisma INTEGER"]
    race_fields = ["id INTEGER PRIMARY KEY", "race TEXT"]
    class_fields = ["id INTEGER PRIMARY KEY", "class TEXT"]
    equipment_fields = ["id INTEGER PRIMARY KEY", "equipment TEXT"]
    character_stats_fields = ["character_id INTEGER, strength INTEGER, dexterity INTEGER, constitution INTEGER, intelligence INTEGER, wisdom INTEGER, charisma INTEGER,  FOREIGN KEY(character_id) REFERENCES characters(id)"]
    update_fields = ["id INTEGER PRIMARY KEY", "table_name TEXT", "last_update TEXT"]

    # Create the tables
    create_table("characters", character_fields)


def insert_into_table(table_name, fields, values):
    try:
        # Connect to the database and create a cursor
        conn = sqlite3.connect('db/characters.db')
        c = conn.cursor()

        # Prepare the placeholders for the INSERT command
        placeholders = ', '.join('?' * len(values))

        # Prepare the SQL command
        sql_command = f"INSERT OR REPLACE INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"

        # Execute the SQL command
        c.execute(sql_command, values)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        c.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error inserting into table {table_name}: {e}")

def select_from_table(table_name, fields, condition=None):
    try:
        # Connect to the database and create a cursor
        conn = sqlite3.connect('db/characters.db')
        c = conn.cursor()

        # Prepare the SQL command
        sql_command = f"SELECT {', '.join(fields)} FROM {table_name}"
        if condition is not None:
            sql_command += f" WHERE {condition}"

        # Execute the SQL command
        c.execute(sql_command)

        # Fetch the results
        results = c.fetchall()

        # Close the cursor and connection
        c.close()
        conn.close()

        return results
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

def get_random_race():
    races = select_from_table('races', ['name'])
    race = random.choice(races)[0]
    return race

def get_random_class():
    classes = select_from_table('classes', ['name', 'stat_order'])
    _class, stat_order_str = random.choice(classes)
    stat_order = stat_order_str.split(',')
    return _class, stat_order

def get_random_equipment():
    equipment_list = select_from_table('equipment', ['equipment'])
    equipment = random.choice(equipment_list)[0]
    return equipment

def roll_ability_score():
    roll = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(roll)[1:])  # Discard the lowest roll

def generate_character_name(race):
    response = exponential_backoff(lambda: openai.Completion.create(engine="text-davinci-003", prompt= f"Generate a unique name for a {race} fantasy character ", max_tokens=30))
    return response.choices[0].text.strip()

def roll_character_stats():
    # Roll 6 ability scores without assigning them to specific abilities yet
    stats = [roll_ability_score() for _ in range(6)]
    return stats

def generate_character():
    race = get_random_race()
    _class, stat_order = get_random_class()

    # Roll stats and sort them in descending order, since higher ability scores are generally better
    stats = sorted(roll_character_stats(), reverse=True)

    # Map sorted stats to abilities based on class stat_order
    abilities = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    sorted_abilities = {ability: stat for ability, stat in zip(stat_order, stats)}

    equipment = get_random_equipment()
    name = generate_character_name(race)

    character = {
        "name": name,
        "race": race,
        "class": _class,
        "equipment": equipment,
        "stats": sorted_abilities,
    }
    return character


def generate_backstory(character):
    # Themes for the backstory chosen at random
    themes = ["heroic", "dark", "tragic", "magical"]
    theme = random.choice(themes)
    prompt = f"Generate a {theme} backstory for a {character['race']} {character['class']} named {character['name']} who carries a {character['equipment']}, including their motivations and fears that led them to become an adventurer."
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
    return response.choices[0].text.strip()

def output_to_database(character, backstory):
    # Extract the stats from the character in the order that matches your database
    stats = character['stats']
    strength = stats['Strength']
    dexterity = stats['Dexterity']
    constitution = stats['Constitution']
    intelligence = stats['Intelligence']
    wisdom = stats['Wisdom']
    charisma = stats['Charisma']

    insert_into_table(
        'characters', 
        ['name', 'race', '_class', 'equipment', 'backstory', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'],
        [character['name'], character['race'], character['class'], character['equipment'], backstory, strength, dexterity, constitution, intelligence, wisdom, charisma]
    )

if __name__ == "__main__":
    character = generate_character()
    print(character)
    backstory = generate_backstory(character)
    print(f"Backstory:")
    print(backstory)
    
    output_to_database(character, backstory)

conn.close()