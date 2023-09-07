from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
    g,
)
from .models import User
from todor import db
from werkzeug.security import generate_password_hash, check_password_hash
import functools

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, generate_password_hash(password))

        error = None

        user_name = User.query.filter_by(username=username).first()

        if user_name is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            error = f"El usuario {username} ya está registrado"
        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None

        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            error = "Usuario o Password invalidos"

        if error is None:
            session.clear()
            session["user_id"] = user.id_user
            return redirect(url_for("todo.index"))
        flash(error)
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def loguin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
