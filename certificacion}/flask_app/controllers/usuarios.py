from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.usuarios import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("registro.html")


@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect(url_for("index"))

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect(url_for("cine"))


@app.route("/login", methods=["POST"])
def login():
    is_valid, user = User.validate_login(request.form)
    if not is_valid:
        return redirect(url_for("index"))

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("La contraseña es incorrecta.", "login")
        return redirect(url_for("index"))

    session["user_id"] = user.id
    return redirect(url_for("cine"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))