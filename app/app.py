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

# Define a request parser for event creation
event_parser = reqparse.RequestParser()
event_parser.add_argument('name', type=str, required=True, help='Event Name is required')
event_parser.add_argument('date', type=str, required=True, help='Event Date is required')
event_parser.add_argument('location', type=str, required=True, help='Event Location is required')
event_parser.add_argument('description', type=str, default='', help='Event Description')
event_parser.add_argument('capacity', type=int, required=True, help='Event Capacity is required (minimum 1)')
event_parser.add_argument('poster', type=str, default='', help='Event Poster URL')

class EventListResource(Resource):
    @jwt_required()
    def get(self):
        events = Event.query.all()
        event_list = []

        for event in events:
            event_info = {
                'event_id': event.event_id,
                'name': event.name,
                'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
                'location': event.location,
                'description': event.description,
                'capacity': event.capacity,
                'poster':event.poster
            }
            event_list.append(event_info)

            return jsonify({'events': event_list})
        
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity() 

        args = event_parser.parse_args()

        # Convert the date string to a datetime object
        date_str = args['date']
        date_format = '%Y-%m-%d %H:%M:%S'
        event_date = datetime.strptime(date_str, date_format)

        event = Event(
            organizer_id=current_user_id,
            name=args['name'],
            date=event_date,  
            location=args['location'],
            description=args['description'],
            capacity=args['capacity'],
            poster=args['poster']  
        )
        db.session.add(event)
        db.session.commit()
        return {'message': 'Event created successfully'}, 201

api.add_resource(EventListResource, '/events')

# Define a request parser for searching events by ID
reqparse.RequestParser().add_argument('event_id', type=int, required=True)

class EventSearchResource(Resource):
    def get(self, event_id):
        event = Event.query.get_(event_id)
        if event is None:
            return {'message': 'Event not found'}, 404

        event_info = {
            'event_id': event.event_id,
            'name': event.name,
            'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
            'location': event.location,
            'description': event.description,
            'capacity': event.capacity,
            'poster': event.poster
        }

        return jsonify({'event': event_info})

api.add_resource(EventSearchResource, '/search-events/<int:event_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)