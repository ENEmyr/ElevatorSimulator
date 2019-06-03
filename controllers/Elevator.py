import time

class Elevator:
    
    #property
    __maxFloor = 30
    __currFloor = 1
    __maxCapacity = 10
    __currCapacity = 0
    __isUp = True
    __Id = 0
    __type = 0 #Low floor or High floor
    __speed = 1
    __dinningFloor = 0
    __meanFloor = 15
    __servTo = dict()
    __defaultFloor = 1

    # redundant property, used for data mocking
    __passenger_queue = [
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
        { 1 : 0, 2 : 0, 3 : 4, 0 : 0, 5 : 0, 6 : 0, 7 : 0 },
    ]

    def __init__(self, ID, maxCapacity, maxFloor, type, dinningFloor = 0):
        self._Elevator__Id = ID
        self._Elevator__maxCapacity = maxCapacity
        self._Elevator__type = type
        self._Elevator__maxFloor = maxFloor
        self._Elevator__dinningFloor = dinningFloor
        self._Elevator__meanFloor = maxFloor//2
        self._Elevator__servTo.update( {i : 0 for i in range(1, maxFloor + 1)} )
        
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
    
    def addServ(self):
        # thread.accquire()
        nPassenger = self.getQueue(self.getCurrFloor())
        dequeue_dict = dict()
        # if the elevator is not empty go along with SCAN algorithm
        for p in nPassenger.keys():
            # SCAN algorithm
            if self.isUp() and p <= self.getCurrFloor():
                # if the direction is up, the elevator will not receive a passenger that laying on the down floors
                continue
            elif not self.isUp() and p >= self.getCurrFloor():
                # if the direction is down, the elevator will not receive a passenger that laying on the top floors
                break
            # passenger pick up in the conditions that current capacity of elevator must have enough of space
            if self.getCurrCapacity() < self.getMaxCapacity():
                nPick = self.getMaxCapacity() - self.getCurrCapacity()
                if nPick > nPassenger.get(p):
                    nPick = nPassenger.get(p)
                self._Elevator__servTo[p] += nPick
                self._Elevator__currCapacity -= nPick
                dequeue_dict[p] = nPick
            else:
                break
        self.dequeue(self.getCurrFloor(), dequeue_dict)
        # thread.release()
        time.sleep(1)
        return self

    def signal(self, floor = 0):
        # this method will check the current floor that have any request occur or not and return result 
        if floor == 0: floor = self.getCurrFloor()
        nPassenger = self.getQueue(floor)
        flag = False
        maxFloor = [self.getMeanFloor(), self.getMaxFloor()](self.getType() == 1)
        if self.isUp():
            # if the elevator direction is going up
            for i in range(floor, maxFloor):
                if nPassenger.get(i) > 0:
                    flag = True
                    break
        else:
            # if the elevator direction is going down
            for i in range(floor, 1, -1):
                if self.getType() == 1 and i < self.getMeanFloor() and i != 1:
                    continue
                if nPassenger.get(i) > 0:
                    flag = True
                    break

        return flag

    def serv(self):
        # release passenger to the floor
        nPassenger = self._Elevator__servTo[self.getCurrFloor()]
        self._Elevator__servTo[self.getCurrFloor()] = 0
        self._Elevator__currCapacity += nPassenger
        self.passengerArrived(self.getCurrFloor(), nPassenger)
        time.sleep(1)
        return self

    def moveToDefault(self):
        if self.getCurrFloor() == self.getDefaultFloor():
            return True
        if self.getCurrCapacity() != 0:
            return self.move()
        if self.signal(self.getCurrFloor() + 1):
            return self.move()
        else:
            if self.getCurrFloor() > self.getDinningFloor():
                self._Elevator__isUp = False
                self._Elevator__currFloor -= 1
            else:
                self._Elevator__isUp = True
                self._Elevator__currFloor += 1
        return moveToDefault()

    def move(self):
        # Give the direction to elevator
        if self.getCurrCapacity() == 0 and \
           self.getCurrFloor() != self.getMaxFloor() and \
           self.getCurrFloor() != 1:
            # if the elevator is empty go along with Shortest distance first algorithm
            nPassQ = self.getQueue(self.getCurrFloor())
            nOnTop, nOnBottom = 0, 0
            for i in range(1, self.getMaxFloor()):
                if (nOnTop != 0 and nOnBottom != 0) or \
                   (self.getCurrFloor() + i > self._Elevator__maxFloor or self.getCurrFloor() - i < 1):
                       break
                if nPassQ.get(self.getCurrFloor() + i) != 0 and nOnTop == 0: nOnTop = i
                if nPassQ.get(self.getCurrFloor() - i) != 0 and nOnBottom == 0: nOnBottom = i
            if nOnBottom < nOnTop:
                self._Elevator__isUp = False
            elif nOnBottom > nOnTop:
                self._Elevator__isUp = True
            else:
                if nOnTop == nOnBottom == 0:
                    return self.moveToDefault()
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
            self._Elevator__currFloor += 1
        else:
            #if directtion of the elevator is set to down
            # doAnimation(self.getSpeed())
            self._Elevator__currFloor -= 1
        
        # Move service condition for High floor transport elevator that can't do a service on low floor
        if (self.getType() == 1) and\
           (self.getCurrFloor() < self.getMeanFloor()) and\
           (self.getCurrFloor() != 1):
                return self.move()
        # Decide to serv passenger on this floor or not
        if self._Elevator__servTo[self.getCurrFloor()] > 0:
            self.serv()
        # Decide to add more passenger or pass away
        if self.signal() and self.getCurrCapacity() != self.getMaxCapacity():
            self.addServ()
        
        return self.move()

                
    # Redundant method, use for data mocking
    
    def getQueue(self, floor):
        # interface to ElevatorHandler
        return self._Elevator__passenger_queue[floor]
    
    def dequeue(self, floor, passenger_dict):
        # interface to ElevatorHandler
        for k in passenger_dict.keys():
            self._Elevator__passenger_queue[k] -= passenger_dict.get(k)
        return
    
    def passengerArrived(self, floor, n):
        # interface to ElevatorHandler
        pass
        return
    
    def isDinning(self):
        # interface to ElevatorHandler
        return False