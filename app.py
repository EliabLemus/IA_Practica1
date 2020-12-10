# app.py
import csv
import codecs 
from io import StringIO

# also importing the request module
from flask import Flask, render_template, request, jsonify
UPLOAD_FOLDER='/Users/macbookpro/Documents/IA/Laboratorio/Practica1/flask_app'
ALLOWED_EXTENSIONS= set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# # home route
@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('form.html', fileName = ' ')

# serving form web page
@app.route("/my-form", methods = ['GET', 'POST'])
def form():
    if request.method == 'GET':
           return render_template('form.html', fileName = ' ')
       
    if request.method == 'POST':
        print('post')
       # Create variable for uploaded file
        print('request.files', request.files)
        print('request.form', request.form)
        f = request.files['archivo']    
        fstring = StringIO(f.read().decode())
        reader = csv.reader(fstring, delimiter=',')
        file_up =''
        for row in reader:
            file_up += ', '.join(row)
            print(row)
        
        return render_template('form.html')
        
@app.route('/upload',methods = ['POST'])
def upload_route_summary():
    if request.method == 'POST':
    
        # Create variable for uploaded file
        f = request.files['archivo']  

        #store the file contents as a string
        fstring = f.read().decode()
        print(fstring)
        #create list of dictionaries keyed by header row
        # csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]

        #do something list of dictionaries
    return "success"


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