import sqlite3
from datetime import date
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import destinations
import errors
import validations

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        errors.forbidden()

@app.route("/")
def index():
    all_destinations = destinations.get_destinations()
    return render_template("index.html", destinations=all_destinations)

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

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        if len(result) == 0:
            return "VIRHE: väärä tunnus tai salasana"

        user_id = result[0][0]
        password_hash = result[0][1]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/new_destination")
def new_destination():
    require_login()
    return render_template("new_destination.html")

@app.route("/create_destination", methods=["POST"])
def create_destination():
    require_login()
    title = request.form["title"]
    content = request.form["description"]
    creation_time = date.today()
    user_id = session["user_id"]

    if not validations.check_destination(title, content):
        errors.forbidden()

    destinations.add_destination(title, content, creation_time, user_id)

    return redirect("/")

@app.route("/destination/<int:destination_id>")
def show_destination(destination_id):
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    return render_template("show_destination.html", destination=destination)

@app.route("/edit_destination/<int:destination_id>")
def edit_destination(destination_id):
    require_login()
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    return render_template("edit_destination.html", destination=destination)

@app.route("/update_destination", methods=["POST"])
def update_destination():
    require_login()
    destination_id = request.form["destination_id"]
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    title = request.form["title"]
    content = request.form["description"]

    if not validations.check_destination(title, content):
        errors.forbidden()

    destinations.update_destination(destination_id, title, content)

    return redirect("/destination/" + str(destination_id))

@app.route("/remove_destination/<int:destination_id>", methods=["GET", "POST"])
def remove_destination(destination_id):
    require_login()
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    if request.method == "GET":
        return render_template("remove_destination.html", destination=destination)

    if request.method == "POST":
        if "remove" in request.form:
            destinations.remove_destination(destination_id)
            return redirect("/")
        else:
            return redirect("/destination/" + str(destination_id))

@app.route("/find_destination")
def find_destination():
    query = request.args.get("query")
    if query:
        results = destinations.find_destinations(query)
    else:
        query = ""
        results = []
    return render_template("find_destination.html", query=query, results=results)
