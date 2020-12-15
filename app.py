# app.py
import csv
import codecs 
from io import StringIO
from genetic_algoritm import calculatedNote, execute, printObject,getBestSolution,log

data_rows = []
individuos = []
finalization_criteria = {'max_generation': False,'best_value': False,'criteria_3': False}
parents_choose = {'tournament': False,'best_value': False,'pairs': False}
results = {}
save_solution=[]
# also importing the request module
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.debug = True
app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    

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
        if request.form.get('Modelo') == 'Modelo' or request.form.get('Subir') == 'Subir':
            print('generate+model')
            if request.files['loadFile'].filename == '':
                print('no file')
                return render_template('form.html',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose,results=results)
                        # Request radio buttons
            finalization_criteria_value=request.form['finalization_criteria']
            parents_choose_value=request.form['choose_parents']
            
            
            parents_choose[parents_choose_value] = True
            
            finalization_criteria[finalization_criteria_value] = True
            # print('father choose:', father_choose)
            
            f = request.files['loadFile']
            print('f:',f)    
            fstring = StringIO(f.read().decode())
            reader = csv.DictReader(fstring, delimiter=',')
            file_up =''
            # Numero de filas
            list_of_dicts = list(reader)
            print('parents_choose_value',parents_choose_value)
            print('finalization_criteria_value',finalization_criteria_value)
            
            options = {'parents_option': parents_choose_value, 'finalization_criteria_option': finalization_criteria_value}
            results = {}
            results = execute(list_of_dicts,options=options)
            

            return render_template('form.html', finalization_criteria=finalization_criteria,parents_choose=parents_choose, results=results)

        elif request.form.get('Nota') == 'Nota':
            #Projects score
            
            p1=request.form.get('proyecto1')
            p2=request.form.get('proyecto2')
            p3=request.form.get('proyecto3')
            p4=request.form.get('proyecto4')
            model=request.form.get('hmodel_selected')
            fitness=request.form.get('hfitness_value')
            
                
            if model == None:
                model=getBestSolution()
            else:
                new_model = model.strip("[").strip("]").split(",")
                print('model:',new_model)
                print('hmodel_selected:',new_model)
                model=[float(i) for i in new_model]
            
            result_score = calculatedNote(model,[float(p1),float(p2),float(p3),float(p4)])
            results = {'calculated_note': result_score,'fitness_value': fitness, 'model_selected': model,
                       'proyecto1': p1, 'proyecto2': p2, 'proyecto3': p3, 'proyecto4': p4}
            
            log('Nota Calculada: ', results)
            return render_template('form.html', fileName = ' ',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose,results=results)
        else:
            print(request.form)
            print('else')
            results = {}
            return render_template('form.html', fileName = ' ',file_content = 'hola',finalization_criteria=finalization_criteria,parents_choose=parents_choose,results=results)
        
    
    

        

