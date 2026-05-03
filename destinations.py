import db

def add_destination(title, content, user_id, classes):
    sql = """INSERT INTO destinations (title, content, creation_time, user_id)
            VALUES (?, ?, datetime('now', 'localtime'), ?)"""
    db.execute(sql, [title, content, user_id])

    destination_id = db.last_insert_id()
    sql = """INSERT INTO destination_classes (title, value, destination_id)
            VALUES (?, ?, ?)"""
    for class_title, value in classes:
        db.execute(sql, [class_title, value, destination_id])
    return destination_id

def get_destinations():
    sql = """SELECT d.id,
                    d.title,
                    strftime('%d.%m.%Y', d.creation_time)
                    AS creation_time,
                    d.user_id,
                    u.id AS user_id,
                    u.username,
                    GROUP_CONCAT(dc.title || ': ' || dc.value, ', ') AS classes
            FROM destinations d
            JOIN users u ON d.user_id = u.id
            LEFT JOIN destination_classes dc ON d.id = dc.destination_id
            GROUP BY d.id
            ORDER BY d.id DESC"""
    return db.query(sql)

def get_destination(destination_id):
    sql = """SELECT d.id,
                    d.title,
                    d.content,
                    strftime('%d.%m.%Y', d.creation_time) AS creation_time,
                    u.id AS user_id,
                    u.username
            FROM destinations d, users u
            WHERE d.user_id = u.id AND d.id = ?"""
    result = db.query(sql, [destination_id])
    return result[0] if result else None

def update_destination(destination_id, title, content, classes):
    sql = """UPDATE destinations
            SET title = ?, content = ?
            WHERE id = ?"""
    db.execute(sql, [title, content, destination_id])

    sql = "DELETE FROM destination_classes WHERE destination_id = ?"
    db.execute(sql, [destination_id])

    sql = """INSERT INTO destination_classes (title, value, destination_id)
            VALUES (?, ?, ?)"""
    for class_title, value in classes:
        db.execute(sql, [class_title, value, destination_id])

def remove_destination(destination_id):
    sql = """DELETE FROM destinations WHERE id = ?"""
    db.execute(sql, [destination_id])

def find_destinations(query):
    sql = """SELECT id, title
            FROM destinations
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY id DESC"""

    results = db.query(sql, ["%" + query + "%", "%" + query + "%"])
    count = len(results)
    return results, count

def get_classes(destination_id):
    sql = """SELECT title, value
            FROM destination_classes
            WHERE destination_id = ?"""
    return db.query(sql, [destination_id])

def get_all_classes():
    sql = """SELECT title, value
            FROM classes
            ORDER BY id"""
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def add_comment(content, user_id, destination_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, destination_id)
            VALUES (?, datetime('now', 'localtime'), ?, ?)"""
    return db.execute(sql, [content, user_id, destination_id])

def get_comments(destination_id):
    sql = """SELECT c.id,
                    c.user_id,
                    u.username,
                    c.destination_id,
                    c.content,
                    strftime('%d.%m.%Y %H:%M', c.sent_at) AS sent_at
            FROM comments c, users u
            WHERE c.user_id = u.id AND c.destination_id = ?
            ORDER BY c.id"""
    return db.query(sql, [destination_id])

def add_image(image, image_type, destination_id):
    sql = """INSERT INTO images (image, image_type, destination_id)
            VALUES (?, ?, ?)"""
    db.execute(sql, [image, image_type,destination_id])

def get_images(destination_id):
    sql = "SELECT id FROM images WHERE destination_id = ?"
    return db.query(sql, [destination_id])

def get_image(image_id):
    sql = "SELECT image, image_type FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0] if result else None

def remove_image(image_id, destination_id):
    sql = """DELETE FROM images
            WHERE id = ? AND destination_id = ?"""
    db.execute(sql, [image_id, destination_id])
