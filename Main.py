
import sys
from PyQt5                      import QtCore, QtGui
from PyQt5.QtCore               import QDateTime, QObject, Qt, QTimer, pyqtSignal, pyqtSlot, QCoreApplication
import os
import signal
from NetworkModule.ControlNetworkModule import ControlNetWorkModule
from ProcessManagement.ProcessManagement import ProcessManagement

class Main(QObject):
    __networkModuleController:ControlNetWorkModule
    __concentratordAndForwarderPM:ProcessManagement
    def __init__(self):
        QObject.__init__(self)
        self.__networkModuleController = ControlNetWorkModule()
        self.__networkModuleController.Start4Gmodule()
        self.__concentratordAndForwarderPM = ProcessManagement()

    #     self.__timerTest = QTimer(self)
    #     self.__timerTest.timeout.connect(self.__test)
    #     self.__timerTest.start(1000)
    # def __test(self):
    #     print("ok...")
    
if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    signal.signal(signal.SIGINT, lambda *args: app.quit())
    main = Main()
    sys.exit(app.exec_())