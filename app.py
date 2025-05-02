import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import patterns
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_patterns = patterns.get_patterns()
    return render_template("index.html", patterns=all_patterns)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    patterns = users.get_patterns(user_id)
    return render_template("show_user.html", user=user, patterns=patterns)

@app.route("/find_pattern")
def find_pattern():
    query = request.args.get("query")
    if query:
        results = patterns.find_patterns(query)
    else:
        query = ""
        results = []
    return render_template("find_pattern.html", query=query, results=results)

@app.route("/pattern/<int:pattern_id>")
def show_pattern(pattern_id):
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        abort(404)
    classes = patterns.get_classes(pattern_id)
    return render_template("show_pattern.html", pattern=pattern, classes=classes)

@app.route("/new_pattern")
def new_pattern():
    require_login()
    classes, elements = patterns.get_all_classes()
    return render_template("new_pattern.html", classes=classes, elements=elements)

@app.route("/create_pattern", methods=["POST"])
def create_pattern():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1500:
        abort(403)
    user_id = session["user_id"]

    all_classes, elements = patterns.get_all_classes()

    classes = []
    for one_class in all_classes:
        value = request.form[f"{one_class}"]
        if value:
            classes.append((f"{one_class}", value))

    patterns.add_pattern(title, description, user_id, classes)

    return redirect("/")

@app.route("/edit_pattern/<int:pattern_id>")
def edit_pattern(pattern_id):
    require_login()
    pattern = patterns.get_pattern(pattern_id)
    if not pattern:
        abort(404)
    if pattern["user_id"] != session["user_id"]:
        abort(403)

    all_classes, elements = patterns.get_all_classes()
    classes = {}
    for entry in patterns.get_classes(pattern_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_pattern.html", pattern=pattern, all_classes=all_classes, classes=classes, elements=elements)

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
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1500:
        abort(403)

    all_classes, elements = patterns.get_all_classes()

    classes = []
    for one_class in all_classes:
        value = request.form[f"{one_class}"]
        if value:
            classes.append((f"{one_class}", value))

    patterns.update_pattern(pattern_id, title, description, classes)

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

    try:
        users.create_user(username, password1)
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

        user_id = users.check_login(username, password)
        if user_id:
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
