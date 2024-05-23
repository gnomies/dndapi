import os
import random
import sqlite3
import requests
import anthropic
from dotenv import load_dotenv
import time

# Load .env file
load_dotenv()

# Get Anthropic API key from .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

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
    character_fields = ["id INTEGER PRIMARY KEY", "name TEXT", "race TEXT", "_class TEXT", "equipment TEXT", "magic_item TEXT", "backstory TEXT", "strength INTEGER", "dexterity INTEGER", "constitution INTEGER", "intelligence INTEGER", "wisdom INTEGER", "charisma INTEGER"]
    race_fields = ["id INTEGER PRIMARY KEY", "race TEXT"]
    class_fields = ["id INTEGER PRIMARY KEY", "class TEXT"]
    equipment_fields = ["id INTEGER PRIMARY KEY", "equipment TEXT"]
    magic_item_fields = ["id INTEGER PRIMARY KEY", "magic_item TEXT"]
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

# Initialize Anthropic client
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def exponential_backoff(func, max_retries=5):
    wait_time = 1
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            else:
                print(f"Request failed with {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2
                wait_time += random.uniform(0, 1)

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
    equipment_list = select_from_table('equipment', ['name'])
    equipment = random.choice(equipment_list)[0]
    return equipment

def get_random_magic_item():
    magic_items_list = select_from_table('magic_items', ['name'])
    magic_item = random.choice(magic_items_list)[0]
    return magic_item

def roll_ability_score():
    roll = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(roll)[1:])

def generate_character_name(race):
    response = exponential_backoff(lambda: anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=20,
        messages=[
            {"role": "user", "content": f"Generate a unique name for a {race} fantasy character"}
        ]
    ))
    # Extracting the text content from the response
    name = next(item.text for item in response.content if item.type == 'text')
    return name.strip()

def roll_character_stats():
    stats = [roll_ability_score() for _ in range(6)]
    return stats

def generate_character():
    race = get_random_race()
    _class, stat_order = get_random_class()
    stats = sorted(roll_character_stats(), reverse=True)
    abilities = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    sorted_abilities = {ability: stat for ability, stat in zip(stat_order, stats)}
    equipment = get_random_equipment()
    magic_item = get_random_magic_item()
    name = generate_character_name(race)
    character = {
        "name": name,
        "race": race,
        "class": _class,
        "equipment": equipment,
        "magic_item": magic_item,
        "stats": sorted_abilities,
    }
    return character

def generate_backstory(character):
    themes = ["heroic", "dark", "tragic", "magical", "alternate world", "astral plane", "time travel"]
    theme = random.choice(themes)
    prompt = f"Generate a {theme} backstory for a {character['race']} {character['class']} named {character['name']} who carries a {character['equipment']} and a {character['magic_item']}, including their motivations and fears that led them to become an adventurer.Short description of what they sound and look like"
    response = exponential_backoff(lambda: anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    ))
    # Extracting the text content from the response
    backstory = next(item.text for item in response.content if item.type == 'text')
    return backstory.strip()

def insert_into_table(table_name, fields, values):
    try:
        conn = sqlite3.connect('db/characters.db')
        c = conn.cursor()
        placeholders = ', '.join('?' * len(values))
        sql_command = f"INSERT OR REPLACE INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
        c.execute(sql_command, values)
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error inserting into table {table_name}: {e}")

def select_from_table(table_name, fields, condition=None):
    try:
        conn = sqlite3.connect('db/characters.db')
        c = conn.cursor()
        sql_command = f"SELECT {', '.join(fields)} FROM {table_name}"
        if condition is not None:
            sql_command += f" WHERE {condition}"
        c.execute(sql_command)
        results = c.fetchall()
        c.close()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Error selecting from table {table_name}: {e}")

def output_to_database(character, backstory):
    stats = character['stats']
    strength = stats['Strength']
    dexterity = stats['Dexterity']
    constitution = stats['Constitution']
    intelligence = stats['Intelligence']
    wisdom = stats['Wisdom']
    charisma = stats['Charisma']
    insert_into_table(
        'characters', 
        ['name', 'race', '_class', 'equipment', 'magic_item', 'backstory', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'],
        [character['name'], character['race'], character['class'], character['equipment'], character['magic_item'], backstory, strength, dexterity, constitution, intelligence, wisdom, charisma]
    )

if __name__ == "__main__":
    character = generate_character()
    print(character)
    backstory = generate_backstory(character)
    print(f"Backstory:")
    print(backstory)
    output_to_database(character, backstory)
