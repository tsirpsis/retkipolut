import secrets
from flask import Flask, redirect, render_template, request, session, flash, make_response
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

def check_csrf():
    if "csrf_token" not in request.form:
        errors.forbidden()
    if request.form["csrf_token"] != session["csrf_token"]:
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
        flash("VIRHE: Antamasi salasanat eivät täsmää. Anna salasanat uudelleen.","error")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    if not validations.check_registration(username, password1):
        flash("VIRHE: Käyttäjätunnus tai salasana on liian lyhyt tai pitkä.", "error")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    if users.create_user(username, password1):
        flash("Tunnus luotu onnistuneesti! Voit nyt kirjautua sisään.", "success")
        return redirect("/login")
    flash("VIRHE: Käyttäjätunnus on jo varattu. Valitse toinen tunnus.", "error")
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
            session["csrf_token"] = secrets.token_hex(16)

            if "register" in next_page:
                return redirect("/")
            return redirect(next_page)

        flash("VIRHE: Väärä käyttäjätunnus tai salasana.", "error")
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
    user_comments = users.get_comments(user_id)

    return render_template("show_user.html", user=user,
                           user_destinations=user_destinations,
                           user_comments=user_comments)

@app.route("/new_destination")
def new_destination():
    require_login()

    classes = destinations.get_all_classes()
    return render_template("new_destination.html", classes=classes)

@app.route("/create_destination", methods=["POST"])
def create_destination():
    require_login()
    check_csrf()

    title = request.form["title"]
    content = request.form["description"]
    user_id = session["user_id"]

    if not validations.check_destination(title, content):
        errors.forbidden()

    entries = request.form.getlist("classes")
    all_classes = destinations.get_all_classes()

    classes = validations.check_classes(entries, all_classes)
    if classes == [] or classes:
        destination_id = destinations.add_destination(title, content, user_id, classes)
        flash("Uusi retkikohde lisätty onnistuneesti!", "success")
        return redirect("/destination/" + str(destination_id))
    errors.forbidden()

@app.route("/destination/<int:destination_id>")
def show_destination(destination_id):
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()

    session["destination_id"] = destination["id"]

    classes = destinations.get_classes(destination_id)
    comments = destinations.get_comments(destination_id)
    images = destinations.get_images(destination_id)

    return render_template("show_destination.html",
                           destination=destination, classes=classes,
                           comments=comments, images=images)

@app.route("/edit_destination/<int:destination_id>")
def edit_destination(destination_id):
    require_login()
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    all_classes = destinations.get_all_classes()
    classes = {}
    for category in all_classes:
        classes[category] = ""
    for entry in destinations.get_classes(destination_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_destination.html", destination=destination,
                            all_classes=all_classes, classes=classes)

@app.route("/update_destination", methods=["POST"])
def update_destination():
    require_login()
    check_csrf()

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

    entries = request.form.getlist("classes")
    all_classes = destinations.get_all_classes()

    classes = validations.check_classes(entries, all_classes)
    if classes == [] or classes:
        destinations.update_destination(destination_id, title, content, classes)
        flash("Retkikohde päivitetty onnistuneesti!", "success")
        return redirect("/destination/" + str(destination_id))
    errors.forbidden()

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
        check_csrf()
        if "remove" in request.form:
            destinations.remove_destination(destination_id)
            flash("Retkikohde poistettu onnistuneesti!", "success")
            return redirect("/")
        return redirect("/destination/" + str(destination_id))

@app.route("/find_destination")
def find_destination():
    query = request.args.get("query")
    if query:
        results, count = destinations.find_destinations(query)
    else:
        query = ""
        results = []
        count = 0
    return render_template("find_destination.html", query=query,
                           results=results, count=count)

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    user_id = session["user_id"]
    destination_id = request.form["destination_id"]

    content = request.form["content"]
    if not validations.check_comment(content):
        errors.forbidden()

    session_destination_id = session.get("destination_id")
    destination = destinations.get_destination(destination_id)

    if not destination:
        errors.not_found()
    if str(destination_id) != str(session_destination_id):
        errors.forbidden()

    destinations.add_comment(content, user_id, destination_id)
    return redirect("/destination/" + str(destination_id))

@app.route("/edit_comment/<int:comment_id>")
def edit_comment(comment_id):
    require_login()

    comment = users.get_comment(comment_id)
    if not comment:
        errors.not_found()
    if comment["user_id"] != session["user_id"]:
        errors.forbidden()

    return render_template("edit_comment.html", comment=comment)

@app.route("/update_comment", methods=["POST"])
def update_comment():
    require_login()
    check_csrf()

    comment_id = request.form["comment_id"]
    destination_id = request.form["destination_id"]

    comment = users.get_comment(comment_id)

    if not comment:
        errors.not_found()
    if comment["user_id"] != session["user_id"]:
        errors.forbidden()

    content = request.form["content"]

    if not validations.check_comment(content):
        errors.forbidden()

    users.update_comment(comment_id, content)
    flash("Kommentti päivitetty onnistuneesti!", "success")
    return redirect("/destination/" + str(destination_id))

@app.route("/images/<int:destination_id>")
def edit_images(destination_id):
    require_login()
    destination = destinations.get_destination(destination_id)

    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    images = destinations.get_images(destination_id)

    return render_template("images.html", destination=destination, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    destination_id = request.form["destination_id"]
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    file = request.files["image"]
    image_type = file.content_type

    image = file.read()

    if not validations.check_image_type(image_type):
        flash("VIRHE: Väärä tiedostomuoto. Tiedostomuodon tulee olla .jpg tai .png.", "error")
        return redirect("/images/" + str(destination_id))

    if not validations.check_image_size(image):
        flash("VIRHE: Liian suuri kuva. Kuvan maksimikoon tulee olla 500 KB.", "error")
        return redirect("/images/" + str(destination_id))

    destinations.add_image(image, image_type, destination_id)
    flash("Uusi kuva lisätty onnistuneesti!", "success")
    return redirect("/destination/" + str(destination_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image, image_type = destinations.get_image(image_id)

    if not image:
        errors.not_found()

    response = make_response(bytes(image))

    if image_type in ('image/jpg', 'image/jpeg'):
        response.headers.set("Content-Type", "image/jpeg")
    if image_type == 'image/png':
        response.headers.set("Content-Type", "image/png")

    return response

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    destination_id = request.form["destination_id"]
    destination = destinations.get_destination(destination_id)
    if not destination:
        errors.not_found()
    if destination["user_id"] != session["user_id"]:
        errors.forbidden()

    image_ids = request.form.getlist("image_id")

    if not image_ids:
        flash("VIRHE: Et ole valinnut yhtään kuvaa poistettavaksi.", "error")
        return redirect("/images/" + str(destination_id))

    for image_id in image_ids:
        destinations.remove_image(image_id, destination_id)

    flash("Kuva(t) poistettu onnistuneesti!", "success")
    return redirect("/images/" + str(destination_id))
