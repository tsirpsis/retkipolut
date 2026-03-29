import db

def add_destination(title, content, creation_time, user_id):
        sql = "INSERT INTO destinations (title, content, creation_time, user_id) VALUES (?, ?, ?, ?)"
        db.execute(sql, [title, content, creation_time, user_id])

