from flask import Flask, redirect, url_for
from config import config
from app.extensions import db, migrate, login_manager, ma


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ma.init_app(app)

    # Configurar Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Tenés que iniciar sesión para acceder."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(user_id)

    # Importar modelos para que Migrate los detecte
    from app.models import User, Account, Category, Transaction  # noqa

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.accounts import accounts_bp
    from app.routes.categories import categories_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(transactions_bp)

    # Ruta raíz
    @app.route("/")
    def index():
        return redirect(url_for("transactions.index"))

    return app
