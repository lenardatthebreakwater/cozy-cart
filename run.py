from shop import app
from waitress import serve
from paste.translogger import TransLogger

if __name__ == "__main__":
	serve(TransLogger(app))
