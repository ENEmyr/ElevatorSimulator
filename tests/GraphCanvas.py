from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib import style

class GraphCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        style.use('seaborn-pastel')
        self.__figure = Figure(figsize=(width, height), dpi = dpi)
        super().__init__(self.__figure)
        self.__axes = self.__figure.add_subplot(111)
        self.__ani = animation.FuncAnimation(self.__figure, self.animate, interval = 1000)
    
    def animate(self, i):
        graph_data = open('./src/plot.txt', 'r').read()
        labels = ["Time(hour)", "Population"]
        lines = graph_data.split('\n')
        xList = []
        yList = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xList.append(int(x))
                yList.append(int(y))
        self.__axes.clear()
        self.__axes.set_title("Traffics")
        self.__axes.set_xlabel(labels[0])
        self.__axes.set_ylabel(labels[1])
        self.__axes.plot(xList, yList)

'''
    def plot(self):
        x = np.array([50, 30, 40])
        labels = ["A", "B", "C"]
        ax = self.figure.add_subplot(111)
        ax.pie(x, labels=labels)
'''