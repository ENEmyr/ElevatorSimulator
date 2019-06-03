from controllers.PoissonDistribution import PoissonDistribution
import time
from random import randrange, choice, choices

class Passenger(PoissonDistribution):

    __limit = 0 
    __currentTime = 1
    __maxFloor = 0
    __maxPassenger = 0
    __lam = []
    __defaultLam = False
    __eachFloor = dict()
    __eachFloorArrival = dict()
    __totDown, __totUp = dict(), dict()

    def __init__(self, 
                 floor: int,
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
        self.__maxFloor = floor
        self.__maxPassenger = passenger
        self.__eachFloor[1] = self.__maxPassenger
        self.__eachFloor.update({i : 0 for i in range(2, floor + 1)})
        self.__eachFloorArrival = {i : 0 for i in range(1, floor + 1)}
        self.__totDown = {i : 0 for i in range(1, floor + 1)}
        self.__totUp = {i : 0 for i in range(1, floor + 1)}
    
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
            self.__eachFloorArrival[1] = self.genSample().getMostFreq()
            if self.__eachFloorArrival[1] > self.__maxPassenger:
                self.__eachFloorArrival[1] = self.__eachFloor[1]
            return self
        elif self.__currentTime == self.__limit - 1:
            # Close the building
            for i in range(1, self.__maxFloor + 1):
                self.__eachFloorArrival[i] = self.__eachFloor[i]
            return self
        else: 
            # Working time
            if self.__defaultLam:
                # if user does not give a set of lamda, we'll auto generate it with 1 - 70% of floor population
                percentage = randrange(1, 71)
                self.__lam.append(percentage)
                for i in range(1, self.__maxFloor + 1):
                    if self.__eachFloor[i] <= 0:
                        self.__eachFloorArrival[i] = 0
                        continue
                    newLam = percentage * self.__eachFloor[i] // 100
                    newK = self.__eachFloor[i]
                    self.setK(newK).setLam(newLam)
                    self.__eachFloorArrival[i] = self.genSample().getMostFreq()
                    if self.__eachFloorArrival[i] > self.__eachFloor[i]: self.__eachFloorArrival[i] = self.__eachFloor[i]
            else:
                # if user give a set of lamda
                for i in range(1, self.__maxFloor + 1): 
                    if self.__eachFloor[i] <= 0:
                        self.__eachFloorArrival[i] = 0
                        continue
                    newLam = self.__lam[self.__currentTime] * self.__eachFloor[i] // 100
                    newK = self.__eachFloor[i]
                    self.setK(newK).setLam(newLam)
                    self.__eachFloorArrival[i] = self.genSample().getMostFreq()
                    if self.__eachFloorArrival[i] > self.__eachFloor[i]: self.__eachFloorArrival[i] = self.__eachFloor[i]
        
        return self
    
    def transfer(self):
        # TODO add servToFloor queue to identify which floor that passenger want to go in, and edit line 22(relative)
        # TODO modify sourcecode that collect totUp & totDown(line 11, 25, 26, 27) to use a property and collect it by seperates a floor too
        for i in range(1, self.__maxFloor + 1):
            totUp, totDown = 0, 0 
            # No one in i floor 
            if self.__eachFloorArrival[i] == 0: continue
            elif self.__currentTime == self.__limit - 1:
                # Close the building, force to go to first floor
                trans = self.__eachFloorArrival[i]
                self.__eachFloor[1] += trans
                self.__eachFloor[i] -= trans
                self.__eachFloorArrival[i] -= trans
                totDown = trans
            else:
                # Working time
                # every floor except curent floor
                floorChoice = list( set({i for i in range(1, self.__maxFloor + 1)}) - set([i]) )
                weight = dict({i : 100//len(floorChoice) for i in floorChoice})
                while self.__eachFloorArrival[i] > 0:
                    #trans = randrange(1, self.__eachFloorArrival[i] + 1)
                    trans = 1 
                    floor = choices(floorChoice, list(weight.values()))[0]
                    weight[floor] -= 10 * (100//len(floorChoice)) // 100 # Every random will reduce a prob if that floor by 10%
                    self.__eachFloor[floor] += trans
                    self.__eachFloor[i] -= trans
                    self.__eachFloorArrival[i] -= trans
                    if floor > i : totUp += trans 
                    else: totDown += trans 
            print("Total Up: {}, Total Down: {}".format(totUp, totDown))
        return self
    
    def run(self):
        while self.__currentTime < self.__limit:
            self.genArrival().transfer().show()
            self.__currentTime += 1
            time.sleep(1)
    

if __name__ == "__main__":
    p = Passenger(6, 30, 6, [90, 30, 60, 20, 80])
    p.run()