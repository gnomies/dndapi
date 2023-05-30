from flask import Flask, render_template, request
import creator
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Connect to the database and create a cursor
    conn = sqlite3.connect('db/characters.db')
    c = conn.cursor()

    # Query the database for all characters
    c.execute("SELECT * FROM characters")
    character_tuples = c.fetchall()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Convert character tuples to dictionaries
    characters = [dict(zip(["id", "name", "race", "_class", "equipment", "backstory", "stats"], character_tuple)) for character_tuple in character_tuples]

    new_character = None
    if request.method == 'POST':
        new_character = creator.generate_character()
        backstory = creator.generate_backstory(new_character)
        creator.output_to_database(new_character, backstory)

    return render_template('home.html', characters=characters, new_character=new_character)


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
    character = dict(zip(["id", "name", "race", "_class", "equipment", "backstory", "stats"], character_tuple))

    # Render a template for the character
    return render_template('character.html', character=character)



if __name__ == '__main__':
    app.run(debug=True)