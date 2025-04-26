import os
import random
import sqlite3
import time
from dotenv import load_dotenv
import anthropic

# Load .env file
load_dotenv()

# Get Anthropic API key from .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Path to the database
db_path = 'db/villagernpc.db'

# Initialize Anthropic client
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def create_table(table_name, fields):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        fields_str = ", ".join(fields)
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({fields_str})
        ''')
        conn.commit()
        c.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error creating table {table_name}: {e}")

if __name__ == "__main__":
    # Define the fields for each table as lists of strings
    character_fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "name TEXT", "race TEXT", "profession TEXT", "equipment TEXT", "magic_item TEXT", "backstory TEXT", "strength INTEGER", "dexterity INTEGER", "constitution INTEGER", "intelligence INTEGER", "wisdom INTEGER", "charisma INTEGER"]
    race_fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "race TEXT"]
    class_fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "class TEXT"]
    equipment_fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "equipment TEXT"]
    magic_item_fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "magic_item TEXT"]
    character_stats_fields = ["character_id INTEGER, strength INTEGER, dexterity INTEGER, constitution INTEGER, intelligence INTEGER, wisdom INTEGER, charisma INTEGER,  FOREIGN KEY(character_id) REFERENCES characters(id)"]
    update_fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "table_name TEXT", "last_update TEXT"]

    # Create the tables
    create_table("characters", character_fields)

def insert_into_table(table_name, fields, values):
    try:
        conn = sqlite3.connect(db_path)
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
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql_command = f"SELECT {', '.join(fields)} FROM {table_name}"
        if condition:
            sql_command += f" WHERE {condition}"
        c.execute(sql_command)
        results = c.fetchall()
        c.close()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Error selecting from table {table_name}: {e}")

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

def get_randomprofession():
    classes = select_from_table('workplace', ['name', 'stat_order'])
    profession, stat_order_str = random.choice(classes)
    stat_order = stat_order_str.split(',')
    return profession, stat_order

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
        max_tokens=30,
        messages=[
            {"role": "user", "content": f"Generate a unique name for a {race} fantasy npc character"}
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
    profession, stat_order = get_randomprofession()
    stats = sorted(roll_character_stats(), reverse=True)
    abilities = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    sorted_abilities = {ability: stat for ability, stat in zip(stat_order, stats)}
    equipment = get_random_equipment()
    magic_item = get_random_magic_item()
    name = generate_character_name(race)
    character = {
        "name": name,
        "race": race,
        "profession": profession,
        "equipment": equipment,
        "magic_item": magic_item,
        "stats": sorted_abilities,
    }
    return character

def generate_backstory(character):
    themes = ["Comfort in Routine", "Lack of Ambition", "Fear of Failure", "Insecurity", "Acceptance of Fate", "Contentment with Role", "Past Trauma", "Desire for Peace", "Bound by Magic", "Connection to the World", "Loved Ones", "Unrequited Love", "Wisdom and Insight", "Duty and Responsibility"]
    theme = random.choice(themes)
    prompt = f"Generate a {theme} short NPC backstory for a {character['race']} {character['profession']} named {character['name']} who carries a {character['equipment']} and a {character['magic_item']}, include a voice type and physical description that fits with their job title."
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

def output_to_database(character, backstory):
    stats = character['stats']
    insert_into_table(
        'characters', 
        ['name', 'race', 'profession', 'equipment', 'magic_item', 'backstory', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'],
        [character['name'], character['race'], character['profession'], character['equipment'], character['magic_item'], backstory, stats['Strength'], stats['Dexterity'], stats['Constitution'], stats['Intelligence'], stats['Wisdom'], stats['Charisma']]
    )

if __name__ == "__main__":
    character = generate_character()
    print(character)
    backstory = generate_backstory(character)
    print("Backstory:")
    print(backstory)
    output_to_database(character, backstory)
