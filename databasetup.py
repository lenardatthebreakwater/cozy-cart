from shop import app, db

try:
	with app.app_context():
		db.create_all()
		print("Database successfully created!")
except Exception as e:
	print(f"There was  problem creating the database: {e}")
