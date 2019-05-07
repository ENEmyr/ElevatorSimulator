import threading
import time

class testClass:

    __instance = None
    __threadLock = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if testClass.__instance == None:
            testClass.__threadLock = threading.Lock()
            testClass.__instance = testClass
        return testClass.__instance

    @staticmethod
    def printTime():
        return "time : {}".format(time.ctime(time.time()))
    
    @staticmethod
    def pararelCal(*args):
        name=threading.current_thread().getName()
        testClass.__threadLock.acquire()
        print("I'm {} a data is : {}  {}".format(name, args[0], testClass.printTime()))
        time.sleep(2)
        testClass.__threadLock.release()
        return
    
    def __init__(self):
        """ Virtually private constructor """
        if testClass.__instance != None:
            testClass.__threadLock = None
            testClass.__instance = None
        raise Exception("Can't instantiate a singleton class.")
    