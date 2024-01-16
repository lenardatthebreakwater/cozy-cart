from flask import Blueprint, render_template

product_blueprint = Blueprint("product_blueprint", __name__)

@product_blueprint.get("/product/1")
def product():
	return render_template("product.html")
