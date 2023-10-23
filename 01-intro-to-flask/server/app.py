#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, make_response, jsonify


# 3. ✅ Initialize the App
app = Flask(__name__)
  
    
    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` 
    

 # 4. ✅ Migrate 

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

# can add url pattern matching with <>
# data gets passed into view function as a parameter
@app.route('/books/<int:id>')
def book_by_id(id):
    return make_response(jsonify({"id": id}), 200)
   

# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route



# 9.✅ Update the route to find a `production` by its `title` and send it to our browser
    
   

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5000, debug=True)
