import random
# Return an array of random values between low and high boundaries
def getSolutions(low, high, size):
    return [random.uniform(low, high) for _ in range(size)]

# Return an array of arrays with random values 
def getIndividuals(width, length):
    return [getSolutions(-2,2,width) for i in range(length)]
print(getIndividuals(4,25))