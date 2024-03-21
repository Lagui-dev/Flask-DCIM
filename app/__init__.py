from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main.main import main as main_bp
    app.register_blueprint(main_bp, url_prefix='/main')

    from app.rack.rack import rack as rack_bp
    app.register_blueprint(rack_bp, url_prefix='/rack')

    return app
