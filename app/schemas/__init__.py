from app.extensions import ma
from app.models.user import User
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from marshmallow import fields, validate, validates, ValidationError


# ── User ──────────────────────────────────────────────

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)

    email = fields.Email(required=True)


class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


# ── Account ───────────────────────────────────────────

class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        load_instance = True
        exclude = ("user_id",)

    name = fields.String(required=True, validate=validate.Length(min=1, max=255))


# ── Category ──────────────────────────────────────────

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        exclude = ("user_id",)

    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    type = fields.String(required=True, validate=validate.OneOf(["income", "expense"]))


# ── Transaction ───────────────────────────────────────

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True
        exclude = ("user_id",)

    amount = fields.Decimal(required=True, as_string=True, validate=validate.Range(min=0.01))
    type = fields.String(required=True, validate=validate.OneOf(["income", "expense"]))
    date = fields.Date(required=True)

    # Datos anidados para mostrar en las respuestas
    account = fields.Nested(AccountSchema, dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)


# Instancias listas para usar en las rutas
user_schema = UserSchema()
register_schema = RegisterSchema()
login_schema = LoginSchema()
account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
