from flask import Blueprint, render_template, request
from shop.models import Product

home_blueprint = Blueprint("home_blueprint", __name__)

@home_blueprint.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.name).paginate(page=page, per_page=5)
    return render_template('home.html', products=products, page=page)
