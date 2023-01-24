from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from functools import wraps
import uuid # for public id

# for token generation
import jwt
from datetime import datetime, timedelta
from  werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SECRET_KEY'] = 'your secret key'

cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(80))

class URL(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    threshold = db.Column(db.Integer)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url_id = db.Column(db.Integer)
    result = db.Column(db.Integer)

# with app.app_context():
#     db.create_all()
#     db.session.commit()

# token_required is a decorator function that checks for the presence of a valid JWT in the request header
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            # print('****', token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # print('****', data)
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except Exception as e:
            print(e)
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


# sign-up route
@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form
  
    # gets name, email and password
    username = data.get('username')
    password = data.get('password')
  
    # checking for existing user
    user = User.query\
        .filter_by(username = username)\
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id = str(uuid.uuid4()),
            username = username,
            password = generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)

# login route
@app.route('/login', methods =['POST'])
def login():
    # creates a dictionary of the form data
    auth = request.form
  
    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm ="Login required !!"'})
    
    user = User.query\
        .filter_by(username = auth.get('username'))\
        .first()
    
    if check_password_hash(user.password, auth.get('password')):
        # print('****', user.public_id)
        token = jwt.encode({
            'public_id' : user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token' : token}), 201)
    
    # returns 403 if password is wrong
    return make_response('Could not verify', 403, {'WWW-Authenticate' : 'Wrong password !!"'})

@app.route('/api/user', methods =['GET'])
@token_required
def test(current_user):
    return jsonify({'message' : 'Hello, ' + current_user.username + ' !!'})

if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug = True)