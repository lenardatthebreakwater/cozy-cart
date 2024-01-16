from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from .models import Product

class AddProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(min=1, max=128)])
    stock = IntegerField("Stock", validators=[DataRequired()])
    cost = FloatField("Cost", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    image = FileField("Image", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("Add Product")

    def validate_username(self, name):
        if Product.query.filter_by(name=name.data).first():
            raise ValidationError("You already have a product with the same name")
