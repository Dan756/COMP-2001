from flask import Flask, request, jsonify, session
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from __init__ import app
from auth import authenticate_token, required_role, SECRET_KEY
from datetime import timedelta
from flask_session import Session

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
app.config['SESSION_STORAGE'] = 'filesystem'
app.config['APP_SECRET_KEY'] = SECRET_KEY  
Session(app)

AUTHENTICATION_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

health_ns = api.namespace('Health', description='Server health check')

@health_ns.route('/ping')
class Ping(Resource):
    @api.doc(description="Check the status of the server")
    @api.response(200, "Request successful", example={"message": "pong"})
    def get(self):
        """Returns a pong response to verify the server is operational"""
        return {"message": "pong"}, 200

users_ns = api.namespace('users', description='Operations related to users')
trails_ns = api.namespace('trails', description='Operations related to trails')
feature_ns = api.namespace('feature', description='Operations related to features')
trail_feature_ns = api.namespace('trailFeature', description='Operations related to trail features')
authentication_ns = api.namespace('authentication', description='Operations related to user authentication')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)