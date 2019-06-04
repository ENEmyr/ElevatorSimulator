from controllers.Elevator import Elevator
from controllers.ElevatorHandler import ElevatorHandler
from controllers.Passenger import Passenger
import time

if __name__ == "__main__":
    maxElevator = 3
    maxFloor = 10
    timeLimit = 12 
    elevatorHandler = ElevatorHandler.getInstance()
    elevatorHandler.setNElevator(maxElevator).setMaxFloor(maxFloor)
    passengers = []
    elevators = []
    passengers.append(Passenger(1, elevatorHandler.getMaxFloor(), 50, timeLimit))
    for floor in range(2, elevatorHandler.getMaxFloor() + 1):
        passengers.append(Passenger(floor, elevatorHandler.getMaxFloor(), 0, timeLimit))
    for eID in range(1, maxElevator + 1):
        if eID <= maxElevator - maxElevator//2:
            elevators.append(Elevator(eID, 10, maxFloor, 0))
        else:
            elevators.append(Elevator(eID, 10, maxFloor, 1))
    
    for i in range(1, timeLimit + 1):
        print("\nTime : {}\n".format(i))
        for n in range(maxFloor):
            print("Floor {} passenger {}\n".format(n+1, passengers[n]._Passenger__maxPassenger))
            passengers[n].setTime(i)
            passengers[n].genArrival().transfer().sendToQueue()
        print("\n {}".format('='*20))
        for j in range(1, 20):
            for n in range(len(elevators)):
                #print(" >> Lift {} now in floor {}\n".format(elevators[n].getID(), elevators[n].getCurrFloor()))
                elevators[n].loadPassenger().move()
                elevators[n].unloadPassenger()
        for n in range(len(passengers)):
            passengers[n].getInFloor()
        time.sleep(0.2)
    
    passengers[1].getInFloor()
    
    print("\n\nFloor {} passenger {}\n".format(1, passengers[1]._Passenger__maxPassenger))
    print("\n\nWaiting: {}".format(elevatorHandler.getQueue()))
    # passengers[0].genArrival().transfer().sendToQueue()
    # # print(passengers[0]._Passenger__maxPassenger)
    # # print(passengers[0]._Passenger__eachFloor[1])
    # for f in elevatorHandler.getQueue():
    #     print("{} \n".format(f))
    
    # elevators[0].loadPassenger()

    # print(elevators[0].getCurrCapacity())
    # print(elevators[0]._Elevator__servTo)
    # print("\n")

    # for f in elevatorHandler.getQueue():
    #     print("{} \n".format(f))
    
    # print("\nmaxPassenger F2 = {}\n".format(passengers[1]._Passenger__maxPassenger))
    # elevators[0].move()
    # elevators[0].unloadPassenger()
    # passengers[1].getInFloor()
    # print("\n\n{}\n\n".format(elevatorHandler.getWait()))
    # print("\nmaxPassenger F2 = {}\n".format(passengers[1]._Passenger__maxPassenger))
    # for e in elevators:
    #     print("type {}".format(e.getType()))
    # for p in passengers:
    #     print("{} {}\n".format(p.getEachFloor(), p.loadPassenger()))
