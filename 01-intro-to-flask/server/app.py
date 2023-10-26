#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Pet, Owner


# 3. ✅ Initialize the App
app = Flask(__name__)
    
# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

 # 4. ✅ Migrate 
migrate = Migrate()
migrate.init_app(app, db)
# flask-sqlalchemy = "2.5.1"

# Alembic commands:
# to create the db framework:
#  flask db init  (only needs to be run once)
# to create a revision:
#  flask db migrate -m 'add pets'
# to apply the changes:
#  flask db upgrade head

# 5. ✅ Navigate to `seed.rb`

# 6. ✅ Routes
@app.route('/')
def root():
    # make_resonse needs json data and status code
    return make_response(jsonify({}), 200)
    # return make_response('<h1>HELLO</h1>', 200)

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

@app.route('/owners/<int:id>')
def onwer_by_id(id):
    owner = Owner.query.filter(Owner.id == id).one()
    return make_response(jsonify(owner.to_dict()), 200)
   

# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route



# 9.✅ Update the route to find a `production` by its `title` and send it to our browser
    
   

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5000, debug=True)
