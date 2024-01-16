from flask import Blueprint, render_template

cart_blueprint = Blueprint("cart_blueprint", __name__)

@cart_blueprint.get("/")
def cart():
    return render_template("cart.html")