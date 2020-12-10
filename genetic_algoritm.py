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
    def __init__(self, solution = [], fitnessValue = 0, calculatedNote = 0, realNote = 0):
        self.solution = solution
        self.fitnessValue = fitnessValue
        self.calculatedNote = calculatedNote
        self.realNote = realNote

#Model: 
#𝑁𝐶 = 𝑤 𝑃 + 𝑤 𝑃 + 𝑤 𝑃 + 𝑤 𝑃
#NC -> Nota calculada 
#p[1-4] -> Nota proyecto 
#w[1-4] -> Constantes

solution = [0.45,0.2,0.34,0.15]
project_score = [[75,50,90,65], [80,95,88,80],[20,55,60,58],[60,28,69,50]]
real_notes = [71.75,84.65,52.45,53.9]

#Take both lists based on the model and operates as 𝑤1 𝑃1 + 𝑤2 𝑃2 + 𝑤3 𝑃3 + 𝑤4 𝑃4

def calculatedNote(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))
nodes = []
index = 0
for k in project_score:
    calc_note=calculatedNote(solution, k)
    nodes.append(Node(solution=solution,calculatedNote=calc_note,realNote=real_notes[index]))
    index+=1

n=len(nodes)
cuad_error = 0
for i in nodes:
    cuad_error += math.pow((i.realNote - i.calculatedNote),2)
    i.fitnessValue = 1/n * (cuad_error)
    
for o in nodes:
    print('- - -')
    printObject(o)

