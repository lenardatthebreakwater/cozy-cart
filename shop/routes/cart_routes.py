from flask import Blueprint, render_template, session, redirect
from shop.forms import CheckoutForm
from shop.models import PendingOrder
from dotenv import load_dotenv
from shop import fernet
import requests
import base64
import json
import os

load_dotenv()

cart_blueprint = Blueprint("cart_blueprint", __name__)

@cart_blueprint.get("/cart")
def cart():
  form = CheckoutForm()
  return render_template("cart.html", title="Cart", form=form)


@cart_blueprint.post("/cart/checkout")
def checkout():
  form = CheckoutForm()
  if form.validate_on_submit():
    encrypted_firstname = fernet.encrypt(form.firstname.data.encode()).decode()
    encrypted_lastname = fernet.encrypt(form.lastname.data.encode()).decode()
    encrypted_email = fernet.encrypt(form.email.data.encode()).decode()
    encrypted_phone = fernet.encrypt(form.phone.data.encode()).decode()
    customer_address = f"{form.line1.data}, {form.city.data}, {form.state.data}, {form.country.data}"
    encrypted_address = fernet.encrypt(customer_address.encode()).decode()
    encrypted_postal_code = fernet.encrypt(form.postal_code.data.encode()).decode()

    new_order = PendingOrder(
      firstname=encrypted_firstname,
      lastname=encrypted_lastname,
      email=encrypted_email,
      phone=encrypted_phone,
      address=encrypted_address,
      postal_code=encrypted_postal_code,
    )
    db.session.add(new_order)
    db.session.commit()

    line_items = []
    for cart_item in session["cart"]:
      line_items.append({
        "amount": int(cart_item["cost"] * 100),
        "currency": "PHP",
        "name": cart_item["name"],
        "quantity": cart_item["quantity"]
      })
    
    url = "https://api.paymongo.com/v1/checkout_sessions"

    payload = { "data": { "attributes":{
      "billing": {
        "address": {
          "line1": form.line1.data,
          "city": form.city.data,
          "state": form.state.data,
          "postal_code": form.postal_code.data,
          "country": form.country.data
        },
        "name": f"{form.firstname.data} {form.lastname.data}",
        "email": form.email.data,
        "phone": form.phone.data
      },
      "line_items": line_items,
      "payment_method_types": ["gcash"],
      "send_email_receipts": True,
      "show_line_items": True
    }}}

    paymongo_secret_key = os.getenv("PAYMONGO_SECRET_KEY")
    b64encoded_paymongo_secret_key = base64.b64encode(paymongo_secret_key.encode()).decode()
    headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Basic {b64encoded_paymongo_secret_key}"}
    response = requests.post(url, json=payload, headers=headers)
    response_dict = json.loads(response.text)

    encrypted_paymongo_checkout_session_id = fernet.encrypt(response_dict["data"]["id"].encode()).decode()
    if "checkout_session_id" not in session:
      session["checkout_session_id"] = encrypted_paymongo_checkout_session_id

    return redirect(response_dict["data"]["attributes"]["checkout_url"])

  else:
    abort(500)


@cart_blueprint.post("/cart/checkout/success")
def checkout_success():
  session["cart"].clear()
  #Expire the paymongo checkout session object using the paymongo checkout session id stored in the session
  return render_template("checkout_success.html")
