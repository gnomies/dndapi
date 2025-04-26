import os
import random
import sqlite3
import requests
import anthropic
from dotenv import load_dotenv
import time

# Load .env file
load_dotenv()

# Database paths
DB_PATH = 'db/characters.db'  # Single database for both reference and character data

def get_reference_connection():
    """Get connection to reference data (read-only intent)"""
    return sqlite3.connect(DB_PATH)

def get_character_connection():
    """Get connection for character data (read-write)"""
    return sqlite3.connect(DB_PATH)

# Get Anthropic API key from .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

# Initialize Anthropic client
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
# Seed with current time in milliseconds
random.seed(int(time.time() * 1000))

import secrets
def get_random_race():
    try:
        with get_reference_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM races")
            races = c.fetchall()
            if not races:
                raise ValueError("No races found in database")
            # Use secrets module for better randomness
            random_index = secrets.randbelow(len(races))
            return races[random_index][0]
    except sqlite3.Error as e:
        print(f"Error getting race: {e}")
        return None
    
# Organize themes by category
NPC_THEMES = {
    "personal_struggles": [
        "Overcoming Self-Doubt",
        "Breaking Family Traditions",
        "Finding Purpose",
        "Redemption from Past Mistakes",
        "Living with Chronic Limitations"
    ],
    "social_themes": [
        "Burden of Expectations",
        "Torn Between Two Worlds",
        "Secret Double Life",
        "Forbidden Knowledge",
        "Unspoken Obligations"
    ],
    "philosophical": [
        "Questioning Faith",
        "The Weight of Responsibility",
        "Freedom vs. Security",
        "Legacy and Remembrance",
        "The Cost of Power"
    ],
    "fantasy_specific": [
        "Cursed Blessing",
        "Magical Corruption",
        "Ancient Prophecy Burden",
        "Lost Heritage",
        "Magical Exhaustion"
    ],
    "emotional": [
        "Survivor's Guilt",
        "Haunted by Success",
        "Fear of Change",
        "Perfectionism Paralysis",
        "Emotional Numbness"
    ],
    "aspirations": [
        "Seeking Lost Treasure",
        "Building a Legacy",
        "Mastering an Ancient Art",
        "Discovering New Lands",
        "Creating Magical Innovations"
    ],
    "relationships": [
        "Rivalries and Competition",
        "Mentoring the Next Generation",
        "Star-Crossed Romance",
        "Blood Feuds",
        "Unlikely Partnerships"
    ],
    "occupational": [
        "Professional Pride",
        "Trade Secrets",
        "Guild Politics",
        "Entrepreneurial Spirit",
        "Craft Obsession"
    ],
    "positive_traits": [
        "Boundless Curiosity",
        "Unwavering Loyalty",
        "Infectious Optimism",
        "Natural Leadership",
        "Creative Problem-Solver"
    ],
    "active_quests": [
        "Hunting a Specific Monster",
        "Gathering Rare Components",
        "Solving Ancient Mysteries",
        "Defending the Vulnerable",
        "Expanding Business Empire"
    ],
    "cultural_identity": [
        "Cultural Ambassador",
        "Preserving Old Ways",
        "Bridging Two Cultures",
        "Revolutionary Ideas",
        "Traditional vs Modern"
    ],
    "magical_interests": [
        "Experimental Magic Research",
        "Artifact Collection",
        "Magical Conservation",
        "Spell Innovation",
        "Magical Archaeology"
    ]
}

def create_table(table_name, fields):
    try:
        with get_character_connection() as conn:
            c = conn.cursor()
            fields_str = ", ".join(fields)
            c.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name}
                ({fields_str})
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table {table_name}: {e}")

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
    try:
        with get_reference_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM races")
            races = c.fetchall()
            if not races:
                raise ValueError("No races found in database")
            return random.choice(races)[0]
    except sqlite3.Error as e:
        print(f"Error getting race: {e}")
        return None
    
def get_random_class():
    try:
        with get_reference_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name, stat_order FROM classes")
            classes = c.fetchall()
            print(f"Classes found: {classes}")  # Debug print
            if not classes:
                raise ValueError("No classes found in database")
            _class, stat_order_str = random.choice(classes)
            stat_order = stat_order_str.split(',')
            return _class, stat_order
    except sqlite3.Error as e:
        print(f"Error getting class: {e}")
        return None, None
    
def get_random_workplace():
    try:
        with get_reference_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name, stat_order FROM workplaces")
            workplaces = c.fetchall()
            if not workplaces:
                raise ValueError("No workplaces found in database")
            workplace, stat_order_str = random.choice(workplaces)
            stat_order = stat_order_str.split(',')
            return workplace, stat_order
    except sqlite3.Error as e:
        print(f"Error getting workplace: {e}")
        return None, None
    
def get_random_equipment():
    try:
        with get_reference_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM equipment")
            equipment_list = c.fetchall()
            if not equipment_list:
                raise ValueError("No equipment found in database")
            return random.choice(equipment_list)[0]
    except sqlite3.Error as e:
        print(f"Error getting equipment: {e}")
        return None

def get_random_magic_item():
    try:
        with get_reference_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM magic_items")
            magic_items_list = c.fetchall()
            if not magic_items_list:
                raise ValueError("No magic items found in database")
            return random.choice(magic_items_list)[0]
    except sqlite3.Error as e:
        print(f"Error getting magic item: {e}")
        return None

def roll_ability_score():
    roll = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(roll)[1:])

def generate_character_name(race, gender_weights={"male": 50, "female": 50}): # Adjust for better balances.
    genders = list(gender_weights.keys())
    weights = list(gender_weights.values())
    gender = random.choices(genders, weights=weights, k=1)[0]
    
    response = exponential_backoff(lambda: anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=30,
        messages=[
            {"role": "user", "content": f"Generate ONLY a name (first and last) for a {gender} {race} fantasy NPC character. Respond with just the name, nothing else."}
        ]
    ))
    name = next(item.text for item in response.content if item.type == 'text')
    cleaned_name = name.strip().split('\n')[0]
    if len(cleaned_name) > 50:
        cleaned_name = cleaned_name[:50]
    return cleaned_name, gender

def generate_character(character_type="adventurer"):
    race = get_random_race()
    if race is None:
        raise ValueError("Could not get a random race from the database")
    
    if character_type == "adventurer":
        profession, stat_order = get_random_class()
    else:  # villager
        profession, stat_order = get_random_workplace()
    
    if profession is None or stat_order is None:
        raise ValueError(f"Could not get {character_type} profession from the database")

    stats = sorted(roll_character_stats(), reverse=True)
    sorted_abilities = {ability: stat for ability, stat in zip(stat_order, stats)}
    equipment = get_random_equipment()
    magic_item = get_random_magic_item()
    name, gender = generate_character_name(race)
    
    character = {
        "name": name,
        "gender": gender,
        "race": race,
        "profession": profession,  # This can be either class or workplace
        "type": character_type,    # Keep track of whether it's an adventurer or villager
        "equipment": equipment,
        "magic_item": magic_item,
        "stats": sorted_abilities,
    }
    return character

def roll_character_stats():
    stats = [roll_ability_score() for _ in range(6)]
    return stats

def generate_backstory(character):
    # Randomly select a category, then a theme from that category
    category = random.choice(list(NPC_THEMES.keys()))
    theme = random.choice(NPC_THEMES[category])
    
    # Adjust the prompt based on character type
    profession_type = "class" if character['type'] == "adventurer" else "occupation"
    
    prompt = f"""Create a short NPC backstory (2-3 paragraphs) for:
    - Name: {character['name']}
    - Race: {character['race']}
    - {profession_type.capitalize()}: {character['profession']}
    - Equipment: {character['equipment']}
    - Magic Item: {character['magic_item']}
    - Theme: {theme}
    - Character Type: {character['type']} NPC
    
    Create a backstory where the character is ACTIVELY involved in their profession or calling. Avoid the trope of retired or former adventurers unless specifically relevant to the theme.
    
    Include:
    1. How the theme drives their current activities
    2. A recent incident that demonstrates this theme
    3. Their ongoing goals and motivations
    4. How they interact with others in pursuit of their goals
    
    Make sure the character is vibrant, active, and engaged in the world, not just defined by past failures or retirements."""

    # Make the API call
    response = exponential_backoff(lambda: anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    ))

    # Extracting the text content from the response
    backstory = next(item.text for item in response.content if item.type == 'text')
    return backstory.strip()

def output_to_database(character, backstory):
    try:
        with get_character_connection() as conn:
            c = conn.cursor()
            stats = character['stats']
            c.execute('''
                INSERT INTO characters 
                (name, gender, race, profession, type, equipment, magic_item, backstory, 
                 strength, dexterity, constitution, intelligence, wisdom, charisma)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (character['name'], character['gender'], character['race'], character['profession'], 
                  character['type'], character['equipment'], character['magic_item'], 
                  backstory, stats['Strength'], stats['Dexterity'], stats['Constitution'], 
                  stats['Intelligence'], stats['Wisdom'], stats['Charisma']))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting character: {e}")

def view_characters():
    try:
        with get_character_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM characters ORDER BY id DESC LIMIT 5")
            characters = c.fetchall()
            for char in characters:
                print(f"\nCharacter: {char[1]} ({char[2]} {char[3]})")
                print(f"Type: {char[4]}")
                print(f"Equipment: {char[5]}")
                print(f"Magic Item: {char[6]}")
                print(f"Stats: STR {char[8]}, DEX {char[9]}, CON {char[10]}, INT {char[11]}, WIS {char[12]}, CHA {char[13]}")
                print(f"Backstory: {char[7][:100]}...")  # First 100 characters
    except sqlite3.Error as e:
        print(f"Error viewing characters: {e}")

if __name__ == "__main__":
    # Define table structures
    character_fields = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "name TEXT",
        "gender TEXT",
        "race TEXT",
        "profession TEXT", # This can be either a class or workplace
        "type TEXT", # "adventurer" or "villager"
        "equipment TEXT",
        "magic_item TEXT",
        "backstory TEXT",
        "strength INTEGER",
        "dexterity INTEGER",
        "constitution INTEGER",
        "intelligence INTEGER",
        "wisdom INTEGER",
        "charisma INTEGER"
    ]
    
    # Create tables if they don't exist
    create_table("characters", character_fields)
    
    # Generate multiple characters
    num_characters = 100  # Change this to however many you want
    
    for i in range(num_characters):
        print(f"\n{'='*50}")
        print(f"Generating character {i+1} of {num_characters}")
        print(f"{'='*50}\n")
        
        # Generate either an adventurer or villager
        character_type = "villager" #random.choice(["adventurer", "villager"])
        
        # Generate character
        character = generate_character(character_type)
        print(f"Generated {character_type} character:")
        print(character)
        
        # Generate backstory
        backstory = generate_backstory(character)
        print(f"Backstory:")
        print(backstory)
        
        # Save to database
        output_to_database(character, backstory)
        
        # Optional: Add a small delay to avoid API rate limits
        time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"Successfully generated {num_characters} characters!")
    print(f"{'='*50}")