import sqlite3
import requests

# Classes data
stat_weights = {
    'barbarian': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Charisma', 'Intelligence'],
    'bard': ['Charisma', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Strength'],
    'cleric': ['Wisdom', 'Strength', 'Constitution', 'Charisma', 'Dexterity', 'Intelligence'],
    'druid': ['Wisdom', 'Constitution', 'Dexterity', 'Intelligence', 'Charisma', 'Strength'],
    'fighter': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
    'monk': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Charisma', 'Intelligence'],
    'paladin': ['Strength', 'Charisma', 'Constitution', 'Wisdom', 'Dexterity', 'Intelligence'],
    'ranger': ['Dexterity', 'Wisdom', 'Constitution', 'Strength', 'Charisma', 'Intelligence'],
    'rogue': ['Dexterity', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma', 'Strength'],
    'sorcerer': ['Charisma', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Strength'],
    'warlock': ['Charisma', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Strength'],
    'wizard': ['Intelligence', 'Constitution', 'Dexterity', 'Wisdom', 'Charisma', 'Strength'],
    'bloodhunter': ['Dexterity', 'Constitution', 'Intelligence', 'Strength', 'Charisma', 'Wisdom'],
}

# Function to create a table
def create_table(cursor, table_name, fields):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    fields_str = ", ".join(fields)
    cursor.execute(f"CREATE TABLE {table_name} ({fields_str})")

# Create a connection to the database
conn = sqlite3.connect('db/characters.db')
cursor = conn.cursor()

# Create the classes table
create_table(cursor, "classes", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "stat_order TEXT NOT NULL"])
# Insert the classes and their stat orders into the database
for i, (class_name, stat_order) in enumerate(stat_weights.items(), start=1):
    stat_order_str = ','.join(stat_order)
    cursor.execute('INSERT INTO classes(id, name, stat_order) VALUES (?, ?, ?)', (i, class_name, stat_order_str))

conn.commit()

# Fetch and store races data from the Open5e API
def fetch_and_store_races():
    response = requests.get("https://api.open5e.com/races/")
    if response.status_code == 200:
        races_list = response.json()["results"]
        create_table(cursor, "races", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL"])
        for i, race in enumerate(races_list, start=1):
            cursor.execute('INSERT INTO races(id, name) VALUES (?, ?)', (i, race["name"]))
        conn.commit()
    else:
        print("Failed to fetch races from API")

fetch_and_store_races()

# Fetch and store equipment data from the Open5e API
def fetch_and_store_equipment():
    equipment_endpoints = ["weapons", "armor"]
    create_table(cursor, "equipment", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "document_url TEXT NOT NULL"])
    
    item_id = 1
    for endpoint in equipment_endpoints:
        next_url = f"https://api.open5e.com/{endpoint}/"
        while next_url:
            response = requests.get(next_url)
            if response.status_code == 200:
                data = response.json()
                equipment_list = data["results"]
                for equipment in equipment_list:
                    cursor.execute('INSERT INTO equipment(id, name, document_url) VALUES (?, ?, ?)', 
                                   (item_id, equipment["name"], equipment["document__slug"]))
                    item_id += 1
                next_url = data["next"]
            else:
                print(f"Failed to fetch {endpoint} from API")
                break

    conn.commit()

fetch_and_store_equipment()

# Fetch and store magic items data from the Open5e API
def fetch_and_store_magic_items():
    create_table(cursor, "magic_items", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "document_url TEXT NOT NULL"])
    
    item_id = 1
    next_url = "https://api.open5e.com/magicitems/"
    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            magic_items_list = data["results"]
            for magic_item in magic_items_list:
                cursor.execute('INSERT INTO magic_items(id, name, document_url) VALUES (?, ?, ?)', 
                               (item_id, magic_item["name"], magic_item["document__slug"]))
                item_id += 1
            next_url = data["next"]
        else:
            print("Failed to fetch magic items from API")
            break

    conn.commit()

fetch_and_store_magic_items()

# Commit and close the connection
conn.commit()
conn.close()
