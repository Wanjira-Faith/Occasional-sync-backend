from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///occasional_sync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False