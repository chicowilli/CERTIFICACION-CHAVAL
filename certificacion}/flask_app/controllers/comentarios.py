from flask import redirect, request, session, url_for
from flask_app import app
from flask_app.models.comentarios import Comment


@app.route("/cine/<int:movie_id>/comentar", methods=["POST"])
def comentar(movie_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    if not request.form["content"].strip():
        return redirect(url_for("ver_peli", id=movie_id))

    data = {
        "content": request.form["content"],
        "user_id": session["user_id"],
        "movie_id": movie_id,
    }
    Comment.save(data)
    return redirect(url_for("ver_peli", id=movie_id))


@app.route("/cine/comentario/<int:id>/borrar")
def borrar_comentario(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    Comment.delete(id)
    return redirect(request.referrer or url_for("cine"))