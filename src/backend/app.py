from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask import make_response
import logging
import semver


import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'secret123'
    app.config['JWT_SECRET_KEY'] = 'secret1234'

    CORS(
        app,
        resources={r"*": {"origins": ["*", "http://localhost:5173/"]}},
        allow_headers=["Authorization", "Content-Type"],
        methods=["GET", "POST", "OPTIONS"],
        supports_credentials=True,
        max_age=86400
    )

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # def check_version():
    #     version = request.header.get('app-version', '0.0.0')
    #     if semver.compare(version, '1.2.0')<0:
    #         return jsonify({'message' : 'Please update your client application.'}), 426
    #     return None
    
    @app.route('/')
    def index():
        # version_check = check_version()
        # if version_check:
        #     return version_check
        return jsonify({'status': 200})

    @app.route('/register', methods=['POST'])
    def register():
        # version_check = check_version()
        # if version_check:
        #     return version_check
        try:
            data = request.get_json()
            hashed_password = bcrypt.generate_password_hash(
                data['password']).decode('utf-8')
            new_user = User(username=data['username'], password=hashed_password, motto = data.get('motto', ''))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 500


    @app.route('/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            user = User.query.filter_by(username=data['username']).first()
            if user and bcrypt.check_password_hash(user.password, data['password']):
                access_token = create_access_token(identity={'username': user.username})
                #return jsonify({'token': access_token}), 200 //here we are sending JSON format of cookie
                response = make_response(jsonify({'message': 'Login Successful'}), 200)
                response.set_cookie('token', access_token, httponly= True, secure=False)
                logging.debug(f"Set cookie token: {access_token}")
                return response
            return jsonify({'message': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'message': str(e)})

    @app.route('/user', methods=['GET'])
    @jwt_required()
    def user():
        current_user = get_jwt_identity()
        # return user information
        user = User.query.filter_by(username = current_user['username']).first()
        print(user)
        return jsonify({'username': user.username, 'motto': user.motto})

    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # for recording, I need to create a new field for motto in the db
    motto = db.Column(db.String(250), nullable = True)


if __name__ == '__main__':
    app = create_app()
    app.run(port=3002, debug=True)
