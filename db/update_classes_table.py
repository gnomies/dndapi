import sqlite3

# stat_weights.py

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

# Create a connection to the database
conn = sqlite3.connect('db\characters.db')
cursor = conn.cursor()

# Delete the existing table if it exists
cursor.execute("DROP TABLE IF EXISTS classes")

# Then, create the table
cursor.execute('''
    CREATE TABLE classes(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        stat_order TEXT NOT NULL
    )
''')

# Insert the classes and their stat orders into the database
for i, (class_name, stat_order) in enumerate(stat_weights.items(), start=1):
    # Serialize the stat order as a comma-separated string
    stat_order_str = ','.join(stat_order)
    
    cursor.execute('''
        INSERT INTO classes(id, name, stat_order)
        VALUES (?, ?, ?)
    ''', (i, class_name, stat_order_str))

conn.commit()  # Commit the changes

# Remember to close the connection when you're done
conn.close()