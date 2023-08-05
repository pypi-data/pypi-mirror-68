import abc
from abc import ABC

class Fitness(ABC):

     @abc.abstractmethod
     def Evaluate(self,x):
       pass

