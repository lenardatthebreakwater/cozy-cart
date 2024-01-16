from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "cake"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
db = SQLAlchemy(app)

from shop.routes import home_blueprint
app.register_blueprint(home_blueprint)

from shop.routes import product_blueprint
app.register_blueprint(product_blueprint)
