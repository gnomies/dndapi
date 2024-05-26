import os
import subprocess
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Path to the database
db_path = 'db/villagernpc.db'

def get_all_characters():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, name, race, _class FROM characters')
    characters = c.fetchall()
    c.close()
    conn.close()
    return characters

def get_character_by_id(character_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT name, race, _class, equipment, magic_item, backstory, strength, dexterity, constitution, intelligence, wisdom, charisma, image_filename FROM characters WHERE id = ?', (character_id,))
    character = c.fetchone()
    c.close()
    conn.close()
    return character

def run_script():
    script_path = 'npc_creator_anthropic.py'
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    # The script outputs the character and backstory in the console.
    output_lines = result.stdout.strip().split("\n")
    character = eval(output_lines[0])  # Assuming the first line is the character dictionary
    backstory = "\n".join(output_lines[2:])  # Assuming the rest is the backstory
    return character, backstory

@app.route('/')
def index():
    characters = get_all_characters()
    return render_template('index.html', characters=characters)

@app.route('/character/<int:character_id>')
def character_detail(character_id):
    character = get_character_by_id(character_id)
    if character:
        return render_template('character_detail.html', character=character)
    else:
        return "Character not found", 404

@app.route('/add', methods=['GET'])
def add_character():
    character, backstory = run_script()

    name = character['name']
    race = character['race']
    character_class = character['_class']
    equipment = character['equipment']
    magic_item = character['magic_item']
    strength = character['stats']['Strength']
    dexterity = character['stats']['Dexterity']
    constitution = character['stats']['Constitution']
    intelligence = character['stats']['Intelligence']
    wisdom = character['stats']['Wisdom']
    charisma = character['stats']['Charisma']
    image_filename = character.get('image_filename')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO characters (name, race, _class, equipment, magic_item, backstory, strength, dexterity, constitution, intelligence, wisdom, charisma, image_filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (name, race, character_class, equipment, magic_item, backstory, strength, dexterity, constitution, intelligence, wisdom, charisma, image_filename))
    conn.commit()
    c.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
