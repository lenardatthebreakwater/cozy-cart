from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "itsasecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "admin_blueprint.admin_login"

from shop.models import Admin
@login_manager.user_loader
def load_user(admin_id):
    admin = Admin.query.filter_by(id=admin_id).first()
    return admin

from shop.routes import product_blueprint
app.register_blueprint(product_blueprint)

from shop.routes import admin_blueprint
app.register_blueprint(admin_blueprint)

from shop.routes import cart_blueprint
app.register_blueprint(cart_blueprint)
