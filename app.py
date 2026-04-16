from flask import Flask, redirect, render_template, request, session, flash
import markupsafe
import config
import destinations
import errors
import validations
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        errors.forbidden()

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    all_destinations = destinations.get_destinations()
    return render_template("index.html", destinations=all_destinations)

@app.route("/register")
def register():
    return render_template("register.html", filled={})

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("VIRHE: Antamasi salasanat eivät ole samat.")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    if not validations.check_registration(username, password1):
        flash("Käyttäjätunnus tai salasana on liian lyhyt.")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    if users.create_user(username, password1):
        flash("Tunnus luotu onnistuneesti! Kirjaudu vielä sisään.")
        return redirect("/login")
    flash("VIRHE: Käyttäjätunnus on jo varattu. Valitse toinen tunnus.")
    return redirect("/register")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={}, next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)
        if user_id:
            session["username"] = username
            session["user_id"] = user_id

            if "register" in next_page:
                return redirect("/")
            return redirect(next_page)

        flash("VIRHE: Väärä käyttäjätunnus tai salasana.")
        filled = {"username": username}
        return render_template("login.html", filled=filled,  next_page=next_page)

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        errors.not_found()
    user_destinations = users.get_destinations(user_id)
    return render_template("show_user.html", user=user, user_destinations=user_destinations)

@app.route("/new_destination")
def new_destination():
    require_login()
    classes = destinations.get_all_classes()
    return render_template("new_destination.html", classes=classes)

@app.route("/create_destination", methods=["POST"])
def create_destination():
    require_login()
    title = request.form["title"]
    content = request.form["description"]
    user_id = session["user_id"]

    if not validations.check_destination(title, content):
        errors.forbidden()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))

    destination_id = destinations.add_destination(title, content, user_id, classes)
    flash("Uusi retkikohde lisätty onnistuneesti!")
    return redirect(f"/destination/{ destination_id }")

@app.route("/destination/<int:destination_id>")
def show_destination(destination_id):
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    classes = destinations.get_classes(destination_id)

    return render_template("show_destination.html", destination=destination, classes=classes)

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
    flash("Retkikohde päivitetty onnistuneesti!")
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
