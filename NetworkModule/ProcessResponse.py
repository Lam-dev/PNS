from typing import Optional
from PyQt5.QtCore import QObject
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from GlobalClass.GlobalClass import DataGPS
from NetworkModule.GetLocationFromGPRMC   import  GetLocation
import os

class ProcessResponse(QObject):
    SignalMac = pyqtSignal(str)
    SignalImei = pyqtSignal(list)
    SignalNotSim = pyqtSignal()
    SignalNextStep = pyqtSignal()
    SignalSendInit = pyqtSignal()
    SignalGPSdata = pyqtSignal(DataGPS)
    SignalGPSinvalid = pyqtSignal()
    SignalHaveSim = pyqtSignal()
    SignalUnplugSim = pyqtSignal()
    SignalHaveNoGPSmessage = pyqtSignal()   #khong nhan dc ban tin GPS

    def __init__(self):
        QObject.__init__(self)
        self.flagIs4Gor3G = False
        self.__getLocationFromGPRMC = GetLocation()
        self.timerTestNetworkNotify = QTimer(self)
        self.__flagReciptedGPSmessage = False
        self.flagRecitedGPRMC = False   # chắc chắn đã nhận được bản tin GPS
        self.__timerCheckReciptedGPSmessage = QTimer()
        self.__timerCheckReciptedGPSmessage.timeout.connect(self.__CheckReciptedGPSmessage)
        self.__timerCheckReciptedGPSmessage.start(90000)
        self.__timerFakeGPS = QTimer(self)
        self.__timerFakeGPS.timeout.connect(lambda:self.processResponseData("GPRMC".encode("utf-8")))
        self.__flagSimNotInserted = False
        
        # self.__runOnDevice = os.uname()[2].__contains__("sunxi")
        
        # self.timerTestNetworkNotify.timeout.connect(self.testNetworkNotify)
        # self.timerTestNetworkNotify.start(7000)
        # self.stepShow = 0

    # def testNetworkNotify(self):
    #     if(self.stepShow == 0):
    #         self.__networkAndConnectNotify.changeIntensity(3)
    #     elif(self.stepShow == 1):
    #         self.__networkAndConnectNotify.showSPN("VNM")
            
    #     elif(self.stepShow == 2):
    #         self.__networkAndConnectNotify.showNetworkMode("4G")
    #     elif(self.stepShow == 3):
    #         self.SignalNotSim.emit()
    #         self.timerTestNetworkNotify.stop()
    #     self.stepShow += 1
    
    # def resetSim(self):
    #     self.stepShow = 0
    #     self.timerTestNetworkNotify.start(7000)


    def __fakeGPS(self, fake):
        if(fake):
            self.__timerFakeGPS.start(1000)
        else:
            self.__timerFakeGPS.stop()

    def __CheckReciptedGPSmessage(self):
        if(not self.__flagReciptedGPSmessage):
            self.SignalHaveNoGPSmessage.emit()
            self.__networkAndConnectNotify.gpsErr()
        self.__flagReciptedGPSmessage = False

    def processResponseData(self, data):
        """xử lý dữ liệu nhận từ module 4G
        Args:
            data ([bytes]): [dữ liệu nhận]
        """
        stringMessage = self.__byteToCharacter(data)
        # if(self.__runOnDevice):
        #     print(stringMessage)
        if(stringMessage.__contains__("GPRMC")):
            if(self.__globalObj.LS_DV):
                return
            self.flagRecitedGPRMC = True
            self.__flagReciptedGPSmessage = True
            _valid, gpsData = self.__getLocationFromGPRMC.analysGPRMC(stringMessage)
            if(_valid & (not self.__globalObj.LS_GP)):
                self.SignalGPSdata.emit(gpsData)
                self.__networkAndConnectNotify.gpsStt(True)
            else:
                self.__networkAndConnectNotify.gpsStt(False)
                self.SignalGPSinvalid.emit()

        elif((stringMessage.__len__() == 17) & (stringMessage[0:15].isdecimal())):
            self.__convertImeiToListByte(stringMessage)
            self.__convertImeiToMacStr(stringMessage)

        elif(stringMessage.__contains__("+CSQ:")):
            self.__SQchange(stringMessage)

        elif(stringMessage.__contains__("+CNSMOD:")):
            self.__analysCNSMode(stringMessage)
            
        elif(stringMessage.__contains__("PB DONE")):
            if(self.__globalObj.LS_LS):
                self.__error("inserted")
                return
            self.SignalSendInit.emit()

        elif(stringMessage.__contains__("CSPN:")):
            self.__reciptSPN(stringMessage)

        elif(stringMessage.__contains__("ERROR") | stringMessage.__contains__("not inserted")):
            self.__error(stringMessage)
        
        elif(stringMessage.__contains__("+ICCID:")):
            self.__flagSimNotInserted = False
            self.SignalHaveSim.emit()   # co lay dc sim number => co sim

        elif(stringMessage.__contains__("OK")):
            self.SignalNextStep.emit()
            self.SignalSendInit.emit()

        elif(stringMessage.__contains__("+SIMCARD: NOT")):
            self.SignalUnplugSim.emit()
            self.__networkAndConnectNotify.noSim()
            self.__flagSimNotInserted = True

    def __error(self, messageErr):
        if(messageErr.__contains__("inserted")):
            self.__networkAndConnectNotify.noSim()
            self.SignalNotSim.emit()
            self.__flagSimNotInserted = True
    
    def __byteToCharacter(self, ByteArray):
        StringData = ""
        for item in ByteArray:
            StringData += chr(item)
        return StringData

    def __SQchange(self, stringCSQ):
        if(self.__flagSimNotInserted):
            return
        rssiAndBer = stringCSQ.split(':')[1]
        rssi = rssiAndBer.split(',')[0]
        rssiNumber = int(rssi)
        if((rssiNumber > 24) & (rssiNumber <= 30)):
            self.__networkAndConnectNotify.changeIntensity(4)
        elif((rssiNumber > 18) & (rssiNumber <= 24)):
            self.__networkAndConnectNotify.changeIntensity(3)
        elif((rssiNumber > 10) & (rssiNumber <= 18)):
            self.__networkAndConnectNotify.changeIntensity(2)
        elif((rssiNumber >= 0) & (rssiNumber <= 10)):
            self.__networkAndConnectNotify.changeIntensity(1)
        else:
            self.__networkAndConnectNotify.changeIntensity(0)

    def __reciptSPN(self, message):
        try:
            print(message)
            spnAndDisplayMode = message.split(":")[1]
            spn = spnAndDisplayMode.split(",")[0]
            spn = spn.replace('"', '')
            self.__networkAndConnectNotify.showSPN(spn)
        except Exception as ex:
            print("__reciptSPN", ex)

    def __analysCNSMode(self, message):
        try:
            rightPart = message.split(':')[1]
            if(rightPart.__contains__(',')):
                status = int(rightPart.split(',')[1])
            else:
                status = int(rightPart)
        except:
            status = 0
        if(status == 0):
            self.flagIs4Gor3G = False
            self.__networkAndConnectNotify.showNetworkMode('?')

        elif(status == 1):
            self.flagIs4Gor3G = False
            self.__networkAndConnectNotify.showNetworkMode('2G')

        elif((status == 2) | (status == 3)):
            self.flagIs4Gor3G = True
            self.__networkAndConnectNotify.showNetworkMode("2.5G")

        elif((status == 4) | (status == 5) | (status == 6) | (status == 7)):
            self.flagIs4Gor3G = True
            self.__networkAndConnectNotify.showNetworkMode("3G")
            
        elif((status == 8)):
            self.flagIs4Gor3G = True
            self.__networkAndConnectNotify.showNetworkMode("4G")   

    def __convertImeiToListByte(self, stringImei):
        lstByte = []
        for i in stringImei:
            lstByte.append(ord(i))
        self.SignalImei.emit(lstByte[0:15])

    def __convertImeiToMacStr(self, stringImei):
        strMac = stringImei[2:4]+':'+stringImei[4:6]+':'+stringImei[6:8]+':'+stringImei[8:10]+':'+stringImei[10:12]+':'+stringImei[12:14]
        self.SignalMac.emit(strMac)
