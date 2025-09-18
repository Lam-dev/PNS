from GlobalClass.GlobalClass import DataGPS
from NetworkModule.ProcessResponse import ProcessResponse
import time
from UART.UARTconnection   import UART
from      PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import os

if(os.uname()[2].__contains__("sunxi")):
    import OPi.GPIO as GPIO
else:
    from NetworkModule   import FakeModule as GPIO
import enum
import threading
import glob
from NetworkModule.ControlPowerPin   import  ControlPowerPin
from NetworkModule.InitQmi     import  InitQmi

class ControlNetWorkModule(QObject):
    SignalGPSdata = pyqtSignal(DataGPS)
    SignalGPSinvalid = pyqtSignal()
    SignalImei = pyqtSignal(list)
    __SignalShowSPN = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        self.__controlPowerObj = ControlPowerPin(GPIO)
        self.GPIOobj = GPIO
      
        self.__runOnDevice = os.uname()[2].__contains__("sunxi")
        if(self.__runOnDevice):
            self.uartObj = UART("/dev/ttyS2", 115200, 0.2)
        else:
            self.uartObj = UART("/dev/ttyUSB1", 115200, 0.2)
        self.__processResponse = ProcessResponse()
        self.__processResponse.SignalNotSim.connect(self.__noSim)
        self.__processResponse.SignalNextStep.connect(self.__SignalNextStep)
        self.__processResponse.SignalSendInit.connect(self.SendInit)
        self.__processResponse.SignalGPSdata.connect(self.SignalGPSdata.emit)
        self.__processResponse.SignalGPSinvalid.connect(self.SignalGPSinvalid.emit)
        self.__processResponse.SignalHaveSim.connect(self.__HaveSim)
        self.__processResponse.SignalUnplugSim.connect(self.__unplugSim)
        self.__processResponse.SignalImei.connect(self.SignalImei.emit)
        self.__timerReinitQMI = QTimer(self)
        self.__timerReinitQMI.timeout.connect(self.__reinitQMI)
        self.__internetIsAvalable = False
        self.__moduleIsRunning = False

        self.stepInit4Gmodule = Init4GmoduleStep.CGPS.value
        self.uartObj.SignalReciptedData.connect(self.__processResponse.processResponseData)
        self.timerWaitFor4GmoduleReponse = QTimer(self)
        self.timerWaitFor4GmoduleReponse.timeout.connect(self.SendInit)
        self.__flagSimNotInserted = False
        self.__flagIs4Gor3G = False       #cờ xác định đang ở trạng thái 3G hoặc 4G(Chỉ trong trạng thái này mới chạy QMI)
        self.__flagQMIisRunning = False   #đang chạy một lệnh QMI hay không
        self.runInit4GshTime = 0
        self.__numberTimesRequestSPNfail = 0
        
    def __unplugSim(self):
        self.__flagSimNotInserted = True

    def __HaveSim(self):
        """co sim duoc ket noi
        """
        self.stepInit4Gmodule += 1
        self.SendInit()
    
    def __SignalNextStep(self):
        self.timerWaitFor4GmoduleReponse.stop()
        self.stepInit4Gmodule += 1

    def __noSim(self):
        if(not self.__flagSimNotInserted):
            self.__flagSimNotInserted = True
            self.stepInit4Gmodule  = Init4GmoduleStep.CGPSINFOCFG.value # neu khong co sim thi bo qua cac buoc check song, check mod...
            self.SendInit()
    
    def __sendCheckSimCard(self):
        if(self.__flagSimNotInserted):
            # self.__controlPowerObj.resetSimPowerPin()
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CPIN?\r"))

    def __ResetSimModule(self, forceReset):
        """Tat bat lai module sim
        """
        if(self.__flagSimNotInserted | forceReset):   #nếu đang không nhận được sim mới cho phép reset
            self.__networkAndConnectNotify.restartModuleSim()
            self.__flagSimNotInserted = False
            self.timerWaitFor4GmoduleReponse.stop()   
            self.stepInit4Gmodule = Init4GmoduleStep.CGPS.value
            self.__controlPowerObj.resetModuleThread()
            

    def OffSimModule(self, force):
        """Tat module sim cho che do khong chay DAT
        Args:
            force (_type_): _description_
        """
        if(force):
            self.__networkAndConnectNotify.restartModuleSim()
            self.__flagSimNotInserted = False
            self.timerWaitFor4GmoduleReponse.stop()
            self.stepInit4Gmodule = Init4GmoduleStep.CGPS.value
          
            self.__offSimModule()
    
    def __offSimModule(self):
        self.__controlPowerObj.offSimModule()
  

    def __internetAvailable(self):
        self.__internetIsAvalable = True
        if(self.__timerReinitQMI.isActive()):
            self.__timerReinitQMI.stop()

    def __notInternet(self):
        self.__internetIsAvalable = False
        if(self.stepInit4Gmodule >= Init4GmoduleStep.Finish.value):
            if(not self.__flagSimNotInserted):
                if(not self.__timerReinitQMI.isActive()):
                    self.__timerReinitQMI.start(30000)
                    
    def SendInit(self):
        if(self.stepInit4Gmodule != Init4GmoduleStep.Finish.value):
            self.timerWaitFor4GmoduleReponse.start(12000)
        if(self.stepInit4Gmodule == Init4GmoduleStep.CICCID.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CICCID\r")) #Yêu cầu ID sim
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CGSN.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CGSN\r")) # Yêu cầu số seri của module
        elif(self.stepInit4Gmodule == Init4GmoduleStep.AUTOCSQ.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+AUTOCSQ=1,1\r")) # Yêu cầu module thông báo khi có thay đổi cường độ sóng
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CSNMOD.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CNSMOD=1\r")) # tự động gửi thông tin khi chuyển mạng 3G, 4G,..
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CGPS.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CGPS=0,1\r")) # bật GPS
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CGPSHOT.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CGPSHOT\r")) # Bật GPS chế động nhanh.
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CGPSHOR.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CGPSHOR=5\r")) # Chỉnh sai số tối đa cho GPS( = 5 có nghĩa tối đa 5 mét)
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CGPSINFOCFG.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CGPSINFOCFG=3,3\r")) #yêu cầu module gửi bản tin GPS mỗi 3s một lần
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CSQ_WHAT.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CSQ\r")) # 
        elif(self.stepInit4Gmodule == Init4GmoduleStep.CSNMOD_WHAT.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CNSMOD?\r"))
        elif(self.stepInit4Gmodule == Init4GmoduleStep.SPN.value):
            self.uartObj.SendDataToUART(self.__characterToByte("AT+CSPN?\r")) # lấy tên nhà mạng.
        else:
            if((not self.__flagSimNotInserted)):
                # self.__timerRequestCNSandSPN.start(3000)
                if((not self.__flagQMIisRunning) & self.__processResponse.flagIs4Gor3G):
                    self.timerWaitFor4GmoduleReponse.stop()
                    self.__flagQMIisRunning = True
                    thread =threading.Thread(target = self.__runIniQMI, args = (), daemon = True)
                    thread.start()
            else:
                self.timerWaitFor4GmoduleReponse.stop()
                  
    def __runIniQMI(self):
        """chạy lệnh khởi tạo QMI
        """
        haveQmiDevice, spn = InitQmi.initQmi()
        # self.__networkAndConnectNotify.findQmiDevice(haveQmiDevice)
        self.__flagQMIisRunning = False
        self.__SignalShowSPN.emit(spn)
            
    def __characterToByte(self, StringData):
        ByteArray = []
        for item in StringData:
            ByteArray.append(ord(item))
        return ByteArray

    def __reinitQMI(self):
        if(not self.__flagSimNotInserted):
            self.SendInit()

    def Start4Gmodule(self):
        self.uartObj.UARTinit()
        self.uartObj.StartTimerReadUARTdata()
        self.__controlPowerObj.startSimPowerThread()

class Init4GmoduleStep(enum.Enum):
    CICCID = 3
    CGSN = 6
    AUTOCSQ = 8
    CSNMOD = 7
    CGPS = 0
    CGPSHOT = 1
    CSNMOD_WHAT = 5
    CSQ_WHAT = 4
    CGPSINFOCFG = 10
    CGPSHOR = 2
    SPN = 9
    Finish = 11