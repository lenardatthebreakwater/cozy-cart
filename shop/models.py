from . import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Customer: <{username}>"
