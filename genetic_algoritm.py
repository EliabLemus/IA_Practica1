import random, functools, operator, math, datetime
data_rows=[]
# individuals_population=[]
max_generations = 100 
global_population = 500
best_solution = [0.16394592305796651, 0.1371219182443406, 0.289936743604601, 0.40379898519615676]

class Solution:
    def __init__(self, solution_proposed = [], fitnessValue = 0):
        self.solution_proposed = solution_proposed
        self.fitnessValue = fitnessValue
         
class Row:
    def __init__(self,rn,cn,project_notes=[]):
        self.rn = rn
        self.cn = cn
        self.project_notes = project_notes
        
# Return an array of random values between low and high boundaries
def getSolutions(low, high, size):
    return [random.uniform(low, high) for _ in range(size)]

def getBestSolution():
    return best_solution
# Return an array of arrays with random values 
def getPopulation(numberOfSolutions, size):
    """
    numberOfSolutions: w1,w2,w3,w4...wn
    size: Size of population
    """
    population = []
    for i in range(0,size):
        population.append(Solution(getSolutions(-2,2,numberOfSolutions)))
    return population

def printObject(o):
    tmp = vars(o)
    for item in tmp:
        print(item, ':', tmp[item])
        

#Model: 
#𝑁𝐶 = 𝑤 𝑃 + 𝑤 𝑃 + 𝑤 𝑃 + 𝑤 𝑃
#NC -> Nota calculada 
#p[1-4] -> Nota proyecto 
#w[1-4] -> Constantes

#Take both lists based on the model and operates as 𝑤1 𝑃1 + 𝑤2 𝑃2 + 𝑤3 𝑃3 + 𝑤4 𝑃4

def calculatedNote(*lists):
    """
    calculatedNote(list_of_solutions,list_of_projec_notes)
    """
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))

def fitnessValue(N=0,data_rows=[],solution=[]):
    """
    N= Number of rows 
    data_rows= rows in file
    solution= propossed solution 
    
    """        
    for d in data_rows:
        d.cn=calculatedNote(solution,d.project_notes)
    pre_sum=0
    for k in data_rows:
        pre_sum+=((k.rn - k.cn) ** 2)
    result = pre_sum/N
    return result

    
def buildPopulation(file_rows=[],population=global_population):
    """
    file_rows: Data from csv file
    population: number of initial population to work 
    """
    data_rows.clear()
    row_count = len(file_rows)
    for r in file_rows:
        data_rows.append(Row(cn=0,rn=float(r.get('NOTA FINAL')),project_notes=[float(r.get('PROYECTO 1')), float(r.get('PROYECTO 2')), float(r.get('PROYECTO 3')), float(r.get('PROYECTO 4'))]))
    
    individuals_population=getPopulation(4,population)
    
    for s in individuals_population:
        s.fitnessValue=fitnessValue(row_count,data_rows=data_rows,solution=s.solution_proposed)    
    return individuals_population
def check_criteria(generation,criteria_option,population=[]):
    """
        population: individuals with solution propossals 
        generation: number of generation working 
        criteria: Type of criteria to evaluate
    """
    criteria = 0 
    if criteria_option == 'max_generation':
        criteria = 0
    elif criteria_option == 'best_value':
        criteria = 1
    elif criteria_option == 'criteria_3':
        criteria = 2
    else:
        criteria = 0
        
    log('Generacion: ', generation,'/', max_generations)
    if criteria == 0:
        #Maxima generacion
        return generation > max_generations
    elif criteria == 1: 
        # un miembro de la poblacion alcance un valor fitnes. 
        for i in population:
            if i.fitnessValue <= 2:
                return True
            else:
                return False
    elif criteria == 3:
        average = fitnessAverage(population)
        return average <=5
    return False
def fitnessAverage(population):
    results=[a.fitnessValue for a in population]
    return float(sum(results)/len(results)) 
        
def chooseFathers(population, choose_father_options):
    """
    will be selected the best of two
    """
    tipo = 0 
    if choose_father_options == 'tournament':
        tipo = 0 
    elif choose_father_options == 'best_value':
        tipo = 1
    elif choose_father_options == 'pairs':
        tipo = 2
    else:
        tipo = 0 
    
    log('Promedio valor fitness:', fitnessAverage(population))
    parents =[]
    population.sort(key=lambda x: x.fitnessValue, reverse=False)
    if tipo == 0: #tournament
        # population.sort(key=lambda x: x.fitnessValue, reverse=False)
        # Seleccion por torneo 
        log('seleccion de padres por torneo')
        population.sort(key=lambda x: x.fitnessValue, reverse=False)
        limit=int(len(population)/2)
        for i in range(0,limit):
            parentA = population[i]
            parentB = population[i+1]
            parents.append(parentB if parentB.fitnessValue < parentA.fitnessValue else parentA)
            i+=2
        return parents
    elif tipo == 1: #Best value 
        log('Seleccion de padres por mejor valor')
        #padres con el mejor valor fitness
        population.sort(key=lambda x: x.fitnessValue, reverse=False)
        limit=int(len(population)/2)
        for i in range(0,limit):
            parentA = population[i]
            parents.append(parentA)
        return parents
    elif tipo == 2: 
        log('Seleccion de padres por pares')
        for j in range(0,len(population)):
            if j%2 == 0:
                parentB = population[j]
                parents.append(parentB)
        
        return parents

def match(parents):
    """
    Emparejar
    """
    mid = int(len(parents)/2)
    sons=[]
    i=0
    while(i < mid):
        son1 = Solution()
        son1.solution_proposed = cross(parents[i].solution_proposed,parents[mid + i].solution_proposed)
        son1.solution_proposed = mutate(son1.solution_proposed)
        son1.fitnessValue = fitnessValue(len(data_rows),data_rows,son1.solution_proposed)
        
        son2 = Solution()
        son2.solution_proposed = cross(parents[mid + i].solution_proposed,parents[i].solution_proposed)
        son2.solution_proposed = mutate(son2.solution_proposed)
        son2.fitnessValue = fitnessValue(len(data_rows),data_rows,son2.solution_proposed)
        
        sons.append(son1)
        sons.append(son2)
        i+=1
    
    parents = sorted(parents, key=lambda item: item.fitnessValue, reverse=False)
    
    i=0
    new_population = []
    while(i < len(parents)):
        new_population.append(sons[i])
        new_population.append(parents[i])
        i += 1
        
    return new_population

def cross(parent1,parent2):
    """
    Cruzar
    """
    value1 = random.uniform(0,1)
    value2 = random.uniform(0,1)
    value3 = random.uniform(0,1)
    value4 = random.uniform(0,1)
    
    
    w1 = parent1[0] if value1 <= 0.6 else parent2[0]
    w2 = parent1[1] if value2 <= 0.6 else parent2[1]
    w3 = parent1[2] if value3 <= 0.6 else parent2[2]
    w4 = parent1[3] if value4 <= 0.6 else parent2[3]

    return [w1,w2,w3,w4]

def mutate(solution):
    prob = random.uniform(0,1)
    if prob < 0.5:
        for i in range(0,len(solution)):
            prob = random.uniform(0,1)
            if prob < 0.5:
                solution[i] = random.uniform(-2,2)
            break
    return solution    
def execute(file_rows=[],population=20,options=[]):
    log('Inicio ejecucion - Opciones elegidas:', options)
    data_rows = file_rows
    population = buildPopulation(file_rows=data_rows,population=global_population)
    generation = 0
    stop = check_criteria(generation,criteria_option=options['finalization_criteria_option'],population=population)
    while(stop != True):
        #seleccionar padres
        parents = chooseFathers(population=population,choose_father_options=options['parents_option'])
        population = match(parents) 
        generation += 1
        stop = check_criteria(generation,criteria_option=options['finalization_criteria_option'],population=population)
        log('Generacion:', generation)
    population.sort(key=lambda x: x.fitnessValue, reverse=False)
    log('Valor fitness:',population[0].fitnessValue,' - Modelo:',population[0].solution_proposed)
    return {'model_selected': population[0].solution_proposed, 'fitness_value': population[0].fitnessValue}
def log(*args):
    now = datetime.datetime.now()
    line = '[' + now.strftime('%Y-%m-%d %H:%M:%S') + '] '
    for l in args:
        line+=str(l) 
    print(line)
    line+= "\n"
    with open('algoritm.log', "a+") as log:
        log.write(line)
### Funcion de pruebas
def test_function():
    parents=[]
    parents.append(Solution([0.23077760369354827, -1.1911969230003634, 0.23802431752247877, -0.7998844934669207],fitnessValue=25231.223238253446))   
    parents.append(Solution([0.225615787, 0.75977342793832, -0.64633832856771, 0.482811083181911],fitnessValue=658.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=100.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=90.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=80.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=700.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=110.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=140.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=150.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=170.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=190.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=170.6897142146493)) 
    parents.append(Solution([0.05611795615787, 0.3175977342793832, -0.856771, 0.83181911],fitnessValue=108.6897142146493)) 
    
    # choose = chooseFathers(parents)
    # print('Parents choosed:')
    # for c in choose:
    #     printObject(c)
    # print('cross: ', cross(choose[0].solution_proposed,choose[1].solution_proposed))
    # ut.sort(key=lambda x: x.count, reverse=True)
    parents.sort(key=lambda x: x.fitnessValue, reverse=False)
    for c in parents:
        printObject(c)    
# test_function()