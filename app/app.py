from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///occasional_sync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5555, debug=True)