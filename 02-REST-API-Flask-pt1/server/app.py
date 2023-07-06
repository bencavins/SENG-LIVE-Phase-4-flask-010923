#!/usr/bin/env python3

# 📚 Review With Students:
    # API Fundamentals
    # MVC Architecture and Patterns / Best Practices
    # RESTful Routing
    # Serialization
    # Postman

# Set Up:
    # In Terminal, `cd` into `server` and run the following:
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5000
        # flask db init
        # flask db revision --autogenerate -m 'Create tables' 
        # flask db upgrade 
        # python seed.py

# ReST

# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|



from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Production, CastMember

import os

app = Flask(__name__)
CORS(app)  # fix CORS errors
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Note: `app.json.compact = False` configures JSON responses to print on indented lines
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

# 4. ✅ Create a GET (All) Route
    # 4.1 Make a `get` method that takes `self` as a param.
    # 4.2 Create a `productions` array.
    # 4.3 Make a query for all productions. For each `production`, create a dictionary 
    # containing all attributes before appending to the `productions` array.
    # 4.4 Create a `response` variable and set it to: 
    #  #make_response(
    #       jsonify(productions),
    #       200
    #  )
    # 4.5 Return `response`.
    # 4.6 After building the route, run the server and test in the browser.
@app.get('/productions')
def get_all_productions():
    prods = Production.query.all()
    data = []
    for production in prods:
        data.append(production.to_dict())
    return make_response(
        jsonify(data),
        200
    )

@app.get('/productions/<int:id>')
def get_production_by_id(id):
    prod = Production.query.filter(
        Production.id == id
    ).first()

    if not prod:
        return {'status': "not found"}, 404

    # make_response() and jsonify() get called for us
    return prod.to_dict(), 200

@app.post('/productions')
def post_production():
    data = request.get_json()
    new_prod = Production(
        title=data.get('title'),
        genre=data.get('genre'),
        budget=data.get('budget'),
        image=data.get('image'),
        director=data.get('director'),
        description=data.get('description'),
        ongoing=data.get('ongoing'),
    )
    db.session.add(new_prod)
    db.session.commit()
    return make_response(
        jsonify(new_prod.to_dict()), 201
    )

# An example of a route that accepts more than one http verb
# @app.route('/test/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
# def test(id):
#     prod = Production.query.filter(
#         Production.id == id
#     )
#     if request.method == 'GET':
#         prod.one()
#     elif request.method == 'DELETE':
#         prod.delete()
#     elif request.method == 'PATCH':
#         prod.update()


@app.delete('/productions/<int:id>')
def delete_production_by_id(id):
    Production.query.filter(
        Production.id == id
    ).delete()
    db.session.commit()
    return make_response(
        jsonify({'status': 'success'}), 200
    )

@app.patch('/productions/<int:id>')
def patch_production_by_id(id):
    prod = Production.query.filter(
        Production.id == id
    ).first()
    data = request.get_json()

    for field in data:
        setattr(prod, field, data[field])
        # prod[field] = data[field]
    
    # alternative approach
    # if 'title' in data:
    #     prod.title = data['tile']
    # if 'genre' in data:
    #     prod.genre = data['genre']
    #     # etc...

    db.session.add(prod)
    db.session.commit()
    return make_response(
        jsonify(prod.to_dict()),
        200
    )


# 5. ✅ Serialization
    # This is great, but there's a cleaner way to do this! Serialization will allow us to easily add our 
    # associations as well.
    # Navigate to `models.py` for Steps 6 - 9.

# 10. ✅ Use our serializer to format our response to be cleaner
    # 10.1 Query all of the productions, convert them to a dictionary with `to_dict` before setting them to a list.
    # 10.2 Invoke `make_response`, pass it the production list along with a status of 200. Set `make_response` to a 
    # `response` variable.
    # 10.3 Return the `response` variable.
    # 10.4 After building the route, run the server and test your results in the browser.
 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
