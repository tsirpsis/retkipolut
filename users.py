import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0][0]
    password_hash = result[0][1]

    if check_password_hash(password_hash, password):
        return user_id
    return None

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_destinations(user_id):
    sql = """SELECT id,
                    title,
                    strftime('%d.%m.%Y', creation_time) AS creation_time
                    FROM destinations WHERE user_id = ?"""
    return db.query(sql, [user_id])
