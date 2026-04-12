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
