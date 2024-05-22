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
    response = exponential_backoff(lambda: anthropic_client.completions.create(
        model="claude-v1",  # specify the model name
        prompt=f"\n\nHuman: Generate a unique name for a {race} fantasy character\n\nAssistant:",
        max_tokens_to_sample=30
    ))
    return response.completion.strip()

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
    themes = ["heroic", "dark", "tragic", "magical"]
    theme = random.choice(themes)
    prompt = f"\n\nHuman: Generate a {theme} backstory for a {character['race']} {character['class']} named {character['name']} who carries a {character['equipment']} and a {character['magic_item']}, including their motivations and fears that led them to become an adventurer.\n\nAssistant:"
    response = exponential_backoff(lambda: anthropic_client.completions.create(
        model="claude-v1",  # specify the model name
        prompt=prompt,
        max_tokens_to_sample=1000
    ))
    return response.completion.strip()

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
