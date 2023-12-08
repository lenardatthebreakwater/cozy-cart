from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from shop.forms import RegisterForm, LoginForm
from shop.models import User
from shop import db, bcrypt

user = Blueprint("user", __name__)

@user.get("/register")
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for("home.root"))
    form = RegisterForm()
    return render_template("register.html", form=form)

@user.post("/register")
def register_post():
    if current_user.is_authenticated:
        return redirect(url_for("home.root"))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        country = form.country.data
        city = form.city.data
        contact = form.contact.data
        address = form.address.data
        zipcode = form.zipcode.data
        new_user = User(username=username, email=email, password=hashed_password, country=country, city=city, contact=contact, address=address, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been successfully created", "success")
        return redirect(url_for("home.root"))
    else:
        flash("Failed to create account, please try again", "danger")
        return redirect(url_for("user.register_get"))

@user.get("/login")
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for("home.root"))
    form = LoginForm()
    return render_template("login.html", form=form)

@user.post("/login")
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("home.root"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password.encode("utf-8"), form.password.data):
            login_user(user)
            flash(f"You have successfully logged in as {user.username}", "success")
            return redirect(url_for("home.root"))
        else:
            flash("Login was unsuccessful, please check your email or password", "danger")
            return redirect(url_for("user.login_get"))

@user.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "danger")
    return redirect(url_for("home.root"))
