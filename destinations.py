import db

def add_destination(title, content, creation_time, user_id):
        sql = "INSERT INTO destinations (title, content, creation_time, user_id) VALUES (?, ?, ?, ?)"
        db.execute(sql, [title, content, creation_time, user_id])

def get_destinations():
        sql = "SELECT id, title FROM destinations ORDER BY title"
        return db.query(sql)

def get_destination(destination_id):
        sql = """SELECT destinations.title,
                        destinations.content,
                        destinations.creation_time,
                        users.username
                FROM destinations, users
                WHERE destinations.user_id = users.id AND
                      destinations.id = ?"""
        return db.query(sql, [destination_id])[0]