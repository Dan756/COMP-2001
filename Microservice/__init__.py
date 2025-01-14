import os
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://DTaylor:HgdL295+@DIST-6-505.uopnet.plymouth.ac.uk/COMP2001_DTaylor?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.engine.connect()
        print(app.url_map)
        print("Succesfully connected to the database")
    except Exception as e:
        print("Error connecting to the database:", e)


import tables
import procedures

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
