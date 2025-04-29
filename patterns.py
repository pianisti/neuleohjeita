import db

def add_pattern(title, description, user_id):
    sql = "INSERT INTO patterns (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

def get_patterns():
    sql = "SELECT id, title FROM patterns ORDER BY id DESC"
    return db.query(sql)

def get_pattern(pattern_id):
    sql = """SELECT patterns.id, patterns.title, patterns.description, users.username, users.id user_id
             FROM patterns, users
             WHERE patterns.user_id = users.id AND patterns.id = ?"""
    result = db.query(sql, [pattern_id])
    return result[0] if result else None

def update_pattern(pattern_id, title, description):
    sql = "UPDATE patterns SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, pattern_id])

def remove_pattern(pattern_id):
    sql = "DELETE FROM patterns WHERE id = ?"
    db.execute(sql, [pattern_id])

def find_patterns(query):
    sql = """SELECT id, title
             FROM patterns
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
