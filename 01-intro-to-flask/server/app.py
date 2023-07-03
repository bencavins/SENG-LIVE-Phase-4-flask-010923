#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate # need for db migrations
from models import db, Production

# 3. ✅ Initialize the App
app = Flask(__name__)
    
    # Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


 # 4. ✅ Migrate 
migrate = Migrate(app, db)  # set up alembic
db.init_app(app)  # set up sqlalchemy

# 6. ✅ Routes
@app.route('/', methods=['GET'])
def root():
    # return some response
    return '<h1>Homepage</h1><a href="/hello">hello</a>'

@app.get('/hello')
def get_hello():
    my_dict = {
        'hello': 'world'
    }
    return make_response(
        jsonify(my_dict),
        200
    )

@app.post('/hello')
def post_hello():
    my_dict = {
        'post_hello': 'world'
    }
    return jsonify(my_dict), 201

@app.get('/productions')
def get_productions():
    # query db for productions
    prods = Production.query.all()

    # build data dictionary
    data = []
    for production in prods:
        data.append({
            'title': production.title
        })

    # send response with json data
    return make_response(
        jsonify(data),
        200
    )

# 8. ✅ Create a dynamic route
@app.get('/productions/<int:id>')
def get_production_by_id(id):
    prod = Production.query.filter(
        Production.id == id
    ).one()
    data = {'title': prod.title}
    return make_response(
        jsonify(data),
        200
    )


# 9.✅ Update the route to find a `production` by its `title` and send it to our browser
    
   

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5000, debug=True)
