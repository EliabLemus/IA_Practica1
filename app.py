# app.py
import csv
import codecs 

from io import StringIO

# also importing the request module
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.debug = True

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
        f = request.files['loadFile']    
        fstring = StringIO(f.read().decode())
        reader = csv.DictReader(fstring, delimiter=',')
        file_up =''
        # Numero de filas
        row_count = sum(1 for row in reader)

        print('Numero de filas: {}'.format(row_count))
        for row in reader:
            file_up += ', '.join(row)
        
        return render_template('form.html')
    

        

