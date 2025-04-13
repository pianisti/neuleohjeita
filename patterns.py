import db

def add_pattern(title, description, user_id):
    sql = "INSERT INTO patterns (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

def get_patterns():
    sql = "SELECT id, title FROM patterns ORDER BY id DESC"
    return db.query(sql)

def get_pattern(pattern_id):
    sql = """SELECT patterns.title, patterns.description, users.username
             FROM patterns, users
             WHERE patterns.user_id = users.id AND patterns.id = ?"""
    return db.query(sql, [pattern_id])[0]
