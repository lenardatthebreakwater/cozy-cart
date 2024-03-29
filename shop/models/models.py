from flask_login import UserMixin
from shop import db

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True, nullable=False)
	cost = db.Column(db.Float, nullable=False)
	stock = db.Column(db.Integer, nullable=False)
	description = db.Column(db.Text, nullable=False)
	img_filename = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f'<Product: {self.name}>'


class Admin(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)

	def __repr__(self):
		return f'<Admin: {self.name}>'
