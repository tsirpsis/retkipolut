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
            FROM destinations WHERE user_id = ?
            ORDER BY id DESC"""
    return db.query(sql, [user_id])

def get_comments(user_id):
    sql = """SELECT u.id AS user_id,
                    c.id AS comment_id,
                    c.destination_id,
                    strftime('%d.%m.%Y %H:%M', c.sent_at) AS sent_at,
                    d.title
            FROM users u
            JOIN comments c ON u.id = c.user_id
            JOIN destinations d ON c.destination_id = d.id
            WHERE u.id = ?
            ORDER BY c.sent_at DESC"""
    return db.query(sql, [user_id])

def get_comment(comment_id):
    sql = """SELECT id,
                    user_id,
                    destination_id,
                    content,
                    strftime('%d.%m.%Y %H:%M', sent_at) AS sent_at
            FROM comments
            WHERE id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def update_comment(comment_id, content):
    sql = """UPDATE comments
            SET content = ?
            WHERE id = ?"""
    db.execute(sql, [content, comment_id])
