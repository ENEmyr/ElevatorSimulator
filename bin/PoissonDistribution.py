import numpy as np
import matplotlib.pyplot as plt

class PoissonDistribution:

    __lam = float(0)
    __k = int(0)
    __sampleData = None

    def __init__(self, lam, k):
        self.__lam = lam
        self.__k = k
        self.__sampleData = None
        return self
    
    def setLam(self, lam):
        self.__lam = lam
        return self
    
    def setK(self, k):
        self.__k = k
        return self
    
    def getLam(self):
        return self.__lam
    
    def getK(self):
        return self.__k

    def genSample(self):
        self.__sampleData = np.random.poisson(self.__lam, self.__k)
        return self 
    
    def getSample(self):
        return self.__sampleData
    
    def getMostFreq(self):
        count = np.bincount(self.__sampleData)
        return np.argmax(count)

    def showHistrogram(self):
        count, bins, ignored = plt.hist(self.__sampleData, self.__k, density=True)
        return plt.show()
