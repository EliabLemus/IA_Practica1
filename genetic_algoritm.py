import random, functools, operator, math
data_rows=[]
# individuals_population=[]
max_generations = 500 

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

    
def buildPopulation(file_rows=[],population=20):
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
def check_criteria(generation,criteria=0):
    """
        population: individuals with solution propossals 
        generation: number of generation working 
        criteria: Type of criteria to evaluate
    """
    print('generation: ', generation, max_generations)
    if criteria == 0:
        return generation > max_generations
    else:
        return False
    
def chooseFathers(population):
    """
    will be selected the best of two
    """
    #TODO: Mejorar la seleccion 
    # ut.sort(key=lambda x: x.count, reverse=True)
    population.sort(key=lambda x: x.fitnessValue, reverse=False)
    parents =[]
    limit=int(len(population)/2)
    print('limit:', limit)
    for i in range(0,limit):
        parentA = population[i]
        parentB = population[i+1]
        parents.append(parentB if parentB.fitnessValue < parentA.fitnessValue else parentA)
        i+=2
    return parents
    
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
def execute(file_rows=[],population=20):
    data_rows = file_rows
    population = buildPopulation(file_rows=data_rows)
    generation = 0
    stop = check_criteria(generation,0)
    print('stop:',stop)
    print('Generacion:', generation)
    while(stop != True):
        print('inside while')
        print('Generacion:', generation)
        #seleccionar padres
        parents = chooseFathers(population=population)
        population = match(parents) 
        generation += 1
        stop = check_criteria(generation,0)
        print('Generacion:', generation)
        print('stop', stop)
        for p in population:
            printObject(p)
        
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