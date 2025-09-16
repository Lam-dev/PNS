import time
from GlobalClass.GPIOdefine   import GPIOdefine
import threading
class ControlPowerPin:
    def __init__(self, GPIO):
        self.__gpioObj  = GPIO
        self.__setupOutputMode()
        self.__disableAll()

    def __setupOutputMode(self):
        # self.__gpioObj.setup(GPIOdefine.SimReset.value, self.__gpioObj.OUT)
        self.__gpioObj.setup(GPIOdefine.ModulePowerOn.value, self.__gpioObj.OUT)
        self.__gpioObj.setup(GPIOdefine.SimPowerOn.value, self.__gpioObj.OUT)

    def __disableAll(self):
        # self.__gpioObj.output(GPIOdefine.SimReset.value, self.__gpioObj.LOW)
        self.__gpioObj.output(GPIOdefine.ModulePowerOn.value, self.__gpioObj.LOW)
        self.__gpioObj.output(GPIOdefine.SimPowerOn.value, self.__gpioObj.LOW)

    def resetSimPowerPin(self):
        self.__gpioObj.output(GPIOdefine.SimPowerOn.value, self.__gpioObj.HIGH)
        time.sleep(0.3)
        self.__gpioObj.output(GPIOdefine.SimPowerOn.value, self.__gpioObj.LOW)

    def __startSimModulePowerPin(self):
        """điều khiển các chân ngùôn của module sim
        """
        self.__gpioObj.output(GPIOdefine.ModulePowerOn.value, self.__gpioObj.LOW) # kéo nguồn module xuống
        self.__gpioObj.output(GPIOdefine.SimPowerOn.value, self.__gpioObj.LOW)# #kéo nguồn sim xuống
        time.sleep(2) # chờ 2s
        self.__gpioObj.output(GPIOdefine.ModulePowerOn.value, self.__gpioObj.HIGH) # kéo nguồn module lên
        time.sleep(1) # chờ 1s
        self.__gpioObj.output(GPIOdefine.SimPowerOn.value, self.__gpioObj.HIGH) #kéo nguồn sim lên
        time.sleep(0.3) # chờ 0.3s
        self.__gpioObj.output(GPIOdefine.SimPowerOn.value, self.__gpioObj.LOW) # kéo nguồn sim xuông.

    def offSimModule(self):
        self.__disableAll()
        self.__gpioObj.isOn4G = False

    def __resetModule(self):
        """reset sim module
        """
        self.__disableAll()
        time.sleep(1.5)
        self.__startSimModulePowerPin()
        self.__gpioObj.isOn4G = False
        
    def resetModuleThread(self):
        thread = threading.Thread(target=self.__resetModule, args = (), daemon=True)
        thread.start()

    def startSimPowerThread(self):
        """Các bước điều khiển nguồn của module sim và sim
        """
        thread = threading.Thread(target=self.__startSimModulePowerPin, args= (), daemon= True)
        thread.start()
