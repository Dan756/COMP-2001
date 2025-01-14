from flask import Flask, request, jsonify
from __init__ import db
from __init__ import app
from sqlalchemy import text
from auth import authenticate_token

@app.route('/users/add', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not all(key in data for key in ['user_id', 'name', 'email', 'password', 'role']):
            return jsonify({"message": "All user fields are required"}), 400

        query = text("""
            EXEC [CW2].[add_user] 
            @user_id = :user_id, @name = :name, @email = :email, @password = :password, @role = :role
        """)
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        query = text("EXEC [CW2].[Delete_user] @user_id = :user_id")
        db.session.execute(query, {'user_id': user_id})
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cant delete user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['PUT'])
@authenticate_token
def update_username(user_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC [CW2].[update_username] 
            @user_id = :user_id, @name = :name
        """)
        db.session.execute(query, {'user_id': user_id, 'name': data['name']})
        db.session.commit()
        return jsonify({"message": "User updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cant update user", "error": str(e)}), 500
