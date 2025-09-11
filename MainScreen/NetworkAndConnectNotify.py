
from  MainScreen.NetworkAndConnectNotifyUI  import Ui_Frame
from  PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject, QPropertyAnimation
from  PyQt5 import QtCore, QtGui, QtWidgets

class NetworkAndConnectNotify(QObject, Ui_Frame):
    SignalResetSimModule = pyqtSignal(bool)
    SignalNotInternet = pyqtSignal()   # tin hieu duoc bat o ControlNetworkModule de khoi tao lai Qmi
    SignalInternetAvailable = pyqtSignal()
    SignalShutdownSimModule = pyqtSignal()
    def __init__(self, Frame):
        Ui_Frame.__init__(self)
        QObject.__init__(self)
        self.setupUi(Frame)
        self.pixmapIn0 = QtGui.QPixmap("icon/in0.png")
        self.pixmapIn1 = QtGui.QPixmap("icon/in1.png")
        self.pixmapIn2 = QtGui.QPixmap("icon/in2.png")
        self.pixmapIn3 = QtGui.QPixmap("icon/in3.png")
        self.pixmapIn4 = QtGui.QPixmap("icon/in4.png")
        self.__pixmapInternetAvailable = QtGui.QPixmap("icon/internet25.png")
        self.__pixmapNotInternet = QtGui.QPixmap("icon/hourGlass25.png")
        self.__pixmapNotConnectQMIdevice = QtGui.QPixmap("icon/warning25.png")
        self.__flagNetworkModeShow = False
        self.__flagSPNshow = False
        self.__flagNetworkModeShow = False
        self.__itemMergin = 6
        self.__waitGif = QtGui.QMovie("icon/wait40.gif")
        self.__numberTimeNotReciptGPRMC = 0
        self.__intensityAnim = None
        self.__networkModeAnim = None
        self.__spnAnim = None
        self.__internetAnim = None
        self.__currentGPSstt = None
        self.__currentServerConnectStt = False
        self.__currentSPN = ""
        self.__defaultStatus()
        self.label_intensity.mousePressEvent = lambda event: self.SignalResetSimModule.emit(False)
        self.__numberTimeNotGPS = 0
        self.__haveQmiDevice = True

    def setGlobalObj(self, globalObj) -> None:
        from GlobalClass.GlobalObject import GlobalObject
        self.__globalObj:GlobalObject = globalObj
    
    def findQmiDevice(self, find):
        self.__haveQmiDevice = find
        if(not find):
            self.label_internetStatus.setPixmap(self.__pixmapNotConnectQMIdevice)
        
    def getNetworkModeShowStt(self):
        """lệnh CNSMOD có thể không trả lời đúng trạng thái mạng khi khởi tạo lần đầu tiên nên cần check lại xem đã nhận được hay chưa. nếu chưa nhận được sẽ gửi lại CNSMOD

        Returns:
            [bool]]: Đã có trạng thái mạng hiển thị hay chưa
        """
        return self.__flagNetworkModeShow
    
    def getSPNshowStt(self):
        """lệnh CSPN có thể không trả lời đúng trạng thái mạng khi khởi tạo lần đầu tiên nên cần check lại xem đã nhận được hay chưa. nếu chưa nhận được sẽ gửi lại CSPN
        """
        return self.__flagSPNshow

    def restartModuleSim(self):
        """Khoi dong lai module sim
        khi click vao sim -> yeu cau reset module sim (ControlNetworkModule) -> Nếu đang không có sim -> Restart 
        """
        self.__defaultStatus()

    def __defaultStatus(self):
        self.__flagNetworkModeShow = False
        self.__flagSPNshow = False
        self.__flagNetworkModeShow = False
        self.label_intensity.setGeometry(QtCore.QRect(6, 6, 40, 40))
        self.label_intensity.setMovie(self.__waitGif)
        self.__waitGif.start()
        self.label_internetStatus.setPixmap(self.__pixmapNotInternet)
        self.serverConnectChangeStt(False)
        self.gpsStt(False)
        self.label_network.hide()
        self.label_internetStatus.hide()
        self.label_spn.hide()
    
    def serverConnectStatus(self, stt):
        if(self.__currentServerConnectStt == stt):
            return
        self.__currentServerConnectStt = stt
        if(stt):
            self.label_serverStatus.setStyleSheet('background-color: rgb(0, 200, 0);border-radius:10px')
        else:
            self.label_serverStatus.setStyleSheet('background-color: rgb(150, 150, 150);border-radius:10px')

    def noSim(self):
        self.label_network.hide()
        self.label_internetStatus.hide()
        self.label_spn.hide()
        self.label_intensity.setPixmap(QtGui.QPixmap("icon/notSimCard.png"))
        if(self.__flagSPNshow | self.__flagNetworkModeShow):
            self.__changeIntensityPosition(self.__itemMergin)

    def changeIntensity(self, intensity):
        if(intensity == 4):
            self.label_intensity.setPixmap(self.pixmapIn4)
        elif(intensity == 3):
            self.label_intensity.setPixmap(self.pixmapIn3)
        elif(intensity == 2):
            self.label_intensity.setPixmap(self.pixmapIn2)
        elif(intensity == 1):
            self.label_intensity.setPixmap(self.pixmapIn1)
        elif(intensity == 0):
            self.label_intensity.setPixmap(self.pixmapIn0)
    
    def showNetworkMode(self, strMod):
        self.label_network.setText(strMod)
        self.__showNetworkMode()
    
    def __showNetworkMode(self):
        if(not self.__flagNetworkModeShow):
            self.label_network.show()
            self.__flagNetworkModeShow = True
            self.__slideIntensityToRight(self.label_network.width() + self.__itemMergin * 2)
            self.__showInternet()
            self.__networkModeAnim = self.__createAnim(self.label_network, 0-self.label_network.width(), self.__itemMergin)
            self.__networkModeAnim.start()

    def __showInternet(self):
        self.label_internetStatus.show()
        self.__internetAnim = self.__createAnim(self.label_internetStatus, 0-self.label_network.width(), self.label_network.width() + self.__itemMergin)
        self.__internetAnim.start()

    def showSPN(self, spnName):
        spnName = spnName.strip()
        if(len(spnName.strip()) > 1):
            if(self.__currentSPN != spnName):
                self.__currentSPN = spnName
                stringWidth = self.label_spn.fontMetrics().boundingRect(spnName).width()
                self.label_spn.setGeometry(QtCore.QRect(self.label_spn.x(), self.label_spn.y(), stringWidth, self.label_spn.height()))
                self.label_spn.setText(spnName)
                self.__showSPN()

    def __showSPN(self):
        self.__flagSPNshow = True
        self.label_spn.show()
        self.__changeIntensityPosition(self.label_spn.width() + self.__itemMergin * 2)
        spn_width = self.label_spn.width()
        self.__spnAnim = self.__createAnim(self.label_spn, 0-spn_width, self.__itemMergin)
        self.__spnAnim.start()

    def __slideIntensityToRight(self, desX):
        if(self.label_intensity.x() < desX):
            self.__changeIntensityPosition(desX)

    def __changeIntensityPosition(self, desX):
        curX = self.label_intensity.x()
        self.__intensityAnim = self.__createAnim( self.label_intensity, 0, desX)
        self.__intensityAnim.start()

    # def showNetworkMode(self, strMod):
    #     if(strMod == "NotSim"):
    #         self.label_network.setText('')
    #         self.label_network.setGeometry(self.label_network.x(), self.label_network.y(), self.label_network.width(), 40)
    #         self.label_spn.hide()
    #         self.label_network.setPixmap(QtGui.QPixmap("icon/notSimCard.png"))
    #     elif(strMod == "?"):
    #         self.label_network.setText('')
    #         self.label_network.setPixmap(self.pixmapWaitService)
    #     else:
    #         self.label_network.setGeometry(self.label_network.x(), self.label_network.y(), self.label_network.width(), 25)
    #         self.label_network.setText(strMod)
    #         self.label_spn.show()

    def serverConnectChangeStt(self, stt):
        if(stt):
            self.label_serverStatus.setStyleSheet('background-color: rgb(0, 200, 0);border-radius:10px')
        else:
            self.label_serverStatus.setStyleSheet('background-color: rgb(150, 150, 150);border-radius:10px')

    def gpsStt(self, stt):
        """trang thai GPS thay doi

        Args:
            stt ([bool]): true : co GPS <=> false : ko co GPS
        """
        if(self.__currentGPSstt == stt):
            # if(not self.__currentGPSstt):  # nếu tiếp tục ko có tín hiệu GPS
            #     self.__numberTimeNotGPS += 1
            #     if(self.__numberTimeNotGPS == 20): # 3s 1 lan gps. 15 lan = 45s
            #         if(self.__globalObj.currentStudent != None):  # chi thong bao khi co hojc vien dang dang nhap
            #             self.__numberTimeNotGPS = 0
            return
        elif(stt):
            self.label_gpsStatus.setStyleSheet('background-color: rgb(0, 200, 0);border-radius:10px')
            if(self.__globalObj.currentStudent != None): 
                self.__numberTimeNotGPS = 0
        else:
            self.label_gpsStatus.setStyleSheet('background-color: rgb(150, 150, 150);border-radius:10px')
        self.__currentGPSstt = stt

    def gpsErr(self):
        self.__numberTimeNotReciptGPRMC += 1
        if(self.__numberTimeNotReciptGPRMC == 3):
            self.__numberTimeNotReciptGPRMC = 0
            self.SignalResetSimModule.emit(True)
        self.label_gpsStatus.setStyleSheet('background-color: rgb(200, 0, 0);border-radius:10px')
    
    def internetChangeStt(self, stt):
        if(stt):
            self.SignalInternetAvailable.emit()
            self.label_internetStatus.setPixmap(self.__pixmapInternetAvailable)
        else:
            self.SignalNotInternet.emit()
            if(not self.__haveQmiDevice):
                self.label_internetStatus.setPixmap(self.__pixmapNotConnectQMIdevice)
            else:
                self.label_internetStatus.setPixmap(self.__pixmapNotInternet)

    def __createAnim(self,obj, startX, stopX):
        anim = QPropertyAnimation(obj, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(QtCore.QRect(startX, obj.y() , obj.width(), obj.height()))
        anim.setEndValue(QtCore.QRect(stopX, obj.y(), obj.width(), obj.height()))
        return anim
