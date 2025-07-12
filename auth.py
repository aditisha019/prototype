import sqlite3
import hashlib
import streamlit as st

def initialize_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def create_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Hash the provided password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = c.fetchone()
    conn.close()
    
    return result is not None
