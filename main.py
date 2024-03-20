from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('notes.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS notes
    (latitude REAL, longitude REAL, note TEXT)
''')
conn.commit()

@app.route('/')
def home():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/submit_note', methods=['POST'])
def submit_note():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        note = data['note']

        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('INSERT INTO notes VALUES (?, ?, ?)', (latitude, longitude, note))
        conn.commit()

        return 'Note submitted successfully!', 201

    return 'Invalid request method', 405

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    notes = c.fetchall()
    conn.close()
    return json.dumps(notes), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)