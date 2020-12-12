import random, functools, operator, math

# Return an array of random values between low and high boundaries
def getSolutions(low, high, size):
    return [random.uniform(low, high) for _ in range(size)]

# Return an array of arrays with random values 
def getPopulation(solutions, size):
    return [getSolutions(-2,2,solutions) for i in range(size)]

# population = getPopulation(4,25)
# for a in population:
#     print('Member: {}'.format(a))

def printObject(o):
    tmp = vars(o)
    for item in tmp:
        print(item, ':', tmp[item])
        
class Node:
    def __init__(self, solution = [], fitnessValue = 0, realNote = 0, projectNotes = []):
        self.solution = solution
        self.fitnessValue = fitnessValue
        self.calculatedNote = calculatedNote(solution, projectNotes)
        self.realNote = realNote
        self.projectNotes = projectNotes 

#Model: 
#𝑁𝐶 = 𝑤 𝑃 + 𝑤 𝑃 + 𝑤 𝑃 + 𝑤 𝑃
#NC -> Nota calculada 
#p[1-4] -> Nota proyecto 
#w[1-4] -> Constantes

solution = [0.45,0.2,0.34,0.15] # this will be generated 
# [0]P1 - [1]P2 - [2]P3 - [3]P4 [4]NotaFinal
entrance=[[55,65,71,61,63.7],[94,20,54,29,44.9],[10,31,16,6,13.35]]

project_score = [[75,50,90,65], [80,95,88,80],[20,55,60,58],[60,28,69,50]]
real_notes = [71.75,84.65,52.45,53.9]

#Take both lists based on the model and operates as 𝑤1 𝑃1 + 𝑤2 𝑃2 + 𝑤3 𝑃3 + 𝑤4 𝑃4

def calculatedNote(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))

def fitnessValue(row_count=0,realNote = [], calculatedNote = []):
    substract = [x1 - x2 for (x1, x2) in zip(realNote,calculatedNote)]
    pow_array = []
    for s in substract:
        pow_array.append(s ** 2)
    
    # print(pow_array)    
    result = 0
    print('n: {}'.format(row_count))
    sum_pow_array = sum(pow_array)
    print('sum_pow_array:'.format(sum_pow_array))
    result = 1/row_count * sum(pow_array)
    print(result)
    if result != 0:
        print('Valor fitness: {}'.format(result))
    else:
        print('Valor fitness no se pudo calcular')
    # return 1/n * (realNote - calculateNote )
    

#foreach solution 
# - build new node 
# - build notes 