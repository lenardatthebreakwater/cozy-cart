from flask import Blueprint, render_template, session, redirect, url_for, abort, flash
from shop.models import Product
from shop.forms import AddToCartForm

product_blueprint = Blueprint("product_blueprint", __name__)

@product_blueprint.get("/")
def allproducts():
	products = Product.query.all()
	return render_template("home.html", products=products)

@product_blueprint.get("/product/<int:product_id>")
def product(product_id):
  product = Product.query.get_or_404(product_id)
  form = AddToCartForm()
  return render_template("product.html", product=product, form=form)

"""
Helper funcntion that checks if cart_item which is a dictionary
is inside of session['cart'] 
"""
def isItemInCartSess(cart_session, cart_item):
  for i in cart_session:
    if i["id"] == cart_item["id"]:
      return True
  return False

@product_blueprint.post("/product/<int:product_id>/addtocart")
def addtocart(product_id):
  product = Product.query.get_or_404(product_id)
  form = AddToCartForm()
  if form.validate_on_submit():
    cart = []
    cart_item = {
      "id": product.id,
      "name": product.name,
      "cost": product.cost,
      "quantity": form.quantity.data
    }
    if "cart" not in session:
      session["cart"] = cart
      session["cart"].append(cart_item)
    elif "cart" in session:
      if isItemInCartSess(session["cart"], cart_item) == False:
        session["cart"].append(cart_item)
      elif isItemInCartSess(session["cart"],cart_item) == True:
        for i in session["cart"]:
          if i["id"] == cart_item["id"]:
            i["quantity"] += cart_item["quantity"]
    flash("Item successfully added to Cart")
    return redirect(url_for("product_blueprint.product", product_id=product.id))
  else:
    abort(500)
