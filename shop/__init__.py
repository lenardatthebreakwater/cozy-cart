from flask import Flask
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
"""
app = Flask(__name__)
"""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SECRET_KEY"] = "cake"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "user.login_get"

from .models import User
@login_manager.user_loader
def load_user(user_id):
	user = User.query.filter_by(id=user_id).first()
	return user
"""
from shop.routes import home_blueprint
app.register_blueprint(home_blueprint)

from shop.routes import product_blueprint
app.register_blueprint(product_blueprint)
