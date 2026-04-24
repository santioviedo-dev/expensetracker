from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from marshmallow import ValidationError
from sqlalchemy import func
from datetime import date
from app.extensions import db
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.schemas import transaction_schema, transactions_schema

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions_bp.route("/")
@login_required
def index():
    # Filtros opcionales por query params
    type_filter = request.args.get("type")
    account_filter = request.args.get("account_id")

    query = Transaction.query.filter_by(user_id=current_user.id)

    if type_filter in ("income", "expense"):
        query = query.filter_by(type=type_filter)
    if account_filter:
        query = query.filter_by(account_id=account_filter)

    transactions = query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()

    # Totales del mes actual
    today = date.today()
    monthly = db.session.query(
    Transaction.type,
    func.sum(Transaction.amount).label("total")).filter(
    Transaction.user_id == current_user.id,
    func.extract("month", Transaction.date) == today.month,
    func.extract("year", Transaction.date) == today.year,).group_by(Transaction.type).all()

    totals = {"income": 0, "expense": 0}
    for row in monthly:
        totals[row.type] = float(row.total or 0)
    totals["balance"] = totals["income"] - totals["expense"]

    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "transactions/index.html",
        transactions=transactions,
        totals=totals,
        accounts=accounts,
        type_filter=type_filter,
        account_filter=account_filter,
    )


@transactions_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        try:
            transaction_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("transactions/form.html", transaction=None, accounts=accounts, categories=categories)

        transaction = Transaction(
            user_id=current_user.id,
            account_id=request.form["account_id"],
            category_id=request.form["category_id"],
            amount=request.form["amount"],
            type=request.form["type"],
            description=request.form.get("description", ""),
            date=date.fromisoformat(request.form["date"]),
        )
        db.session.add(transaction)
        db.session.commit()
        flash("Transacción registrada.", "success")
        return redirect(url_for("transactions.index"))

    return render_template("transactions/form.html", transaction=None, accounts=accounts, categories=categories)


@transactions_bp.route("/<string:transaction_id>/edit", methods=["GET", "POST"])
@login_required
def edit(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first_or_404()
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        try:
            transaction_schema.load(request.form)
        except ValidationError as err:
            for field, messages in err.messages.items():
                flash(f"{field}: {', '.join(messages)}", "danger")
            return render_template("transactions/form.html", transaction=transaction, accounts=accounts, categories=categories)

        transaction.account_id = request.form["account_id"]
        transaction.category_id = request.form["category_id"]
        transaction.amount = request.form["amount"]
        transaction.type = request.form["type"]
        transaction.description = request.form.get("description", "")
        transaction.date = date.fromisoformat(request.form["date"])
        db.session.commit()
        flash("Transacción actualizada.", "success")
        return redirect(url_for("transactions.index"))

    return render_template("transactions/form.html", transaction=transaction, accounts=accounts, categories=categories)


@transactions_bp.route("/<string:transaction_id>/delete", methods=["POST"])
@login_required
def delete(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first_or_404()
    db.session.delete(transaction)
    db.session.commit()
    flash("Transacción eliminada.", "info")
    return redirect(url_for("transactions.index"))
