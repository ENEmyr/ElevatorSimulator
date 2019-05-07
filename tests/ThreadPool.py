import time
from multiprocessing.dummy import Pool as ThreadPool
import os
from threading import Thread
import threading
from Elevator import Elevator
from concurrent.futures import ThreadPoolExecutor

threadLock = threading.Lock()
threadsList = dict() 

def runElevator(n):
    result = 0
    name = threading.current_thread().getName()
    print(threadsList[name].getStart())
    threadsList[name].setFloor(n)
    threadLock.acquire()
    print(threadsList[name].printTime())
    result = threadsList[name].cal()
    time.sleep(2)
    threadLock.release()
    return result 

def genElevator(numbers, threads=2):
    pool = ThreadPool(threads)
    for i in range(1, threads+1):
        threadsList.update({"Thread-" + str(i) : Elevator("Thread-" + str(i))})
    results = pool.map(runElevator, numbers)
    pool.close()
    pool.join()
    return results

def main():
    workers = int(input())
    numbers = [i for i in range(1, 8)]
    squareNumbers = genElevator(numbers, workers)
    for n in squareNumbers:
        print(n)
    print("Thread name : {} and final floor : {}".format(threadsList['Thread-3'].getName(), threadsList['Thread-3'].getFloor()))


if __name__ == "__main__":
    main()