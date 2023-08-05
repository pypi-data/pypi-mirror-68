import numpy as np
class Element:
     def __init__(self,nvar):
        self.nvar = nvar
        self.array = np.zeros(nvar)
        self.fitness = 0.0
     
     def getValue(self,i):
        return self.array[i]

     def setValue(self,i,val):
        self.array[i] = val


     def setFitness(self,val):
        self.fitness = val

     def getFitness(self):
       return self.fitness

     def getVector(self):
       return self.array

     def nArray(self):
        return len(self.array)
     
     def __repr__(self):
        return repr((self.fitness))



