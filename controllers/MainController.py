from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QObject
import sys
import time

class MainController(QObject):

    #Property
    __model = None

    def __init__(self, model):
        super().__init__()

        self.__model = model
    
    def startClick(self):
        self.__model.startBtn = True 
        self.__model.moveElevator
    
    def stopClick(self):
        self.__model.stopBtn = True

    def pauseClick(self):
        self.__model.pauseBtn = True
    
    def windowExit(self):
        self.__model.windowExit
    
    def aboutUs(self):
        self.__model.aboutUs