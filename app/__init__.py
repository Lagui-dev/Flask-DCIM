from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from config import Config

db = SQLAlchemy()
migrate = Migrate()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap = Bootstrap5(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main.routes import main as main_bp
    app.register_blueprint(main_bp, url_prefix='/main')

    from app.rack.routes import rack as rack_bp
    app.register_blueprint(rack_bp, url_prefix='/rack')

    from app.hardware.routes import hardware as hardware_bp
    app.register_blueprint(hardware_bp, url_prefix='/hardware')

    from app.interface.routes import interface as interface_bp
    app.register_blueprint(interface_bp, url_prefix='/interface')

    return app
