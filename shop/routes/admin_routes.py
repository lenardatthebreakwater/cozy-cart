import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from shop.forms import AdminRegisterForm, AdminLoginForm, AdminAddProductForm, AdminUpdateProductForm 
from shop.models import Product, Admin
from shop import app, db, bcrypt

admin_blueprint = Blueprint("admin_blueprint", __name__)

@admin_blueprint.get("/admin/dashboard")
@login_required
def admin_dashboard():
  products = Product.query.all()
  return render_template("admin_dashboard.html", title="Admin Dashboard", products=products)


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
  return render_template("admin_register.html", title="Admin Register", form=form)


@admin_blueprint.route("/admin/login", methods=["GET", "POST"])
def admin_login():
  if current_user.is_authenticated:
    return redirect(url_for("admin_blueprint.admin_dashboard"))
  admins = Admin.query.all()
  form = AdminLoginForm()
  if form.validate_on_submit():
    admin = Admin.query.filter_by(name=form.name.data).first()
    if admin and bcrypt.check_password_hash(admin.password.encode("utf-8"), form.password.data):
      login_user(admin)
      flash(f"You are now logged in as {admin.name}", "success")
      return redirect(url_for("admin_blueprint.admin_dashboard"))
    else:
      flash("Login unsuccessful, please check username or password", "danger")
      return redirect(url_for('admin_blueprint.admin_login'))
  return render_template("admin_login.html", title="Admin Login", form=form, admins=admins) 


@admin_blueprint.route("/admin/product/new", methods=["GET", "POST"])
@login_required
def admin_addproduct():
  form = AdminAddProductForm()
  if form.validate_on_submit():
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form.image_file.data.filename)
    new_img_filename = random_hex + file_extension
    img_path = os.path.join(app.root_path, "static/product_images", new_img_filename)
    img = Image.open(form.image_file.data)
    img.thumbnail((550, 500))
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
    flash("Product successfully added", "success")
    return redirect(url_for("admin_blueprint.admin_dashboard"))
  return render_template("admin_addproduct.html", title="Admin Add Product", form=form)


@admin_blueprint.route("/admin/product/<int:product_id>/update", methods=["GET", "POST"])
@login_required
def admin_updateproduct(product_id):
  product = Product.query.get_or_404(product_id)
  form = AdminUpdateProductForm()
  new_img_filename = None
  if form.validate_on_submit():
    product2 = Product.query.filter_by(name=form.name.data).first()
    if product2 and product2.name != product.name:
      flash("A product with the same name already exists", "danger")
      return redirect(url_for("admin_blueprint.admin_updateproduct", product_id=product.id))
    if form.image_file.data:
      current_img_path = os.path.join(app.root_path, "static/product_images", product.img_filename)
      if os.path.exists(current_img_path):
        os.remove(current_img_path)
      random_hex = secrets.token_hex(8)
      _, file_extension = os.path.splitext(form.image_file.data.filename)
      new_img_filename = random_hex + file_extension
      new_img_path = os.path.join(app.root_path, "static/product_images", new_img_filename)
      img = Image.open(form.image_file.data)
      img.thumbnail((550, 500))
      img.save(new_img_path)
    product.name = form.name.data
    product.cost = form.cost.data 
    product.stock = form.stock.data
    product.description = form.description.data
    if new_img_filename:
      product.img_filename = new_img_filename
    db.session.commit()
    flash("Product has been successfully updated", "success")
    return redirect(url_for("admin_blueprint.admin_dashboard"))
  form.name.data = product.name
  form.stock.data = product.stock
  form.cost.data = product.cost
  form.description.data = product.description
  return render_template('admin_updateproduct.html', title="Update Product", form=form, product=product)


@admin_blueprint.route("/admin/product/<int:product_id>/remove")
@login_required
def admin_removeproduct(product_id):
  product = Product.query.get_or_404(product_id)
  img_path = os.path.join(app.root_path, "static/product_images", product.img_filename)
  if os.path.exists(img_path):
    os.remove(img_path)
  db.session.delete(product)
  db.session.commit()
  flash("Product successfully removed", "danger")
  return redirect(url_for("admin_blueprint.admin_dashboard"))


@admin_blueprint.route("/admin/logout")
@login_required
def admin_logout():
  logout_user()
  flash('You have successfully logout', 'danger')
  return redirect(url_for('product_blueprint.allproducts'))
