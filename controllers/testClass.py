from PyQt5.QtCore import QObject, pyqtSignal, QThread, QRunnable
import time
from controllers.WSignals import WSignals
import traceback, sys

class fakeElevator(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    id = None
    round = 0

    def __init__(self, id, round, *args, **kwargs):
        super(fakeElevator, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.id = id
        self.round = round
        self.args = args
        self.kwargs = kwargs
        self.signals = WSignals()    

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress        

    def fnRun(self, id, round, progress_callback):
        for i in range(1, self.round):
            if i < self.round//2:
                self.progress_callback.emit(int(self.id), int(1))
            else:
                self.progress_callback.emit(int(self.id), int(-1))
            time.sleep(1)

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fnRun(self.id, self.round, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
    
    # id = None
    # signal = pyqtSignal(int, int)
    # round = 0

    # def __del__(self):
    #     self.wait()
    
    # def __init__(self, id, round, signal):
    #     QRunnable.__init__(self)
    #     self.id = id
    #     self.round = round
    #     self.signal = signal
    
    # def run(self):
    #     for i in range(1, self.round):
    #         if i < self.round//2:
    #             self.signal.emit(int(self.id), int(1))
    #         else:
    #             self.signal.emit(int(self.id), int(-1))
    #         time.sleep(1)