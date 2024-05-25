import os
import sqlite3
import requests

# Ensure the database directory exists
db_dir = 'db'
db_path = os.path.join(db_dir, 'villagernpc.db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# workplace data
stat_weights = {
        'blacksmith': ['Strength', 'Constitution', 'Dexterity', 'Intelligence', 'Wisdom', 'Charisma'],
        'innkeeper': ['Charisma', 'Constitution', 'Intelligence', 'Wisdom', 'Dexterity', 'Strength'],
        'merchant': ['Charisma', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Strength'],
        'farmer': ['Constitution', 'Strength', 'Wisdom', 'Dexterity', 'Intelligence', 'Charisma'],
        'healer': ['Wisdom', 'Intelligence', 'Charisma', 'Constitution', 'Dexterity', 'Strength'],
        'guard': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'soldier': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'fisherman': ['Dexterity', 'Wisdom', 'Constitution', 'Strength', 'Intelligence', 'Charisma'],
        'herbalist': ['Wisdom', 'Intelligence', 'Dexterity', 'Constitution', 'Charisma', 'Strength'],
        'tailor': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'seamstress': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'butcher': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'carpenter': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'miner': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'entertainer': ['Charisma', 'Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Strength'],
        'alchemist': ['Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma', 'Strength'],
        'priest': ['Wisdom', 'Charisma', 'Intelligence', 'Constitution', 'Dexterity', 'Strength'],
        'priestess': ['Wisdom', 'Charisma', 'Intelligence', 'Constitution', 'Dexterity', 'Strength'],
        'trapper': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Intelligence', 'Charisma'],
        'hunter': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Intelligence', 'Charisma'],
        'chef': ['Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma', 'Strength'],
        'librarian': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'scribe': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'stablemaster': ['Wisdom', 'Dexterity', 'Constitution', 'Strength', 'Intelligence', 'Charisma'],
        'ranger': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Intelligence', 'Charisma'],
        'shipwright': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'thief': ['Dexterity', 'Intelligence', 'Charisma', 'Wisdom', 'Constitution', 'Strength'],
        'wizard': ['Intelligence', 'Wisdom', 'Charisma', 'Dexterity', 'Constitution', 'Strength'],
        'sorcerer': ['Intelligence', 'Wisdom', 'Charisma', 'Dexterity', 'Constitution', 'Strength'],
        'leatherworker': ['Dexterity', 'Strength', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma'],
        'jeweler': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'courier': ['Dexterity', 'Constitution', 'Charisma', 'Wisdom', 'Intelligence', 'Strength'],
        'brewer': ['Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'potter': ['Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'miller': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'cobbler': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'weaver': ['Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma', 'Strength'],
        'shepherd': ['Wisdom', 'Constitution', 'Strength', 'Dexterity', 'Intelligence', 'Charisma'],
        'chandler': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'tanner': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'cooper': ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'glassblower': ['Dexterity', 'Strength', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma'],
        'fletcher': ['Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma', 'Strength'],
        'bowyer': ['Dexterity', 'Strength', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma'],
        'stonecutter': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'silversmith': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'apothecary': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'lumberjack': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'woodcutter': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'cartographer': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'beekeeper': ['Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Charisma', 'Strength'],
        'messenger': ['Dexterity', 'Constitution', 'Charisma', 'Wisdom', 'Intelligence', 'Strength'],
        'crier': ['Charisma', 'Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Strength'],
        'gardener': ['Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Charisma', 'Strength'],
        'falconer': ['Wisdom', 'Dexterity', 'Constitution', 'Charisma', 'Intelligence', 'Strength'],
        'peddler': ['Charisma', 'Dexterity', 'Wisdom', 'Intelligence', 'Constitution', 'Strength'],
        'herald': ['Charisma', 'Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Strength'],
        'saddler': ['Dexterity', 'Strength', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma'],
        'ferrier': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'caravan_leader': ['Charisma', 'Wisdom', 'Strength', 'Constitution', 'Dexterity', 'Intelligence'],
        'dyer': ['Dexterity', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma', 'Strength'],
        'toymaker': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'fortuneteller': ['Wisdom', 'Charisma', 'Intelligence', 'Dexterity', 'Constitution', 'Strength'],
        'gravedigger': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'lamplighter': ['Dexterity', 'Wisdom', 'Constitution', 'Charisma', 'Intelligence', 'Strength'],
        'brewers_assistant': ['Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'inn_cook': ['Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'basket_weaver': ['Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma', 'Strength'],
        'ropemaker': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'stable_hand': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'barber': ['Dexterity', 'Charisma', 'Wisdom', 'Intelligence', 'Constitution', 'Strength'],
        'arcane_blacksmith': ['Strength', 'Constitution', 'Dexterity', 'Intelligence', 'Wisdom', 'Charisma'],
        'mystic_innkeeper': ['Charisma', 'Constitution', 'Intelligence', 'Wisdom', 'Dexterity', 'Strength'],
        'enchanted_merchant': ['Charisma', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Strength'],
        'elemental_farmer': ['Constitution', 'Strength', 'Wisdom', 'Dexterity', 'Intelligence', 'Charisma'],
        'divine_healer': ['Wisdom', 'Intelligence', 'Charisma', 'Constitution', 'Dexterity', 'Strength'],
        'rune_guard': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'aquamancer_fisherman': ['Dexterity', 'Wisdom', 'Constitution', 'Strength', 'Intelligence', 'Charisma'],
        'herbalist_sage': ['Wisdom', 'Intelligence', 'Dexterity', 'Constitution', 'Charisma', 'Strength'],
        'spellweaver_tailor': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'mage_baker': ['Constitution', 'Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Strength'],
        'spirit_butcher': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'enchanted_carpenter': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'mystic_miner': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'bardic_entertainer': ['Charisma', 'Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Strength'],
        'potion_master_alchemist': ['Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma', 'Strength'],
        'divine_priest': ['Wisdom', 'Charisma', 'Intelligence', 'Constitution', 'Dexterity', 'Strength'],
        'divine_priestess': ['Wisdom', 'Charisma', 'Intelligence', 'Constitution', 'Dexterity', 'Strength'],
        'arcane_trapper': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Intelligence', 'Charisma'],
        'hunter_druid': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Intelligence', 'Charisma'],
        'enchanted_chef': ['Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma', 'Strength'],
        'librarian_wizard': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'stable_enchanter': ['Wisdom', 'Dexterity', 'Constitution', 'Strength', 'Intelligence', 'Charisma'],
        'ranger_mage': ['Dexterity', 'Wisdom', 'Strength', 'Constitution', 'Intelligence', 'Charisma'],
        'shipwright_sorcerer': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'shadow_thief': ['Dexterity', 'Intelligence', 'Charisma', 'Wisdom', 'Constitution', 'Strength'],
        'archmage': ['Intelligence', 'Wisdom', 'Charisma', 'Dexterity', 'Constitution', 'Strength'],
        'leatherworker_enchanter': ['Dexterity', 'Strength', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma'],
        'mystic_tavern_keeper': ['Charisma', 'Constitution', 'Wisdom', 'Intelligence', 'Dexterity', 'Strength'],
        'enchanter_jeweler': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'arcane_courier': ['Dexterity', 'Constitution', 'Charisma', 'Wisdom', 'Intelligence', 'Strength'],
        'brewer_alchemist': ['Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'mystic_potter': ['Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'arcane_miller': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'cobbler_conjurer': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'weaver_of_spells': ['Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma', 'Strength'],
        'shepherd_enchanter': ['Wisdom', 'Constitution', 'Strength', 'Dexterity', 'Intelligence', 'Charisma'],
        'chandler_of_light': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'arcane_tanner': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'mystic_cooper': ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'glassblower_sorcerer': ['Dexterity', 'Strength', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma'],
        'fletcher_sage': ['Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma', 'Strength'],
        'bowyer_enchanter': ['Dexterity', 'Strength', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma'],
        'stonecutter_mage': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'silversmith_conjurer': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'mystic_apothecary': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'lumberjack_elementalist': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'woodcutter_elementalist': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'cartographer_diviner': ['Intelligence', 'Wisdom', 'Dexterity', 'Charisma', 'Constitution', 'Strength'],
        'beekeeper_alchemist': ['Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Charisma', 'Strength'],
        'messenger_sprite': ['Dexterity', 'Constitution', 'Charisma', 'Wisdom', 'Intelligence', 'Strength'],
        'crier_bard': ['Charisma', 'Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Strength'],
        'gardener_druid': ['Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Charisma', 'Strength'],
        'falconer_sorcerer': ['Wisdom', 'Dexterity', 'Constitution', 'Charisma', 'Intelligence', 'Strength'],
        'peddler_illusionist': ['Charisma', 'Dexterity', 'Wisdom', 'Intelligence', 'Constitution', 'Strength'],
        'herald_enchanter': ['Charisma', 'Wisdom', 'Dexterity', 'Constitution', 'Intelligence', 'Strength'],
        'saddler_mage': ['Dexterity', 'Strength', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma'],
        'ferrier_enchanter': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'caravan_leader_sage': ['Charisma', 'Wisdom', 'Strength', 'Constitution', 'Dexterity', 'Intelligence'],
        'dyer_illusionist': ['Dexterity', 'Intelligence', 'Constitution', 'Wisdom', 'Charisma', 'Strength'],
        'toymaker_enchanter': ['Dexterity', 'Intelligence', 'Wisdom', 'Charisma', 'Constitution', 'Strength'],
        'fortuneteller_diviner': ['Wisdom', 'Charisma', 'Intelligence', 'Dexterity', 'Constitution', 'Strength'],
        'gravedigger_necromancer': ['Strength', 'Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma'],
        'lamplighter_luminar': ['Dexterity', 'Wisdom', 'Constitution', 'Charisma', 'Intelligence', 'Strength'],
        'brewers_assistant_alchemist': ['Constitution', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'inn_cook_enchanter': ['Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma', 'Strength'],
        'basket_weaver_sage': ['Dexterity', 'Intelligence', 'Wisdom', 'Constitution', 'Charisma', 'Strength'],
        'ropemaker_sorcerer': ['Dexterity', 'Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
        'stable_hand_enchanter': ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'],
        'barber_conjurer': ['Dexterity', 'Charisma', 'Wisdom', 'Intelligence', 'Constitution', 'Strength']
    }

def create_table(cursor, table_name, fields):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    fields_str = ", ".join(fields)
    cursor.execute(f"CREATE TABLE {table_name} ({fields_str})")

def fetch_and_store_data(cursor, table_name, api_url, fields, starting_id):
    item_id = starting_id
    next_url = api_url
    while next_url:
        try:
            response = requests.get(next_url)
            response.raise_for_status()
            data = response.json()
            items_list = data["results"]
            for item in items_list:
                if len(fields) == 2:  # For tables with 2 fields (id, name)
                    cursor.execute(f'INSERT INTO {table_name}({", ".join(fields)}) VALUES (?, ?)', 
                                   (item_id, item["name"]))
                elif len(fields) == 3:  # For tables with 3 fields (id, name, document_url)
                    cursor.execute(f'INSERT INTO {table_name}({", ".join(fields)}) VALUES (?, ?, ?)', 
                                   (item_id, item["name"], item.get("document__slug", "")))
                item_id += 1
            next_url = data["next"]
        except requests.RequestException as e:
            print(f"Failed to fetch data from {api_url}: {e}")
            break

def main():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Create and populate workplace table
        create_table(cursor, "workplace", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "stat_order TEXT NOT NULL"])
        for i, (class_name, stat_order) in enumerate(stat_weights.items(), start=1):
            stat_order_str = ','.join(stat_order)
            cursor.execute('INSERT INTO workplace(id, name, stat_order) VALUES (?, ?, ?)', (i, class_name, stat_order_str))

        # Create races table
        create_table(cursor, "races", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL"])

        # Fetch and store races
        fetch_and_store_data(cursor, "races", "https://api.open5e.com/races/", ["id", "name"], 1)

        # Create equipment table
        create_table(cursor, "equipment", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "document_url TEXT NOT NULL"])

        # Fetch and store equipment
        equipment_endpoints = ["https://api.open5e.com/weapons/", "https://api.open5e.com/armor/"]
        starting_id = 1
        for endpoint in equipment_endpoints:
            fetch_and_store_data(cursor, "equipment", endpoint, ["id", "name", "document_url"], starting_id)
            starting_id += 1000  # Ensure IDs don't overlap

        # Create magic items table
        create_table(cursor, "magic_items", ["id INTEGER PRIMARY KEY", "name TEXT NOT NULL", "document_url TEXT NOT NULL"])

        # Fetch and store magic items
        fetch_and_store_data(cursor, "magic_items", "https://api.open5e.com/magicitems/", ["id", "name", "document_url"], starting_id)

if __name__ == "__main__":
    main()