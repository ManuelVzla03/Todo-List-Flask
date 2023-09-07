from flask import Blueprint, render_template, request, g, redirect, url_for
from todor.auth import loguin_required
from .models import Todo
from todor import db

bp = Blueprint("todo", __name__, url_prefix="/todo")


@bp.route("/list")
@loguin_required
def index():
    todos = Todo.query.all()
    return render_template("todo/index.html", todos=todos)


@bp.route("/create", methods=["POST", "GET"])
@loguin_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]

        todo = Todo(g.user.id_user, title, desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo.index"))
    return render_template("todo/create.html")


def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo


@bp.route("/update/<int:id>", methods=["POST", "GET"])
@loguin_required
def update(id):
    todo = get_todo(id)
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        todo.state = True if request.form.get("state") == "on" else False

        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template("todo/update.html", todo = todo)

@bp.route("/delete/<int:id>")
@loguin_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))