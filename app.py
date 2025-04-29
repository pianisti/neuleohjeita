import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import patterns

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_patterns = patterns.get_patterns()
    return render_template("index.html", patterns=all_patterns)

@app.route("/pattern/<int:pattern_id>")
def show_pattern(pattern_id):
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        abort(404)
    return render_template("show_pattern.html", pattern=pattern)

@app.route("/new_pattern")
def new_patter():
    require_login()
    return render_template("new_pattern.html")

@app.route("/create_pattern", methods=["POST"])
def create_pattern():
    require_login()
    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"]

    patterns.add_pattern(title, description, user_id)

    return redirect("/")

@app.route("/edit_pattern/<int:pattern_id>")
def edit_pattern(pattern_id):
    require_login()
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        abort(404)
    if pattern["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_pattern.html", pattern=pattern)

@app.route("/update_pattern", methods=["POST"])
def update_pattern():
    require_login()
    pattern_id = request.form["pattern_id"]
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        abort(404)
    if pattern["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    description = request.form["description"]

    patterns.update_pattern(pattern_id, title, description)

    return redirect("/pattern/" + str(pattern_id))

@app.route("/remove_pattern/<int:pattern_id>", methods=["GET", "POST"])
def remove_pattern(pattern_id):
    require_login()
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        abort(404)
    if pattern["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_pattern.html", pattern=pattern)

    if request.method == "POST":
        if "remove" in request.form:
            patterns.remove_pattern(pattern_id)
            return redirect("/")
        else:
            return redirect("/pattern/" + str(pattern_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
