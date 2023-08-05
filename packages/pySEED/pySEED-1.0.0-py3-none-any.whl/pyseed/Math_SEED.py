from pyseed.Math_EDA import Math_EDA
from joblib import Parallel, delayed
import multiprocessing
import math
import numpy as np
import threading
import concurrent.futures

class Math_SEED(Math_EDA):
    def __init__(self,ndim):
        self.Mu = []
        self.Nu = []
        for i in range(ndim):
            self.Mu.append(0)
            self.Nu.append(0)

    def Sample(self,Pop,gen,elit):
        npop = len(Pop)
        sample = Pop
        sample = Pop[0:int(npop*elit)]
        return sample

    def Z_Thread(self,Sample,beta):
        dom=[]
        for i in range(0,len(Sample)):
            dom.append(self.Sigma_gx(Sample[i].getFitness(),beta))
        return dom
    def Sigma_gx(self,gx,beta):
        return math.exp(beta*gx)

    def CalMu_Nu(self,dom,j,Sample,beta):
        a = min(dom)
        b = max(dom)
        Z = float(len(Sample))/((b-a)*sum(dom))
        sum1 = 0.0
        sum2 = 0.0
        f1 = lambda x,gx, beta, z: (math.exp(beta*gx)/(z*beta))*x+gx*x
        f2 = lambda gx, beta, a, b: 1/(beta*(b-a))+gx
        f3 = lambda x,gx, beta, z, mu: (math.exp(beta*gx)/(z*beta))*math.pow(x-mu,2)+gx*math.pow(x-mu,2)
        f4 = lambda gx: gx
        for i in range(0,len(Sample)):
           sum1+=f1(Sample[i].getVector()[j],Sample[i].getFitness(), beta, Z)
           sum2+=f2(Sample[i].getFitness(), beta, a, b)
        mu = sum1/sum2
        sum1 = 0.0
        sum2 = 0.0
        for i in range(0,len(Sample)):
            sum1+=f3(Sample[i].getVector()[j],Sample[i].getFitness(), beta, Z,self.Mu[j])
            sum2+=f4(Sample[i].getFitness())
        nu = sum1/sum2
        return (mu,nu)

    def dummy(self,bete,dom,Sample):
        for j in range(0,Sample[0].nArray()):
            self.CalMu_Nu(dom,j,Sample,beta)

    def Mu_and_Nu(self,Sample,optimus):
        beta = 1/optimus
        num_cores = multiprocessing.cpu_count()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.Z_Thread, Sample,beta)
            dom = future.result()
        result = Parallel(n_jobs=num_cores)(delayed(self.CalMu_Nu)(dom,j,Sample,beta) for j in range(0,Sample[0].nArray()))
        for k in range(0,len(result)):
            self.Mu[k] = result[k][0]
            self.Nu[k] = result[k][1]
        return self.Mu, self.Nu

    def gaussianSample(self,Mu,Nu,newpob):
        for i in range(0,len(Mu)):
            for j in range(0,len(newpob)):
                s = np.random.normal(Mu[i],math.sqrt(Nu[i]))
                newpob[j].setValue(i,s)
