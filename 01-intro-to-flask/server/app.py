#!/usr/bin/env python3

import os

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from models import db, Pet, Owner, User


# Initialize the App
app = Flask(__name__)
    
# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')

# Initialize database
db.init_app(app)

# Initialize migration
migrate = Migrate()
migrate.init_app(app, db)

excluded_endpoints = ['login', 'signup', 'check_session', 'root']

@app.before_request
def check_logged_in():
    if request.endpoint not in excluded_endpoints:
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()

        if not user:
            # invalid cookie
            return {'message': 'invalid session'}, 401

# Routes
@app.route('/')
def root():
    # make_resonse needs json data and status code
    return make_response(jsonify({}), 200)
    # return make_response('<h1>HELLO</h1>', 200)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(username=data['username'])
    new_user.password_hash = data['password']
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'user added'}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # check if user exists
    user = User.query.filter(User.username == data['username']).first()

    if not user:
        return {'message': 'user not found'}, 404
    
    if user.authenticate(data['password']):
        # passwords matched, add cookie
        session['user_id'] = user.id
        return {'message': 'login success'}, 201
    else:
        # password did not match, send error resp
        return {'message': 'login failed'}, 401

@app.route('/check_session')
def check_session():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    if not user:
        # invalid cookie
        return {'message': 'invalid session'}, 401
    
    # valid cookie
    return {'message': 'valid session'}, 200

@app.route('/logout', methods=['DELETE'])
def logout():
    # delete cookie
    session.pop('user_id')
    return {'message': 'logged out'}, 200

# methods tells us what http verbs we accept
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return make_response(jsonify({"hello": "world"}), 200)

@app.route('/pets', methods=['GET', 'POST'])
def get_all_pets():
    if request.method == 'GET':
        pets = Pet.query.all()
        body = [pet.to_dict() for pet in pets]
        return make_response(jsonify(body), 200)
    else:  # POST
        # pet_data will be a dict
        pet_data = request.get_json()

        # validate
        if 'name' not in pet_data:
            return {'message': 'name is required'}, 403

        new_pet = Pet(
            name=pet_data.get('name'), 
            owner_id=pet_data.get('owner_id')
        )
        # add to db
        db.session.add(new_pet)
        db.session.commit()

        return new_pet.to_dict(), 201

# can add url pattern matching with <>
# data gets passed into view function as a parameter
@app.route('/pets/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def pets_by_id(id):
    # query the db for a pet with this id
    pet = Pet.query.filter(Pet.id == id).first()

    # check if the pet exists
    if pet is None:
        return {'message': 'pet not found'}, 404

    if request.method == 'GET':
        # send json data to client
        # can use custom serialize rules by passing in "rules"
        return make_response(jsonify(pet.to_dict(rules=('-owner',))), 200)
    elif request.method == 'DELETE':
        # remove from db
        db.session.delete(pet)
        db.session.commit()

        return {}, 200
    
    elif request.method == 'PATCH':
        pet_data = request.get_json()

        # option 1: check each field to see if it is in the request body
        # if 'name' in pet_data:
        #     pet.name = pet_data['name']
        # if 'owner_id' in pet_data:
        #     pet.owner_id = pet_data['owner_id']

        # option 2:
        for field in pet_data:
            # pet.field = pet_data[field]  # <- does not work
            setattr(pet, field, pet_data[field])
        
        # add back to db
        db.session.add(pet)
        db.session.commit()
        
        return pet.to_dict(), 200

@app.route('/owners/<int:id>', methods=['GET', 'DELETE'])
def onwer_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if request.method == 'GET':
        return make_response(jsonify(owner.to_dict()), 200)
    elif request.method == 'DELETE':
        db.session.delete(owner)
        db.session.commit()
        return {}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
