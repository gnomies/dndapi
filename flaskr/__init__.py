from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../flaskr/db/characters.db'
db = SQLAlchemy(app)

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(80), nullable=False)
    _class = db.Column(db.String(80), nullable=False)
    equipment = db.Column(db.String(80), nullable=False)
    backstory = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)

if __name__ == '__main__':
    app.run(debug=True)