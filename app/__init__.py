from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config  # Asumiendo que config.py está junto a __init__.py

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos dentro del contexto de la app
    with app.app_context():
        from . import models  # models.py está en la misma carpeta que __init__.py

    # Registrar blueprints
    # Opción 1: Import relativo si 'app' es una subcarpeta de 'peticiones'
    from .routes import bp
    app.register_blueprint(bp)

    # Si en lugar de eso tuvieras un paquete "peticiones.app" y quisieras importar con el nombre completo:
    # from peticiones.app.routes import bp
    # app.register_blueprint(bp)

    return app