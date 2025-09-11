
import sys
from MainScreen.MainScreenUI  import Ui_Frame
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets          import QMainWindow
from PyQt5.QtCore               import QDateTime, QObject, Qt, QTimer, pyqtSignal, pyqtSlot
import os

from MainScreen.NetworkAndConnectNotify import NetworkAndConnectNotify
from NetworkModule.ControlNetworkModule import ControlNetWorkModule
from ProcessManagement.ProcessManagement import ProcessManament

class Main(Ui_Frame, QObject):
    __networkNotification:NetworkAndConnectNotify
    __networkModuleController:ControlNetWorkModule
    __concentratordAndForwarderPM:ProcessManament
    def __init__(self, MainWindow:QMainWindow):
        QObject.__init__(self)
        self.setupUi(MainWindow)
        self.__networkNotification = NetworkAndConnectNotify(self.frame_networkAndConnectNotify)
        self.__networkModuleController = ControlNetWorkModule(self.__networkNotification)
        self.__networkModuleController.Start4Gmodule()
        self.__concentratordAndForwarderPM = ProcessManament()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if(os.uname()[2].__contains__("sunxi")):
        app.setOverrideCursor(Qt.BlankCursor)
    screen = app.primaryScreen()
    width = 800
    height = 480
    MainWindow = QMainWindow()
    if(os.uname()[2].__contains__("sunxi")):
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.setFixedSize(QtCore.QSize(width, height))
    ui = Main(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())