import db

def get_all_classes():
    sql = "SELECT title, value, element FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    elements = {}
    for title, value, element in result:
        classes[title] = []
    for title, value, element in result:
        classes[title].append(value)
        elements[title] = element

    return classes, elements

def add_pattern(title, description, user_id, classes):
    sql = "INSERT INTO patterns (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

    pattern_id = db.last_insert_id()

    sql = "INSERT INTO pattern_classes (pattern_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [pattern_id, class_title, class_value])

def add_comment(pattern_id, user_id, comment):
    sql = "INSERT INTO comments (pattern_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [pattern_id, user_id, comment])

def get_comments(pattern_id):
    sql = """SELECT comments.comment,
                    comments.user_id,
                    users.id,
                    users.username
             FROM comments, users
             WHERE comments.pattern_id = ? AND comments.user_id = users.id
             ORDER BY comments.id"""
    return db.query(sql, [pattern_id])

def get_images(pattern_id):
    sql = "SELECT id FROM images WHERE pattern_id = ?"
    return db.query(sql, [pattern_id])

def add_image(pattern_id, image):
    sql = "INSERT INTO images (pattern_id, image) VALUES (?, ?)"
    db.execute(sql, [pattern_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(pattern_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND pattern_id = ?"
    db.execute(sql, [image_id, pattern_id])

def get_classes(pattern_id):
    sql = "SELECT title, value FROM pattern_classes WHERE pattern_id = ?"
    return db.query(sql, [pattern_id])

def get_patterns():
    sql = """SELECT patterns.id, patterns.user_id, patterns.title, users.id, users.username
             FROM patterns, users
             WHERE patterns.user_id = users.id
             ORDER BY patterns.id DESC"""
    return db.query(sql)

def get_pattern(pattern_id):
    sql = """SELECT patterns.id,
                    patterns.title,
                    patterns.description,
                    users.username,
                    users.id user_id
             FROM patterns, users
             WHERE patterns.user_id = users.id AND patterns.id = ?"""
    result = db.query(sql, [pattern_id])
    return result[0] if result else None

def update_pattern(pattern_id, title, description, classes):
    sql = "UPDATE patterns SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, pattern_id])

    sql = "DELETE FROM pattern_classes WHERE pattern_id = ?"
    db.execute(sql, [pattern_id])

    sql = "INSERT INTO pattern_classes (pattern_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [pattern_id, class_title, class_value])

def remove_pattern(pattern_id):
    sql = "DELETE FROM comments WHERE pattern_id = ?"
    db.execute(sql, [pattern_id])
    sql = "DELETE FROM images WHERE pattern_id = ?"
    db.execute(sql, [pattern_id])
    sql = "DELETE FROM pattern_classes WHERE pattern_id = ?"
    db.execute(sql, [pattern_id])
    sql = "DELETE FROM patterns WHERE id = ?"
    db.execute(sql, [pattern_id])

def find_patterns(query):
    sql = """SELECT id, title
             FROM patterns
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
