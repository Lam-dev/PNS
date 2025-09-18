
import os
import shlex
import subprocess
from threading import Timer, Thread
import time
class ProcessManagement:
    __concentratordSP:subprocess.Popen
    __MQTTforwarderSP:subprocess.Popen
    __concentratordCommand:str = "sudo ./Concentratord/chirpstack-concentratord-sx1302 -c config.toml"
    __MQTTforwarderCommand:str = "sudo ./MQTTforwarder/chirpstack-mqtt-forwarder -c config.toml"
    __timerCheckProcessIsRun:Timer

    def __init__(self):
        self.__timerCheckProcessIsRun = Timer(interval=30,  function=self.__CheckProcessIsLive)
        if(os.uname()[2].__contains__("sunxi")):
            self.__StartConcentratordAndForwarder()
            
            self.__timerCheckProcessIsRun.start()
        
    def __StartConcentratordAndForwarder(self):
        Thread(target=self.__RunConcentratord, args=(), daemon=False).start()
        time.sleep(10)
        Thread(target=self.__RunMQTTforwarder, args=(), daemon=False).start()


    def __CheckProcessIsLive(self):
        concentratordRet = self.__concentratordSP.poll()
        if(concentratordRet is not None):
            pass
        
        mqttForwarderRet = self.__MQTTforwarderSP.poll()
        if(mqttForwarderRet is not None):
            pass

    def __RunConcentratord(self):
        print("chay process concentrator")
        os.system(self.__concentratordCommand)
        # self.__concentratordSP = subprocess.Popen(shlex.split(self.__concentratordCommand), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)
        print("chay xong process concentrator")

    def __RunMQTTforwarder(self):
        print("chay process MQTTforwarder")
        os.system(self.__MQTTforwarderCommand)
        # self.__MQTTforwarderSP = subprocess.Popen(shlex.split(self.__MQTTforwarderCommand), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)
        print("chay xong process MQTTforwarder")
    