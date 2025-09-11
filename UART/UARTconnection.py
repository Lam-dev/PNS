import serial
import time
import os
import threading
from      PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject



class UART(QObject):

    SignalReciptedData = pyqtSignal(bytes)
    
    def __init__(self, uartPort, uartSpeed, timeout = 0.5):
        super().__init__()
        self.timerReadUARTdata = QTimer(self)
        self.uartPort = uartPort
        self.uartSpeed = uartSpeed
        self.serObj = None
        self.timeout = timeout
        self.timerReadUARTdata.timeout.connect(self.ThreadReadUARTdata)
        self.UARTinit()

    def UARTinit(self):
        try:
            self.serObj = self.__UARTinit()
        except:
            pass

    def StartTimerReadUARTdata(self, cycleTime = None):
        if(cycleTime == None):
            self.timerReadUARTdata.start(500)
        else:
            self.timerReadUARTdata.start(cycleTime)

    def StopTimerReadUARTdata(self):
        self.timerReadUARTdata.stop()
        
    def Close(self):
        try:
            self.serObj.close()
        except:
            pass

    def __UARTinit(self):
        try:
            return serial.Serial(
            port= self.uartPort,
            baudrate = self.uartSpeed,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout= self.timeout,
            write_timeout=0.5)
        except Exception as ex:
            raise ex

    def ThreadListenUART(self):
        thread = threading.Thread(target=self.__UARTlisten, args=(), daemon= True)
        thread.start()

    def ThreadReadUARTdata(self):
        thread = threading.Thread(target=self.ReadUATRdataEmitSignal, args=(), daemon=True)
        thread.start()

    # def __UARTlisten(self):
    #     while True:
    #         self.serObj = self.__UARTinit()
    #         print("Khoi Tao uart")
    #         time.sleep(1)
    #         if(type(self.serObj)is not bool):
    #             while True:
    #                 try:
    #                     inWaiting = self.serObj.inWaiting()
    #                     print("inwaiting ="+self.inWaiting)
    #                     if(self.inWaiting > 0):
    #                         data = self.serObj.read_all()
    #                         print("Khung Nhan = ", data)
    #                         self.SignalReciptedData.emit(data)
    #                         pass
    #                 except:
    #                     pass
    
    def ReadUARTdataAndEmit(self):
        data = self.ReadUATRdata()
        if(data != b''):
            self.SignalReciptedData.emit(data)

    def ReadUATRdataEmitSignal(self):
        try:
            while True:
                if(self.serObj.inWaiting() > 0):
                    data = self.serObj.readline()
                    if(data == b''):
                        return
                    self.SignalReciptedData.emit(data)
                else:
                    return
        except Exception as ex:
            # print(ex)
            return b''

    def ReadUARTdataReturn(self):
        try:
            data = self.serObj.read(1024)
            return data
        except Exception as ex:
            # print(ex)
            return b''

    def SendDataToUART(self, frame):
        try:
            self.serObj.write(frame)
            return True
        except Exception as ex:
            return False
