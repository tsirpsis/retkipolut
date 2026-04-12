import sqlite3
from werkzeug.security import generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False
