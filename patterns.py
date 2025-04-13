import db

def add_pattern(title, description, user_id):
    sql = "INSERT INTO patterns (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])
