from controllers.PoissonDistribution import PoissonDistribution
import time
from random import randrange, choice, choices
from controllers.ElevatorHandler import ElevatorHandler

class Passenger(PoissonDistribution):

    __limit = 0 
    __currentTime = 1
    __maxFloor = 0
    __maxPassenger = 0
    __currentFloor = 0
    __lam = []
    __defaultLam = False
    __eachFloor = dict()
    __arrivalRate = 0 
    __totDown, __totUp = dict(), dict()
    __elevatorHandler = None

    def __init__(self, 
                 currentFloor: int,
                 maxFloor: int,
                 passenger: int,
                 limit: int = 12,
                 lam: list = []
                 ):
        if len(lam) < limit - 1: 
            self.__lam.append(randrange(85, 101))
            self.__defaultLam = True
        else:
            self.__lam = lam
        l = self.__lam[0] * passenger // 100
        super().__init__(l, passenger)
        self.__limit = limit
        self.__currentFloor = currentFloor
        self.__maxFloor = maxFloor
        self.__maxPassenger = passenger
        self.__eachFloor.update({i : 0 for i in range(1, maxFloor + 1)})
        self.__eachFloor[currentFloor] = self.__maxPassenger
        self.__elevatorHandler = ElevatorHandler.getInstance()
    
    def setTime(self, time: int):
        self.__currentTime = time
        return self
    
    def getTime(self):
        return self.__currentTime 
    
    def show(self):
        print("# At Time : {}".format(self.__currentTime))
        for i in range(1, self.__maxFloor + 1):
            print("> floor : {} , nPassenger : {}".format(i, self.__eachFloor[i]))
        return print("=" * 20)
    
    def genArrival(self):
        newLam = 0
        newK = 0

        if self.__currentTime == 1:
            # Open the building
            self.__arrivalRate = self.genSample().getMostFreq()
            if self.__arrivalRate > self.__maxPassenger:
                self.__arrivalRate = self.__maxPassenger 
            return self
        elif self.__currentTime == self.__limit - 1:
            # Close the building
            for i in range(1, self.__maxFloor + 1):
                self.__arrivalRate = self.__maxPassenger
            return self
        else: 
            # Working time
            if self.__defaultLam:
                # if user does not give a set of lamda, we'll auto generate it with 1 - 70% of floor population
                percentage = randrange(1, 71)
                self.__lam.append(percentage)
                newLam = percentage * self.__maxPassenger // 100
                newK = self.__maxPassenger
                self.setK(newK).setLam(newLam)
                self.__arrivalRate = self.genSample().getMostFreq()
                if self.__arrivalRate > self.__maxPassenger: self.__arrivalRate = self.__maxPassenger
            else:
                # if user give a set of lamda
                newLam = self.__lam[self.__currentTime] * self.__maxPassenger // 100
                newK = self.__maxPassenger
                self.setK(newK).setLam(newLam)
                self.__arrivalRate = self.genSample().getMostFreq()
                if self.__arrivalRate > self.__maxPassenger: self.__arrivalRate = self.__maxPassenger
        
        return self
    
    def transfer(self):
        self.clearEachFloor()
        # No one in the floor
        if self.__maxPassenger == 0: return self
        # No arrival rate 
        if self.__arrivalRate == 0: return self
        elif self.__currentTime == self.__limit - 1:
            # Close the building, force to go to first floor
            self.__eachFloor[1] += self.__maxPassenger
            self.__eachFloor[self.__currentFloor] -= self.__maxPassenger
            self.__maxPassenger = 0
        else:
            # Working time
            # every floor except curent floor
            floorChoice = list( set({i for i in range(1, self.__maxFloor + 1)}) - set([self.__currentFloor]) )
            weight = dict({i : 100//len(floorChoice) for i in floorChoice})
            while self.__arrivalRate > 0:
                #trans = randrange(1, self.__eachFloorArrival[i] + 1)
                if self.__maxPassenger == 0 : break
                trans = 1 
                floor = choices(floorChoice, list(weight.values()))[0]
                weight[floor] -= 10 * (100//len(floorChoice)) // 100 # Every random will reduce a prob if that floor by 10%
                self.__eachFloor[floor] += trans
                self.__eachFloor[self.__currentFloor] -= trans
                self.__maxPassenger -= trans
                self.__arrivalRate -= trans
        return self
    
    def sendToQueue(self):
        queue = dict()
        for key in self.__eachFloor.keys():
            if key == self.__currentFloor: continue
            queue.update({key: self.__eachFloor[key]})
        self.__elevatorHandler.enqueue(self.__currentFloor, queue)
        return self.__elevatorHandler.getQueue()

    def clearEachFloor(self):
        for i in range(1, len(self.__eachFloor) + 1):
            if i == self.__currentFloor: continue
            self.__eachFloor[i] = 0
    
#     def run(self):
#         while self.__currentTime < self.__limit:
#             self.genArrival().transfer().show()
#             self.__currentTime += 1
#             #self.__elevatorHandler.enqueue(self.__currentFloor, trans)
#             time.sleep(0.3)
    
#     def getEachFloor(self):
#         return self.__eachFloor
    

# if __name__ == "__main__":
#     e = ElevatorHandler.getInstance()
#     e.setMaxFloor(6)
#     p = Passenger(3, 6, 30, 6, [90, 30, 60, 20, 80])
#     print(p.getEachFloor())
#     print("\n")
#     print(p.genArrival().transfer().sendToQueue())
#     print("\n")
#     print(p.getEachFloor())
#     print("\n\n")
#     print(p.genArrival().transfer().sendToQueue())
#     print("\n")
#     print(p.getEachFloor())
    #p.run()
    #p.setTime(1...n)
    #p.genArrival().transfer()