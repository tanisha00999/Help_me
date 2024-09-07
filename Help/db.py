# db.py

import sqlite3

def get_connection():
    conn = sqlite3.connect('problems.db')
    return conn

def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems
        (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, prayers INTEGER)
    ''')
    conn.commit()
    conn.close()

def add_problem(title, description):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO problems (title, description, prayers)
        VALUES (?, ?, 0)
    ''', (title, description))
    conn.commit()
    conn.close()

def get_problems():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems')
    problems = c.fetchall()
    conn.close()
    return problems

def update_prayer_count(problem_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE problems
        SET prayers = prayers + 1
        WHERE id = ?
    ''', (problem_id,))
    conn.commit()
    conn.close()

def delete_problem(problem_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM problems WHERE id = ?', (problem_id,))
    conn.commit()
    conn.close()
