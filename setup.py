try:
	with open(".env", "w") as file:
		file.write(f"SECRET_KEY=<Your made-up secret key for the application>\nPAYMONGO_SECRET=<your paymongo secret key>\n")
	print(".env file successfully created!")
except Exception as e:
	print("There was a problem creating the .env file: {e}")

import os
try:
	os.mkdir("shop/static/product_images")
	print("shop/static/product_images folder successfully created!")
except FileExistsError as e:
	print("shop/static/product_images folder already exists")

from shop import app, db
try:
	with app.app_context():
		db.create_all()
		print("Database successfully created!")
except Exception as e:
	print(f"There was  problem creating the database: {e}")
