from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from marshmallow import ValidationError
from app.extensions import db
from app.models.category import Category
from app.schemas import category_schema, categories_schema

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
@login_required
def index():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.type, Category.name).all()
    return render_template("categories/index.html", categories=categories)


@categories_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        try:
            category_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("categories/form.html", category=None)

        category = Category(
            user_id=current_user.id,
            name=request.form["name"],
            type=request.form["type"],
        )
        db.session.add(category)
        db.session.commit()
        flash("Categoría creada.", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/form.html", category=None)


@categories_bp.route("/<string:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        try:
            category_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("categories/form.html", category=category)

        category.name = request.form["name"]
        category.type = request.form["type"]
        db.session.commit()
        flash("Categoría actualizada.", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/form.html", category=category)


@categories_bp.route("/<string:category_id>/delete", methods=["POST"])
@login_required
def delete(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    db.session.delete(category)
    db.session.commit()
    flash("Categoría eliminada.", "info")
    return redirect(url_for("categories.index"))
