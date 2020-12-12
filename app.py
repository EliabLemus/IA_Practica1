# app.py
import csv
import codecs 
from io import StringIO
from genetic_algoritm import Solution, Row, calculatedNote, fitnessValue, getPopulation, getSolutions, printObject
data_rows = []
individuos = []
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
        list_of_dicts = list(reader)
        row_count = len(list_of_dicts)
        ## End of csv read 
        ## load rows into data_rows
        for r in list_of_dicts:
            data_rows.append(Row(cn=0,rn=float(r.get('NOTA FINAL')),project_notes=[float(r.get('PROYECTO 1')), float(r.get('PROYECTO 2')), float(r.get('PROYECTO 3')), float(r.get('PROYECTO 4'))]))
            
        #Number of solutions generated 
        
        individuos = getPopulation(4,50)
        for s in individuos:
            print('-_-_-_-_-_--_-- working on: {} -_-_-_-_-_--_--'.format(s.solution_proposed))
            for d in data_rows:
                d.cn=calculatedNote(s.solution_proposed,d.project_notes)
            # for result in data_rows:
            #     printObject(result)
            s.fitnessValue=fitnessValue(row_count,data_rows=data_rows)    
        
        for n in individuos:
            printObject(n)    
        return render_template('form.html')
    
    

        

