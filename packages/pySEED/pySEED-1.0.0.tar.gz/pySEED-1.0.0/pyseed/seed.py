from pyseed.element import Element
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
from pyseed.Math_SEED import Math_SEED
import math


class Seed:
     def __init__(self,npop,nvar,xi,xs,ncall,err=None,optimus=None,elit=None):
         self.npop = npop
         self.nvar = nvar
         self.xi = xi
         self.xs = xs
         self.err = err
         self.optimus = optimus
         self.ncall = ncall
         self.Pob = []
         self.newpob = []
         self.call = 0
         self.elit = elit
         for i in range(0,self.npop):
           self.Pob.append(Element(self.nvar))
           self.newpob.append(Element(self.nvar))
         self.InitPob()


     def InitPob(self):
        for i in range(0,self.npop):
          for j in range(0,self.nvar):
            temp = self.xi+np.random.random_sample()*(self.xs-self.xi)
            self.Pob[i].setValue(j,temp)


     def processInput(self,population,fitness):
       val = fitness.Evaluate(population.getVector())
       population.setFitness(val)
       self.call+=1
       return population

     def run(self,fitness):
       objMath = Math_SEED(self.Pob[0].nArray())
       rgen = 0
       num_cores = multiprocessing.cpu_count()
       Pobcopy = Parallel(n_jobs=-1)(delayed(self.processInput)(self.Pob[i],fitness) for i in range(0,len(self.Pob)))
       for i in range(0,len(Pobcopy)):
          self.Pob[i].setFitness(Pobcopy[i].getFitness())
       self.Pob.sort(key=lambda objelement: objelement.fitness, reverse=True)
       print("Fitness0=",self.Pob[0].getFitness())
       while self.call <= self.ncall:
         sample = objMath.Sample(self.Pob,rgen,self.elit)
         Mu, Nu = objMath.Mu_and_Nu(sample,self.optimus)
         objMath.gaussianSample(Mu,Nu,self.newpob)
         Pobcopy = Parallel(n_jobs=-1)(delayed(self.processInput)(self.newpob[i],fitness) for i in range(0,len(self.Pob)))
         for i in range(0,len(Pobcopy)):
           self.newpob[i].setFitness(Pobcopy[i].getFitness())
         self.newpob.sort(key=lambda objelement: objelement.fitness, reverse=True)
         for i in range(0,len(self.Pob)):
           if(self.newpob[i].getFitness()>self.Pob[i].getFitness()):
             for j in range(0,self.Pob[0].nArray()):
               self.Pob[i].setValue(j,self.newpob[i].getValue(j))
               self.Pob[i].setFitness(self.newpob[i].getFitness())
         rgen+=1
         print("Fitness",rgen,"=",self.Pob[0].getFitness())
         if math.fabs(self.optimus-self.Pob[0].getFitness()) < self.err:
           break
       return self.Pob[0].getVector(), self.Pob[0].getFitness()
