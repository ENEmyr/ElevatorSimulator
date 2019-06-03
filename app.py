import sys
from PyQt5.QtWidgets import QApplication
from views.MainView import MainView
from controllers.MainController import MainController
from models.MainModel import MainModel

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_model = MainModel()
        self.main_controller = MainController(self.main_model)
        self.main_view = MainView(self.main_model, self.main_controller)
        self.main_view.show()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())