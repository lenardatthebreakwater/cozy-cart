from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from shop.models import Product, Admin

class AdminRegisterForm(FlaskForm):
	name = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Register")

	def validate_name(self, name):
		admin = Admin.query.filter_by(name=name.data).first()
		if admin:
			raise ValidationError("Username is already taken")


class AdminLoginForm(FlaskForm):
	name = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	submit = SubmitField("Login")


class AdminAddProductForm(FlaskForm):
	name = StringField("Product Name", validators=[DataRequired(), Length(min=1)])
	cost = FloatField("Cost", validators=[DataRequired()])
	stock = IntegerField("Stock", validators=[DataRequired()])
	description = TextAreaField("Description", validators=[DataRequired(), Length(min=1)])
	image_file = FileField("Product Image", validators=[DataRequired(), FileAllowed(["png", "jpg", "jpeg"])])
	submit = SubmitField("Add Product")

	"""
	-The name of this function should contain validate + _ + the exact 
	name of the form attribute you want to validate
	"""
	def validate_name(self, name):
		product = Product.query.filter_by(name=name.data).first()
		if product:
			raise ValidationError("You already have a product with the same name")


class AdminUpdateProductForm(FlaskForm):
	name = StringField("Product Name", validators=[DataRequired(), Length(min=1)])
	cost = FloatField("Cost", validators=[DataRequired()])
	stock = IntegerField("Stock", validators=[DataRequired()])
	description = TextAreaField("Description", validators=[DataRequired(), Length(min=1)])
	image_file = FileField("New Product Image", validators=[FileAllowed(["png", "jpg", "jpeg"])])
	submit = SubmitField("Update Product")

class AddToCartForm(FlaskForm):
  quantity = IntegerField("Quantity", validators=[DataRequired()])
  submit = SubmitField("Add to Cart")
