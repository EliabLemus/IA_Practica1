# app.py
import csv
import codecs 
from io import StringIO
import genetic_algoritm
data = []
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
        individuos = genetic_algoritm.getPopulation(4,1)
        # individuos=[[0.45,0.2,0.34,0.15]]
        # print(individuos)
        for p in individuos:
            # print(p)
            for i in list_of_dicts:
                # file_up += ', '.join(row)
                data.append(genetic_algoritm.Node(solution=p,realNote=i.get('NOTA FINAL'), projectNotes=[float(i.get('PROYECTO 1')), float(i.get('PROYECTO 2')), float(i.get('PROYECTO 3')), float(i.get('PROYECTO 4'))]))    
            realNoteArr = []
            calcNoteArr = []
            for d in data:
                realNoteArr.append(float(d.realNote))
                calcNoteArr.append(float(d.calculatedNote))
            print('Numero de filas: {}'.format(row_count))
            genetic_algoritm.fitnessValue(row_count=row_count,realNote=realNoteArr,calculatedNote=calcNoteArr)
        return render_template('form.html')
    
    

        

