from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()
def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    
    login.init_app(app)
    login.login_view = 'login'
    db.init_app(app)
    
    
    
    migrate = Migrate(app, db)

    with app.app_context():
        from . import routes, models
        db.create_all()

        return app