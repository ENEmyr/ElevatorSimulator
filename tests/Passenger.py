from PoissonDistribution import PoissonDistribution
from random import randrange
from ElevatorHandler import ElevatorHandler

class Passenger(PoissonDistribution):

    __nPassenger = 0
    __floor = 0
    __intratenant = dict() 
    __elevatorInterface = None

    def __init__(self, nPassenger, floor, lam):
        super().__init__(lam, nPassenger)
        self.__nPassenger = nPassenger
        self.__floor = floor
        self.__elevatorInterface = ElevatorHandler.getInstance()
        for i in range(1, self.__elevatorInterface.getMaxFloor() + 1):
            self.__intratenant.update({i : 0})
    
    def getNPassenger(self):
        return self.__nPassenger
    
    def printIntratenant(self):
        print(self.__intratenant)
    
    def randomIntratenantMove(self):
        self.setK(self.__nPassenger)
        nTenentMove = self.genSample().getMostFreq()
        self.__nPassenger -= nTenentMove
        while(nTenentMove != 0):
            randFloor = randrange(1, self.__elevatorInterface.getMaxFloor() + 1)
            if randFloor == self.__floor:
                continue
            nMove = randrange(1, nTenentMove + 1)
            self.__intratenant[randFloor] += nMove
            nTenentMove -= nMove
        self.requestForService()

    def doMove(self):
        self.__intratenant[1] += self.__nPassenger
        self.__nPassenger = 0
        self.requestForService()

    def requestForService(self):
        self.__elevatorInterface.enqueue(self.__intratenant)


if __name__ == "__main__":
    p = Passenger(30, 3, 24)
    print(p.getNPassenger())
    p.printIntratenant()
    p.randomIntratenantMove()
    p.printIntratenant()
    print(p.getNPassenger())
    print(p.getMostFreq())