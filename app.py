# app.py

# also importing the request module
from flask import Flask, render_template, request

app = Flask(__name__)
# home route
@app.route("/")
def hello():
    return render_template('index.html', name = 'Jane', gender = 'Female')

# serving form web page
@app.route("/my-form")
def form():
    return render_template('form.html')

# handling form data
@app.route('/form-handler', methods=['POST'])
def handle_data():
    welcome_msg = 'Hello '
    name = request.form['name']
    
    if request.form['gender'] == 'Male':
        welcome_msg += 'Mr. ' + name
    elif request.form['gender'] == 'Female':
        welcome_msg += 'Mrs. ' + name

    return welcome_msg

    # # since we sent the data using POST, we'll use request.form
    # print('Name: ', request.form['name'])
    # # we can also request.values
    # print('Gender: ', request.form['gender'])
    # return "Request received successfully!"
# app.run(debug = True) 