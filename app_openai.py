from flask import Flask, render_template, request
import creator_openai as creator_openai
import sqlite3
import os
import glob


app = Flask(__name__, template_folder='static/templates', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def home():
    class_filter = request.args.get('class')

    # Connect to the database and create a cursor
    conn = sqlite3.connect('db/characters.db')
    c = conn.cursor()

    # Query the database for all classes
    c.execute("SELECT DISTINCT _class FROM characters")
    classes = [row[0] for row in c.fetchall()]

    # Query the database for all characters or characters of a specific class
    if class_filter:
        c.execute("SELECT * FROM characters WHERE _class=?", (class_filter,))
    else:
        c.execute("SELECT * FROM characters")

    character_tuples = c.fetchall()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Convert character tuples to dictionaries
    characters = [dict(zip(["id", "name", "race", "_class", "equipment", "backstory", "stats"], character_tuple)) for character_tuple in character_tuples]

    new_character = None
    backstory = None   # initialize backstory
    if request.method == 'POST':
        new_character = creator_openai.generate_character()
        backstory = creator_openai.generate_backstory(new_character)
        creator_openai.output_to_database(new_character, backstory)

    return render_template('home.html', characters=characters, character=new_character, backstory=backstory)

@app.route('/character/<int:character_id>', methods=['GET'])
def character(character_id):
    # Connect to the database and create a cursor
    conn = sqlite3.connect('db/characters.db')
    c = conn.cursor()

    # Query the database for the character with the given ID
    c.execute("SELECT * FROM characters WHERE id=?", (character_id,))
    character_tuple = c.fetchone()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Convert character tuple to a dictionary
    character = dict(zip(["id", "name", "race", "_class", "equipment", "backstory", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"], character_tuple))

    # Create a dictionary of stats
    stats_dict = {
        'Strength': character['strength'],
        'Dexterity': character['dexterity'],
        'Constitution': character['constitution'],
        'Intelligence': character['intelligence'],
        'Wisdom': character['wisdom'],
        'Charisma': character['charisma']
    }

    # Add the stats dictionary to the character dictionary
    character['stats'] = stats_dict

    print(f"Stats dictionary: {stats_dict}")  # Debug line

    # Add the stats dictionary to the character dictionary
    character['stats'] = stats_dict

    # Render a template for the character
    return render_template('character.html', character=character)

if __name__ == '__main__':
    template_files = glob.glob('./static/**/*.html', recursive=True)
    app.run(debug=True, extra_files=template_files)