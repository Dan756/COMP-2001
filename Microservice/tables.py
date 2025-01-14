from __init__ import db
from __init__ import app

class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Trails(db.Model):
    __tablename__ = 'Trails'
    __table_args__ = {'schema': 'CW2'}

    trail_id = db.Column(db.Integer, primary_key=True)
    trail_name = db.Column(db.String(100), nullable=False)
    trail_summary = db.Column(db.String(100))
    trail_description = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))
    location = db.Column(db.String(100))
    length = db.Column(db.Float)
    elevation_gain = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    route_id = db.Column(db.Integer, db.ForeignKey('Routes.route_id'))

class TrailFeature(db.Model):
    __tablename__ = 'TrailFeatures'
    __table_args__ = {'schema': 'CW2'}

    trail_feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(100), nullable=False)

class TrailFeatureMapping(db.Model):
    __tablename__ = 'TrailFeatureMapping'
    __table_args__ = {'schema': 'CW2'}

    trail_feature_mapping_id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer , db.ForeignKey('Trail.trail_id'))
    feature_id = db.Column(db.Integer, db.ForeignKey('TrailFeatures.trail_feature_id'))

class Routes(db.Model):
    __tablename__ = 'Routes'
    __table_args__ = {'schema': 'CW2'}

    route_id = db.Column(db.Integer, primary_key=True)
    route_type = db.Column(db.String(50))


with app.app_context():
    print("Tables Registered with SQLALCHEMY:")
    print(db.metadata.tables.keys())