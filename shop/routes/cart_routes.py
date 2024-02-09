from flask import Blueprint, render_template, session, redirect, abort, url_for
from shop.utils import paymongo_request
from shop.forms import CheckoutForm
from shop.models import PendingOrder
from shop import fernet, db
import requests

cart_blueprint = Blueprint("cart_blueprint", __name__)

@cart_blueprint.route("/cart", methods=["GET", "POST"])
def cart():
  form = CheckoutForm()
  if form.validate_on_submit():
    try:
      encrypted_firstname = fernet.encrypt(form.firstname.data.encode()).decode()
      encrypted_lastname = fernet.encrypt(form.lastname.data.encode()).decode()
      encrypted_email = fernet.encrypt(form.email.data.encode()).decode()
      encrypted_phone = fernet.encrypt(form.phone.data.encode()).decode()
      customer_address = f"{form.line1.data}, {form.city.data}, {form.state.data}, {form.country.data}"
      encrypted_address = fernet.encrypt(customer_address.encode()).decode()
      encrypted_postal_code = fernet.encrypt(form.postal_code.data.encode()).decode()
    except Exception as e:
      print(e)
      abort(500)

    try:
      new_order = PendingOrder(
        firstname=encrypted_firstname,
        lastname=encrypted_lastname,
        email=encrypted_email,
        phone=encrypted_phone,
        address=encrypted_address,
        postal_code=encrypted_postal_code
      )
      db.session.add(new_order)
      db.session.commit()
    except Exception as e:
      print(e)
      abort(500)

    try:
      line_items = []
      for cart_item in session["cart"]:
        line_items.append({
          "amount": int(cart_item["cost"] * 100),
          "currency": "PHP",
          "name": cart_item["name"],
          "quantity": cart_item["quantity"]
        })
      
      success_url = url_for("cart_blueprint.checkout_success")

      paymongo_checkout_id, paymongo_checkout_url = paymongo_request(
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

      if "paymongo_checkout_id" not in session:
        session["paymongo_checkout_id"] = fernet.encrypt(paymongo_checkout_id.encode()).decode()

      return redirect(paymongo_checkout_url)
    except Exception as e:
      print(e)
      abort(500)
  
  return render_template("cart.html", title="Cart", form=form)


"""
@cart_blueprint.post("/cart/checkout/success")
def checkout_success():
  try:
    encrypted_paymongo_checkout_id = session["paymongo_checkout_id"]
    paymongo_checkout_id = fernet.decrypt(encrypted_paymongo_checkout_id)
    url = f"https://api.paymongo.com/v1/checkout_sessions/{paymongo_checkout_id}/expire"
    headers = {"accept": "application/json"}
    response = requests.post(url, headers=headers)
    print(response.text)
    session.clear()
    return "<h1>You have successfully checked out</h1>"
  except Exception as e:
    print(e)
    abort(500)
"""