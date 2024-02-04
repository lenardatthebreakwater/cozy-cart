from flask import Blueprint, render_template, session, redirect, abort
from shop.utils import paymongo_request
from shop.forms import CheckoutForm
from shop.models import PendingOrder
from shop import fernet

cart_blueprint = Blueprint("cart_blueprint", __name__)

@cart_blueprint.route("/cart", methods=["GET", "POST"])
def cart():
  form = CheckoutForm()
  if form.validate_on_submit():
    """
    encrypted_firstname = fernet.encrypt(form.firstname.data.encode()).decode()
    encrypted_lastname = fernet.encrypt(form.lastname.data.encode()).decode()
    encrypted_email = fernet.encrypt(form.email.data.encode()).decode()
    encrypted_phone = fernet.encrypt(form.phone.data.encode()).decode()
    customer_address = f"{form.line1.data}, {form.city.data}, {form.state.data}, {form.country.data}"
    encrypted_address = fernet.encrypt(customer_address.encode()).decode()
    encrypted_postal_code = fernet.encrypt(form.postal_code.data.encode()).decode()
    """
    """
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
    """
    try:
      line_items = []
      for cart_item in session["cart"]:
        line_items.append({
          "amount": int(cart_item["cost"] * 100),
          "currency": "PHP",
          "name": cart_item["name"],
          "quantity": cart_item["quantity"]
        })
    
      paymongo_checkout_id, paymongo_checkout_url = paymongo_request(
        line1=form.line1.data,
        city=form.city.data,
        state=form.state.data,
        postal_code=form.postal_code.data,
        country=form.country.data,
        name=f"{form.firstname.data} {form.lastname.data}",
        email=form.email.data,
        phone=form.phone.data,
        line_items=line_items,
      )

      return redirect(paymongo_checkout_url)
    except Exception as e:
      abort(500)
  
  return render_template("cart.html", title="Cart", form=form)


@cart_blueprint.post("/cart/checkout/success")
def checkout_success():
  session.clear()
  #Expire the paymongo checkout session object using the paymongo checkout session id stored in the session
  return render_template("checkout_success.html")