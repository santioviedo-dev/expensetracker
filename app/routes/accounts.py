from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from marshmallow import ValidationError
from app.extensions import db
from app.models.account import Account
from app.schemas import account_schema, accounts_schema

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_bp.route("/")
@login_required
def index():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template("accounts/index.html", accounts=accounts)


@accounts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        try:
            data = account_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("accounts/form.html", account=None)

        account = Account(user_id=current_user.id, name=request.form["name"])
        db.session.add(account)
        db.session.commit()
        flash("Cuenta creada.", "success")
        return redirect(url_for("accounts.index"))

    return render_template("accounts/form.html", account=None)


@accounts_bp.route("/<string:account_id>/edit", methods=["GET", "POST"])
@login_required
def edit(account_id):
    account = Account.query.filter_by(id=account_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        try:
            account_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("accounts/form.html", account=account)

        account.name = request.form["name"]
        db.session.commit()
        flash("Cuenta actualizada.", "success")
        return redirect(url_for("accounts.index"))

    return render_template("accounts/form.html", account=account)


@accounts_bp.route("/<string:account_id>/delete", methods=["POST"])
@login_required
def delete(account_id):
    account = Account.query.filter_by(id=account_id, user_id=current_user.id).first_or_404()
    db.session.delete(account)
    db.session.commit()
    flash("Cuenta eliminada.", "info")
    return redirect(url_for("accounts.index"))
