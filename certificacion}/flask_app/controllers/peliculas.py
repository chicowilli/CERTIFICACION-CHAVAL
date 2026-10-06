from flask import render_template, request, redirect
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.peliculas import Movie
from flask_app.models.usuarios import User


@app.route("/cine")
def cine():
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = User.get_by_id(session["user_id"])
    movies = Movie.get_all()
    return render_template("cine.html", user=user, movies=movies)


@app.route("/cine/nueva")
def nueva_peli():
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = User.get_by_id(session["user_id"])
    return render_template("nuevapeli.html", user=user)


@app.route("/cine/crear", methods=["POST"])
def crear_peli():
    if "user_id" not in session:
        return redirect(url_for("index"))

    data = {
        "title": request.form["title"],
        "director": request.form["director"],
        "release_date": request.form["release_date"],
        "synopsis": request.form["synopsis"],
        "user_id": session["user_id"],
    }

    if not Movie.validate(data):
        return redirect(url_for("nueva_peli"))

    Movie.save(data)
    return redirect(url_for("cine"))


@app.route("/cine/<int:id>")
def ver_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = User.get_by_id(session["user_id"])
    movie = Movie.get_by_id(id)
    if not movie:
        return redirect(url_for("cine"))
    return render_template("verpeli.html", user=user, movie=movie)


@app.route("/cine/editar/<int:id>")
def editar_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie:
        return redirect(url_for("cine"))
    if movie.user_id != session["user_id"]:
        flash("Solo puedes editar las películas que creaste.", "peli")
        return redirect(url_for("cine"))

    user = User.get_by_id(session["user_id"])
    return render_template("editarpeli.html", user=user, movie=movie)


@app.route("/cine/actualizar/<int:id>", methods=["POST"])
def actualizar_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie or movie.user_id != session["user_id"]:
        return redirect(url_for("cine"))

    data = {
        "id": id,
        "title": request.form["title"],
        "director": request.form["director"],
        "release_date": request.form["release_date"],
        "synopsis": request.form["synopsis"],
    }

    if not Movie.validate(data):
        return redirect(url_for("editar_peli", id=id))

    Movie.update(data)
    return redirect(url_for("cine"))


@app.route("/cine/borrar/<int:id>")
def borrar_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie or movie.user_id != session["user_id"]:
        return redirect(url_for("cine"))

    Movie.delete(id)
    return redirect(url_for("cine"))