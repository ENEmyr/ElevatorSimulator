import time
from controllers.ElevatorHandler import ElevatorHandler

class Elevator:
    
    #property
    __maxFloor = 30
    __currFloor = 1
    __maxCapacity = 10
    __currCapacity = 0
    __isUp = True
    __Id = 0
    __type = 0 #Low floor or High floor, 1==High floor
    __speed = 1
    __dinningFloor = 0
    __meanFloor = 15
    __servTo = dict()
    __defaultFloor = 1
    __elevatorHandler = ElevatorHandler.getInstance()

    def __init__(self, ID, maxCapacity, maxFloor, type, dinningFloor = 0):
        self._Elevator__Id = ID
        self._Elevator__maxCapacity = maxCapacity
        self._Elevator__type = type
        self._Elevator__maxFloor = maxFloor
        self._Elevator__dinningFloor = dinningFloor
        self._Elevator__meanFloor = maxFloor//2
        self._Elevator__servTo.update( {i : 0 for i in range(1, maxFloor + 1)} )
        maxFloor = self.__elevatorHandler.getMaxFloor()
        
    # Setter
    def setSpeed(self, speed):
        self._Elevator__speed = speed
        return self
    
    def setDefaultFloor(self, floor):
        self._Elevator__defaultFloor = floor
        return self

    # Getter
    def getCurrFloor(self):
        return self._Elevator__currFloor
    
    def getMaxFloor(self):
        return self._Elevator__maxFloor
    
    def getCurrCapacity(self):
        return self._Elevator__currCapacity

    def getMaxCapacity(self):
        return self._Elevator__maxCapacity
    
    def getID(self):
        return self._Elevator__Id
    
    def isUp(self):
        return self._Elevator__isUp
    
    def getType(self):
        return self._Elevator__type

    def getDinningFloor(self):
        return self._Elevator__dinningFloor
    
    def getMeanFloor(self):
        return self._Elevator__meanFloor
    
    def getDefaultFloor(self):
        return self._Elevator__defaultFloor
    
    # Method

    def signal(self, currFloor = 0):
        # this method will check the current floor that have any request occur or not and return result 
        if currFloor == 0: floor = self.getCurrFloor()
        scatterPassenger = self.__elevatorHandler.getQueue() #[ {floor 1: nPassenger 1,...,floor n:nPassenger n}1, ... {floor 1: nPassenger 1, ..., floor n : nPassenger n}n]
        neatPassenger = dict() #{floor 1: nPassenger 1,...,floor n: nPassenger n}
        neatPassenger.update({ i:0 for i in range(1, self.getMaxFloor() + 1)})
        for floor in scatterPassenger:
            for key in floor.keys():
                neatPassenger[key] += floor[key]

        flag = False
        maxFloor = [self.getMeanFloor(), self.getMaxFloor()](self.getType() == 1)
        if self.isUp():
            # if the elevator direction is going up
            for i in range(currFloor, maxFloor):
                if neatPassenger.get(i) > 0:
                    flag = True
                    break
        else:
            # if the elevator direction is going down
            for i in range(currFloor, 1, -1):
                if self.getType() == 1 and i < self.getMeanFloor() and i != 1:
                    continue
                if neatPassenger.get(i) > 0:
                    flag = True
                    break

        return flag

    def unloadPassenger(self):
        """ Release passenger back in to the building """
        nPassenger = self._Elevator__servTo[self.getCurrFloor()]
        self._Elevator__servTo[self.getCurrFloor()] = 0
        self._Elevator__currCapacity -= nPassenger
        self.__elevatorHandler.servFloor(self.__currFloor, nPassenger)
        #time.sleep(1)
        return self

    def move(self):
        # Give the direction to elevator
        if self.getCurrCapacity() == 0 and \
           self.getCurrFloor() != self.getMaxFloor() and \
           self.getCurrFloor() != 1:
            # if the elevator is empty go along with Shortest distance first algorithm
            scatterPassenger = self.__elevatorHandler.getQueue() #[ {floor 1: nPassenger 1,...,floor n:nPassenger n}1, ... {floor 1: nPassenger 1, ..., floor n : nPassenger n}n]
            nPassQ = dict() #{floor 1: nPassenger 1,...,floor n: nPassenger n}
            nPassQ.update({ i:0 for i in range(1, self.getMaxFloor() + 1)})
            for floor in scatterPassenger:
                for key in floor.keys():
                    nPassQ[key] += floor[key]
            nOnTop, nOnBottom = 0, 0
            for i in range(1, self.getMaxFloor()):
                if (nOnTop != 0 and nOnBottom != 0) or \
                   (self.getCurrFloor() + i > self.getMaxFloor() or self.getCurrFloor() - i < 1):
                       break
                if nPassQ.get(self.getCurrFloor() + i) != 0 and nOnTop == 0: nOnTop = i
                if nPassQ.get(self.getCurrFloor() - i) != 0 and nOnBottom == 0: nOnBottom = i
            if nOnBottom < nOnTop:
                self._Elevator__isUp = False
            elif nOnBottom > nOnTop:
                self._Elevator__isUp = True
            else:
                if nOnTop == nOnBottom == 0:
                    if self.getCurrFloor() > self.getDefaultFloor():
                        self._Elevator__isUp = False
                    else:
                        self._Elevator__isUp = True
        if self.getCurrFloor() == self.getMeanFloor():
            # if this elevator is not a high floor transport elevator, then change direction
            if self.getType() != 1:
                self._Elevator__isUp = False
        elif self.getCurrFloor() == self.getMaxFloor():
            # if the elvator is on the highest floor, then change its direction to down
            self._Elevator__isUp = False
        elif self.getCurrFloor() == 1:
            # if the elvator is on the lowest floor, then change its direction to up
            self._Elevator__isUp = True
        
        # Move action
        if self.isUp():
            # if direction of the elevator is set to up
            # doAnimation(self.getSpeed())
            if self.getCurrCapacity() != 0:
                self._Elevator__currFloor += 1
                return -1 #return -1 when direction is up
        else:
            #if directtion of the elevator is set to down
            # doAnimation(self.getSpeed())
            if self.getCurrCapacity() != 0:
                self._Elevator__currFloor -= 1
                return 1 #return 1 when direction is up

    def loadPassenger(self):
        """ Load passenger from building to the elevator """
        passenger = self.__elevatorHandler.dequeue(self.__currFloor, self.__maxCapacity - self.__currCapacity)
        capacity = 0
        for d in passenger:
            lst = d.keys()
            for k in lst:
                self.__servTo[k] += d.get(k)
                capacity += d.get(k)
        self.__currCapacity += capacity
        return self