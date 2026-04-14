import db

def add_destination(title, content, user_id):
    sql = """INSERT INTO destinations (title, content, creation_time, user_id)
                VALUES (?, ?, datetime('now', 'localtime'), ?)"""
    db.execute(sql, [title, content, user_id])
    return db.last_insert_id()

def get_destinations():
    sql = "SELECT id, title FROM destinations ORDER BY title"
    return db.query(sql)

def get_destination(destination_id):
    sql = """SELECT destinations.id,
                destinations.title,
                destinations.content,
                strftime('%d.%m.%Y', destinations.creation_time) AS creation_time,
                users.id AS user_id,
                users.username
                FROM destinations, users
                WHERE destinations.user_id = users.id AND
                      destinations.id = ?"""
    result = db.query(sql, [destination_id])
    return result[0] if result else None

def update_destination(destination_id, title, content):
    sql = """UPDATE destinations
                SET title = ?, content = ?
                WHERE id = ?"""
    db.execute(sql, [title, content, destination_id])

def remove_destination(destination_id):
    sql = """DELETE FROM destinations WHERE id = ?"""
    db.execute(sql, [destination_id])

def find_destinations(query):
    sql = """SELECT id, title
                FROM destinations
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])
