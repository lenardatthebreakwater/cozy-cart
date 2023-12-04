from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SECRET_KEY"] = "cake"
db = SQLAlchemy(app)

from shop.blueprints import home
app.register_blueprint(home)

from shop.blueprints import customer
app.register_blueprint(customer)
