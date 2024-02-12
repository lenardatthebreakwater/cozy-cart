from flask import Blueprint, render_template, session, redirect, abort
from shop.utils import create_paymongo_checkout_session
from shop.forms import CheckoutForm

cart_blueprint = Blueprint("cart_blueprint", __name__)

@cart_blueprint.route("/cart", methods=["GET", "POST"])
def cart():
  form = CheckoutForm()
  if form.validate_on_submit():
    try:
      line_items = []
      for cart_item in session["cart"]:
        line_items.append({
          "amount": int(cart_item["cost"] * 100),
          "currency": "PHP",
          "name": cart_item["name"],
          "quantity": cart_item["quantity"]
        })

      paymongo_checkout_id, paymongo_checkout_url = create_paymongo_checkout_session(
        line1=form.line1.data,
        city=form.city.data,
        state=form.state.data,
        postal_code=form.postal_code.data,
        country=form.country.data,
        name=f"{form.firstname.data} {form.lastname.data}",
        email=form.email.data,
        phone=form.phone.data,
        line_items=line_items
      )

      session.pop("cart")
      return redirect(paymongo_checkout_url)
    except Exception as e:
      print(e)
      abort(500)
  
  return render_template("cart.html", title="Cart", form=form)
