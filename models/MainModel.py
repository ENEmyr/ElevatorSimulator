from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool
import time
import threading
from multiprocessing.dummy import Pool as ThreadPool

class MainModel(QObject):
    startBtn_changed = pyqtSignal(bool)
    stopBtn_changed = pyqtSignal(bool)
    pauseBtn_changed = pyqtSignal(bool)
    windowExit_changed = pyqtSignal(bool)
    moveElevator_changed = pyqtSignal(int, int)
    threadPool = QThreadPool()

    def threadFunc(self, nTime):
        for i in range(1, nTime):
            if i < 11:
                self.moveElevator_changed.emit(int(0), int(1))
            else:
                self.moveElevator_changed.emit(int(0), int(-1))
            time.sleep(1)

    @property
    def startBtn(self):
        return self.__startBtn

    @startBtn.setter
    def startBtn(self, value):
        self.__startBtn = value
        self.startBtn_changed.emit(bool(value))

    @property
    def pauseBtn(self):
        return self.__pauseBtn

    @pauseBtn.setter
    def pauseBtn(self, value):
        self.__pauseBtn = value
        self.pauseBtn_changed.emit(bool(value))
    
    @property
    def stopBtn(self):
        return self.__stopBtn

    @stopBtn.setter
    def stopBtn(self, value):
        self.__stopBtn = value
        self.stopBtn_changed.emit(bool(value))

    @property
    def windowExit(self):
        self.windowExit_changed.emit(True)
    
    def ev(self, l):
        print("{} {}".format(l[0], l[1]))
        #self.moveElevator_changed.emit(int(id), int(val))

    @property
    def moveElevator(self):
        """ in this method will create 1+nElevator threads, 1 for Passenger Obj and others for Elevator Obj """
        #nElevator = open("file", r)
        thread1 = threading.Thread(target=self.threadFunc, args=(10,))

    def __init__(self):
        super().__init__()

        self.__startBtn = False 
        self.__stopBtn = False
        self.__pauseBtn = False
    