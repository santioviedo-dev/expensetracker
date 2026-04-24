from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
from app.extensions import db
from app.models.user import User
from app.models.account import Account
from app.models.category import Category
from app.schemas import register_schema, login_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("transactions.index"))

    if request.method == "POST":
        try:
            data = register_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(email=data["email"]).first():
            flash("El email ya está registrado.", "danger")
            return render_template("auth/register.html")

        user = User(email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)

        # Cuenta y categoría por defecto
        db.session.flush()
        account = Account(user_id=user.id, name="Efectivo")
        cat_expense = Category(user_id=user.id, name="General", type="expense")
        cat_income = Category(user_id=user.id, name="Sueldo", type="income")
        db.session.add_all([account, cat_expense, cat_income])
        db.session.commit()

        flash("Cuenta creada. ¡Podés iniciar sesión!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("transactions.index"))

    if request.method == "POST":
        try:
            data = login_schema.load(request.form)
        except ValidationError as err:
            flash("Datos inválidos.", "danger")
            return render_template("auth/login.html")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            flash("Email o contraseña incorrectos.", "danger")
            return render_template("auth/login.html")

        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("transactions.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))
