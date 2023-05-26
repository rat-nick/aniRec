from flask import Flask
from flask_cors import CORS

from .data import DataAccessLayer

app = Flask(__name__)
cors = CORS(app)
dal = DataAccessLayer()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
