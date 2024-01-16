import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for
from shop.forms import AddProductForm
from shop.models import Product
from shop import app, db

product_blueprint = Blueprint("product_blueprint", __name__)

@product_blueprint.get("/product/1")
def product():
	return render_template("product.html")

@product_blueprint.get("/product/new")
def add_product_get():
	form = AddProductForm()
	return render_template("add_product.html", form=form)

def process_image(image_data):
	random_hex = secrets.token_hex(8)
	_, file_extension = os.path.splitext(image_data.filename)
	new_complete_filename = random_hex + file_extension
	file_path = os.path.join(app.root_path, 'static/product_images', new_complete_filename)
	img = Image.open(image_data)
	img.thumbnail((500, 500))
	img.save(file_path)
	return new_complete_filename

@product_blueprint.post("/product/new")
def add_product_post():
	form = AddProductForm()
	if form.validate_on_submit():
		name = form.name.data
		stock = form.stock.data
		cost = form.cost.data
		description = form.description.data
		image_filename = process_image(form.image.data)
		new_product = Product(name=name, stock=stock, cost=cost, description=description, image=image_filename)
		db.session.add(new_product)
		db.session.commit()
		flash("Product successfully added")
		return redirect(url_for("home_blueprint.home"))
	else:
		flash("There was a problem adding the product")
		return redirect(url_for("home_blueprint.home"))
