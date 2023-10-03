from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from models import db, User, Event, EventNotification

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'


app.config['WTF_CSRF_ENABLED'] = False

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///occasional_sync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)
api = Api(app)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])

class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        form = RegistrationForm(data=data)

        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if User.query.filter(User.username == username).first() is not None:
                return {'message': 'Username already exists'}, 400

            try:
                # Use email_validator to validate the email address
                validate_email(email)
            except EmailNotValidError as e:
                return {'message': 'Invalid email address'}, 400

            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=new_user.user_id)

            return {
                'message': "User registered successfully",
                'access_token': access_token
            }, 201
        else:
            return {'message': 'Validation errors', 'errors': form.errors}, 400

api.add_resource(UserRegistrationResource, '/register')

class UserLogInResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not password:
            return{'message':'username and password required'},400
        
        # Check email and password
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email and user_by_email.password == password:
            access_token = create_access_token(identity=user_by_email.user_id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401
        
api.add_resource(UserLogInResource,'/login')


if __name__ == '__main__':
    app.run(port=5555, debug=True)