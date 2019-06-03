class ElevatorHandler:

    __instance = None
    __user = ""
    __passenger_queue = [] 
    __max_floor = 0
    __nElevator = 0
    __waitForGetIntoFloor = dict()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ElevatorHandler.__instance == None:
            ElevatorHandler.__instance = ElevatorHandler
        return ElevatorHandler.__instance

    @staticmethod
    def setUser(msg):
        ElevatorHandler.__User = msg
        return ElevatorHandler.__instance
    
    @staticmethod
    def setNElevator(n):
        ElevatorHandler.__nElevator = n
        return ElevatorHandler.__instance

    @staticmethod
    def setMaxFloor(max):
        ElevatorHandler.__max_floor = max
        # Passenger queue init
        for i in range(1, max + 1):
            passengerEachFloor = dict()
            for j in range(1, max + 1):
                if i == 1 : ElevatorHandler.__waitForGetIntoFloor.update({ j : 0 })
                passengerEachFloor.update({j : 0})
            ElevatorHandler.__passenger_queue.append(passengerEachFloor)
        return ElevatorHandler.__instance
    
    @staticmethod
    def getQueue():
        return ElevatorHandler.__passenger_queue
    
    @staticmethod
    def getWait():
        return ElevatorHandler.__waitForGetIntoFloor

    @staticmethod
    def getMaxFloor():
        return ElevatorHandler.__max_floor
    
    @staticmethod
    def getUser():
        return ElevatorHandler.__User
    
    @staticmethod
    def enqueue(fromFloor:int, intratenant:dict):
        """ Used by passenger """
        if ElevatorHandler.__max_floor == 0:
            raise Exception("passenger_queue is empty, please initialize max floor.")
        for key in intratenant.keys():
            ElevatorHandler.__passenger_queue[fromFloor - 1][key] += intratenant[key]
        return ElevatorHandler.__instance

    @staticmethod
    def dequeue(elevatorID, currentFloor, isUp, size):
        """ Decide to let an elevator dequeue or not, use by elevators."""
        if ElevatorHandler.__max_floor == 0:
            raise Exception("passenger_queue is empty, please initialize max floor.")
        meanFloor = ElevatorHandler.__max_floor - ElevatorHandler.__max_floor//2
        leftList = []
        for tFloor in ElevatorHandler.__passenger_queue[currentFloor - 1]:
            # if this elevator is low floor serv, then break when the floor over the limit
            if elevatorID < meanFloor and tFloor > meanFloor: break
            # if this elevator is high floor serv and the direction is going down, then break when the floor over or equal to mean floor
            if elevatorID >= meanFloor and not isUp and tFloor >= meanFloor: break
            # if this elevator is high floor serv and the direction is going down, then skip when the floor under mean floor but not equal to 1
            if elevatorID >= meanFloor and not isUp and tFloor < meanFloor and tFloor != 1: continue
            # if this elevator is high floor serv and the direction is going up, then skip when the floor under mean floor but not equal to 1
            if elevatorID >= meanFloor and isUp and currentFloor-1 != 0 and tFloor <= meanFloor: continue
            if isUp:
                nLeft = ElevatorHandler.__passenger_queue[currentFloor - 1][tFloor]
                if nLeft == 0 : continue # if this floor have no one want to go
                if size - nLeft < 0:
                    ElevatorHandler.__passenger_queue[currentFloor - 1][tFloor] = nLeft - size
                    nLeft = size
                    size = 0
                    leftList.append(dict({tFloor : nLeft}))
                    break
                else:
                    ElevatorHandler.__passenger_queue[currentFloor - 1][tFloor] = 0
                    size -= nLeft
                    leftList.append(dict({tFloor : nLeft}))
                    if size == 0:
                        break
            else:
                nLeft = ElevatorHandler.__passenger_queue[currentFloor - 1][tFloor]
                if size - nLeft < 0:
                    ElevatorHandler.__passenger_queue[currentFloor - 1][tFloor] = nLeft - size
                    nLeft = size
                    leftList.append(dict({tFloor : nLeft}))
                    break
                else:
                    ElevatorHandler.__passenger_queue[currentFloor - 1][tFloor] = 0
                    size -= nLeft
                    leftList.append(dict({tFloor : nLeft}))
                    if size == 0:
                        break
        return leftList
    
    @staticmethod
    def servFloor(floor, nPassenger):
        """ Use by Elevator class to serv a passenger on its room into floor """
        if ElevatorHandler.__max_floor == 0:
            raise Exception("passenger_queue is empty, please initialize max floor.")
        ElevatorHandler.__waitForGetIntoFloor[floor] += nPassenger
        return ElevatorHandler.__instance

    @staticmethod
    def getToFloor(floor):
        """ Use by Passenger class to receive waiting passenger into its floor """
        if ElevatorHandler.__max_floor == 0:
            raise Exception("passenger_queue is empty, please initialize max floor.")
        nPassenger = ElevatorHandler.__waitForGetIntoFloor[floor]
        ElevatorHandler.__waitForGetIntoFloor[floor] = 0
        return nPassenger
    
    def __init__(self):
        """ Virtually private constructor """
        if ElevatorHandler.__instance != None:
            ElevatorHandler.__instance = None
        raise Exception("Can't instantiate a singleton class.")

# if __name__ == "__main__":
#     e = ElevatorHandler.getInstance()
#     size = 4
#     e.setUser('E')
#     e.setNElevator(3).setMaxFloor(6)

#     print(e.getWait())
#     e.servFloor(2, 25)
#     print(e.getWait())
#     print("\n\n")
#     e.getToFloor(2)
#     print(e.getWait())

#     e.enqueue(3, {5:8, 1:3, 2:4})
#     e.enqueue(1, {5:7, 2:2, 3:1, 4:2})
#     e.enqueue(2, {5:7, 1:1})
#     e.enqueue(4, {5:2, 6:4, 1:7})
#     queue = e.getqueue()
#     print(queue)
#     print(e.getuser())
#     dequeue = e.dequeue(2, 3, false, size)
#     queue = e.getqueue()
#     print(queue)
#     print(dequeue)
#     print(size)