from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "contacts.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
        """)
init_db()

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        contacts = conn.execute("SELECT * FROM contacts").fetchall()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                         (name, phone, email))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    with sqlite3.connect(DB_NAME) as conn:
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            conn.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
                         (name, phone, email, id))
            return redirect(url_for('index'))
        contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (id,)).fetchone()
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
