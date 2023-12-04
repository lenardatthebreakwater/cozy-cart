from flask import Blueprint, render_template, redirect, url_for, flash
from shop.forms import RegisterForm
from shop.models import Customer
from shop import db

customer = Blueprint("customer", __name__)

@customer.get("/register")
def register_get():
    form = RegisterForm()
    return render_template("register.html", form=form)

@customer.post("/register")
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        country = form.country.data
        city = form.city.data
        contact = form.contact.data
        address = form.address.data
        zipcode = form.zipcode.data
        new_user = Customer(username=username, email=email, password=password, country=country, city=city, contact=contact, address=address, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been successfully created")
        return redirect(url_for("home.root"))
