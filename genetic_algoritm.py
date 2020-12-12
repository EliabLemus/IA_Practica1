import random, functools, operator, math

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

def fitnessValue(N=0,data_rows=[]):
    """
    N= Number of rows 
    data_rows= rows in file
    """        
    pre_sum=0
    for k in data_rows:
        pre_sum+=(k.rn - k.cn) ** 2
    result = pre_sum/N
    return result

def executeAlgoritm():
    