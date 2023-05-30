import sqlite3

# Create a connection to the database
conn = sqlite3.connect('db\characters.db')
cursor = conn.cursor()

# Delete the existing table if it exists
cursor.execute("DROP TABLE IF EXISTS races")

# Then, create the table
cursor.execute('''
    CREATE TABLE races(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

# Read races from file and insert them into the database
with open('db\dndraces.txt', 'r') as f:
    races = f.read().splitlines()

for i, race in enumerate(races, start=1):
    cursor.execute('''
        INSERT INTO races(id, name)
        VALUES (?, ?)
    ''', (i, race))

conn.commit()  # Commit the changes

# Remember to close the connection when you're done
conn.close()