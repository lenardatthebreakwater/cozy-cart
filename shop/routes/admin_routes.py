import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from shop.forms import AddProductForm, AdminRegisterForm, AdminLoginForm
from shop.models import Product, Admin
from shop import app, db, bcrypt

admin_blueprint = Blueprint("admin_blueprint", __name__)

@admin_blueprint.get("/admin/dashboard")
@login_required
def admin_dashboard():
  return render_template("admin_dashboard.html")

@admin_blueprint.route("/admin/register", methods=["GET", "POST"])
def admin_register():
  if current_user.is_authenticated:
    return redirect(url_for("admin_blueprint.admin_dashboard"))
  admins = Admin.query.all()
  if admins:
    return redirect(url_for("admin_blueprint.admin_login"))
  form = AdminRegisterForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
    new_admin = Admin(name=form.name.data, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    flash(f'Admin Account successfully created for {form.name.data}', 'success')
    return redirect(url_for("admin_blueprint.admin_login"))
  return render_template("admin_register.html", form=form)

@admin_blueprint.route("/admin/login", methods=["GET", "POST"])
def admin_login():
  if current_user.is_authenticated:
    return redirect(url_for("admin_blueprint.admin_dashboard"))
  form = AdminLoginForm()
  if form.validate_on_submit():
    admin = Admin.query.filter_by(name=form.name.data).first()
    if admin and bcrypt.check_password_hash(admin.password.encode("utf-8"), form.password.data):
      login_user(admin)
      flash(f"You are now logged in as {admin.name}", "success")
      return redirect(url_for("admin_blueprint.admin_dashboard"))
    else:
      flash("Login unsuccessful, please check username or password", "danger")
      return redirect(url_for('admin_blueprint.login'))
  return render_template("admin_login.html", form=form) 

@admin_blueprint.route("/admin/addproduct", methods=["GET", "POST"])
@login_required
def admin_addproduct():
  form = AddProductForm()
  if form.validate_on_submit():
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form.image_file.data.filename)
    new_img_filename = random_hex + file_extension
    img_path = os.path.join(app.root_path, "static/product_images", new_img_filename)
    img = Image.open(form.image_file.data)
    img.thumbnail((350, 300))
    img.save(img_path)
    new_product = Product(
      name=form.name.data,
      cost=form.cost.data,
      stock=form.stock.data,
      description=form.description.data,
      img_filename=new_img_filename
    )
    db.session.add(new_product)
    db.session.commit()
    flash("Product successfully added")
    return redirect(url_for("admin_blueprint.admin_dashboard"))
  return render_template("admin_addproduct.html", form=form)