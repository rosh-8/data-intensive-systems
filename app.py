from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def create_databases():
    databases = {
        "students.db": "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, course TEXT)",
        "books.db": "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)",
        "employees.db": "CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT)"
    }

    for db, query in databases.items():
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(query)
        table = db.split('.')[0]
        count = cur.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]

        if count == 0:
            if table == 'students':
                cur.executemany('INSERT INTO students(name, course) VALUES (?, ?)', [('John','IT'),('Emma','Business')])
            elif table == 'books':
                cur.executemany('INSERT INTO books(title, author) VALUES (?, ?)', [('Python Basics','Mike'),('React Guide','Sarah')])
            else:
                cur.executemany('INSERT INTO employees(name, department) VALUES (?, ?)', [('Alice','HR'),('Bob','Finance')])

        conn.commit()
        conn.close()

create_databases()

@app.route('/data/<db>')
def get_data(db):
    conn = sqlite3.connect(f'{db}.db')
    conn.row_factory = sqlite3.Row
    rows = conn.execute(f'SELECT * FROM {db}').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/data/<db>', methods=['POST'])
def add_data(db):
    data = request.json
    conn = sqlite3.connect(f'{db}.db')
    cur = conn.cursor()

    if db == 'students':
        cur.execute('INSERT INTO students(name, course) VALUES (?, ?)', (data['name'], data['course']))
    elif db == 'books':
        cur.execute('INSERT INTO books(title, author) VALUES (?, ?)', (data['title'], data['author']))
    else:
        cur.execute('INSERT INTO employees(name, department) VALUES (?, ?)', (data['name'], data['department']))

    conn.commit()
    conn.close()
    return {'message':'Added'}

if __name__ == '__main__':
    app.run(debug=True)
