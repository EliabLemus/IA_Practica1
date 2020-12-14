# app.py
import csv
import codecs 
from io import StringIO
from genetic_algoritm import execute, printObject
data_rows = []
individuos = []
finalization_criteria = {'max_generation': False,'best_value': False,'criteria_3': False}
parents_choose = {'tournament': False,'best_value': False,'random': False}
results = {'model_selected': ''}
# also importing the request module
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.debug = True

# # home route
@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('form.html',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose,results=results)

# serving form web page
@app.route("/my-form", methods = ['GET', 'POST'])
def form():
    if request.method == 'GET':
           return render_template('form.html', fileName = ' ',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose)
       
    if request.method == 'POST':
        if request.form.get('Generar modelo') == 'generate_model':
                        # Request radio buttons
            finalization_criteria_value=request.form['finalization_criteria']
            parents_choose_value=request.form['choose_parents']
            
            
            parents_choose[parents_choose_value] = True
            finalization_criteria[finalization_criteria_value] = True

            # print('father choose:', father_choose)
            f = request.files['loadFile']    
            fstring = StringIO(f.read().decode())
            reader = csv.DictReader(fstring, delimiter=',')
            file_up =''
            # Numero de filas
            list_of_dicts = list(reader)
            print('parents_choose_value',parents_choose_value)
            print('finalization_criteria_value',finalization_criteria_value)
            
            options = {'parents_option': parents_choose_value, 'finalization_criteria_option': finalization_criteria_value}
            
            results = execute(list_of_dicts,options=options)
            

            return render_template('form.html', finalization_criteria=finalization_criteria,parents_choose=parents_choose, results=results)

        elif request.form.get('Nota') == 'Nota':
            #Projects score 
            p1=request.form.get('proyecto1')
            p2=request.form.get('proyecto2')
            p3=request.form.get('proyecto3')
            p4=request.form.get('proyecto4')
            print('p1,p2,p3,p4',p1,p2,p3,p4)
            return render_template('form.html', fileName = ' ',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose)
        else:
            print(request.form)
            print('else')
            return render_template('form.html', fileName = ' ',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose)
        
    
    

        

