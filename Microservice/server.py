from flask import Flask, request, jsonify, session
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from __init__ import app
from auth import authenticate_token, required_role, SECRET_KEY
from datetime import timedelta
from flask_session import Session
import jwt
import requests
import procedures
import tables

CORS(app)

api = Api(
    app,
    version='1.0',
    title='Trail Microservice by Dan Taylor',
    description='An API that facilitates the functionality of the trail application by enabling the management of users, trails, and features.',
    doc='/swagger',
    security='BearerAuth'
)

api.authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}

app.config['SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['APP_SECRET_KEY'] = SECRET_KEY  
Session(app)

AUTHENTICATION_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

users_ns = api.namespace('users', description='Operations related to users')
trails_ns = api.namespace('trails', description='Operations related to trails')
trail_features_ns = api.namespace('trailFeature', description='Operations related to features')
trail_feature_mapping_ns = api.namespace('trailFeatureMapping', description='Operations related to trail features')
auth_ns = api.namespace('authentication', description='Operations related to user authentication')

users_model = api.model('Users', {
    'user_id': fields.String(required=True, description='The user\'s ID'),
    'name': fields.String(required=True, description='The user\'s full name'),
    'email': fields.String(required=True, description='The email address of the user'),
    'password': fields.String(required=True, description='The user\'s account password'),
    'role': fields.String(required=True, description='The user\'s assigned role within the system'),
})

trails_model = api.model('Trails', {
    'trail_id': fields.String(required=True, description='The trail\'s ID'),
    'trail_name': fields.String(required=True, description='The trail\'s name'),
    'trail_summary': fields.String(required=True, description='A brief summary of the trail'),
    'trail_description': fields.String(required=True, description='Detailed description of the trail'),
    'difficulty': fields.String(required=True, description='The difficulty level of the trail'),
    'location': fields.String(required=True, description='Geographical location of the trail'),
    'length': fields.Float(required=True, description='The trail\'s total length in kilometers'),
    'elevation_gain': fields.Float(required=True, description='Elevation gain along the trail in meters'),
    'route_id': fields.String(required=True, description='Identifier for the trail route'),
    'creation_date': fields.Integer(required=True, description='Timestamp of when the trail was created'),
})

trail_feature_model = api.model('TrailFeature', {
    'trail_feature_id': fields.String(required=True, description='Unique identifier for the feature'),
    'feature_name': fields.String(required=True, description='Name of the feature'),
})

trail_feature_model = api.model('TrailFeatureMapping', {
    'trail_feature_mapping_id': fields.String(required=True, description='Unique identifier for the trail feature mapping'),
    'trail_id': fields.String(required=True, description='Unique identifier for the trail'),
    'feature_id': fields.String(required=True, description='Unique identifier for the feature'),
    
})

route_model = api.model('Route', {
    'route_id': fields.String(required=True, description='Unique identifier for the route'),
    'route_type': fields.String(required=True, description='The type of route'),
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User\'s email address'),
    'password': fields.String(required=True, description='User\'s account password'),
})

@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.doc('user_login')
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate the user using the Auth API and return a token for further API access."""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Both email and password are required'}, 400

        try:
            # Send authentication request to the Auth API
            response = requests.post(
                AUTHENTICATION_API_URL,
                json={"email": email, "password": password},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                try:
                    auth_response = response.json()
                    if isinstance(auth_response, list) and len(auth_response) >= 2 and auth_response[0] == "Verified":
                        verified_status = auth_response[1]

                        # Store user credentials and role in the session
                        session['email'] = email
                        session['role'] = 'Admin' if verified_status == "True" else 'User'

                        return {
                            "message": "Login successful",
                            "verified": verified_status == "True",
                            "role": session['role']
                        }, 200

                    else:
                        return {"message": "Unexpected format in API response", "response_content": auth_response}, 500

                except ValueError:
                    return {"message": "Failed to parse JSON response from Auth API"}, 500

            else:
                return {
                    "message": f"Authentication failed with status code {response.status_code}",
                    "response_text": response.text
                }, response.status_code

        except requests.RequestException as e:
            return {"message": f"Error while connecting to Auth API: {str(e)}"}, 500


@users_ns.route('')
class Users(Resource):
    @users_ns.expect(users_model)
    @users_ns.doc('add_user')
    def post(self):
        return procedures.add_user()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)