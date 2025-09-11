from      typing import Optional, Tuple
from      PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from      GlobalClass.GlobalClass   import   DataGPS
import random
from datetime import datetime
import os


class GetLocation(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.__flagTimeUpdated = False
        self.__fakeGPS = False
        
    def setGlobalObj(self, globalObj):
        from GlobalClass.GlobalObject import GlobalObject
        self.__loggingObj = globalObj.loggingObj
        self.__globalObj = globalObj
        self.__globalObj.SignalFakeGPS.connect(self.FakeGPS)

    def FakeGPS(self, fake):
        #10.376197, 105.416466
        # self.preLat = 21.015636
        # self.preLong = 105.782955  20.917029,    20.916924, 105.564256  20.917023, 105.563396
        self.preLat = 20.917023
        self.preLong = 105.563396
        self.preSpeed = 0
        self.__fakeGPS = fake

    def analysGPRMC(self, GPRMCmessage:str) -> Tuple[bool, Optional[DataGPS]]:
        if(self.__fakeGPS):
            return self.__createRandomGPS()
        else:
            return self.__extractLoction(GPRMCmessage)

    def __createRandomGPS(self) -> Tuple[bool, Optional[DataGPS]]:
        randomLat = random.randint(10, 30)
        randomLong = random.randint(10, 30)
        addSubLat = random.randint(0, 1)
        addSubLong = random.randint(0, 1)
        speed = random.randint(0, 3)
        addSubSpeed = random.randint(0, 1)
        if(self.preSpeed <= 3):
            self.preSpeed += speed
        elif(self.preSpeed >= 150):
            self.preSpeed -= speed
        else:
            if(addSubSpeed == 0):
                self.preSpeed -= speed
            else:
                self.preSpeed += speed

        if(self.preLong <= 102.324656):
            self.preLong = round(self.preLong + randomLong / 1000000, 6)
        elif(self.preLong >= 107.213988):
            self.preLong = round(self.preLong - randomLong / 1000000, 6)
        else:
            if(addSubLong == 0):
                self.preLong = round(self.preLong - randomLong / 1000000, 6)
            else:
                self.preLong = round(self.preLong + randomLong / 1000000, 6)
            
        if(self.preLat <= 9.396655):
                self.preLat = round(self.preLat+ randomLat / 1000000, 6)
        elif(randomLat >= 22.991289):
            self.preLat = round(self.preLat - randomLat / 1000000, 6)
        else:
            if(addSubLat == 0):
                self.preLat = round(self.preLat - randomLat / 1000000, 6)
            else:
                self.preLat = round(self.preLat + randomLat / 1000000, 6)
                
        data = DataGPS(lat=self.preLat, long=self.preLong, speed=random.randint(40, 60), direction=random.randint(0, 359))
        return True, data

    def __extractLoction(self, gprmcMessage:str) -> Tuple[bool, Optional[DataGPS]]:
        try:
            lstDatasInGPS = gprmcMessage.split(',')
            if(lstDatasInGPS[2] == "A"):
                if(not self.__globalObj.timeUpdated):
                    self.__processTime(lstDatasInGPS[1], lstDatasInGPS[9])
                latLoc = round(self.__degreeMinute2degree(float(lstDatasInGPS[3])), 6)
                longloc = round(self.__degreeMinute2degree(float(lstDatasInGPS[5])), 6)
                speed = int(float(lstDatasInGPS[7])*1.85)
                data = DataGPS(lat=latLoc, long=longloc, speed=speed, direction=0)
                data.lat = latLoc
                data.long = longloc
                data.speed = speed
                if(len(lstDatasInGPS[8]) > 0):
                    directionTrueNorth = int(float(lstDatasInGPS[8]))
                else:
                    directionTrueNorth = 0
                if(directionTrueNorth >= 180):
                    data.direction = directionTrueNorth - 180
                else:
                    data.direction = directionTrueNorth + 180
                return True, data
            else:
                return False, None
        except:
            return False, None
    
    def __processTime(self, stringTime, stringDate):
        time = stringTime[0:2] + ':' + stringTime[2:4] + ':' + stringTime[4:6]
        date = str(2000 + int(stringDate[4:6])) + '/'+ stringDate[2:4] + '/' + stringDate[0:2]
        self.__globalObj.UpdateTimeFromGPS(time, date)
        # try:
            # os.system('date +%Y/%m/%d -s ' + '"%s"'%(date))
            # os.system('date +%T -s ' +'"%s"'%(time))
        # except Exception as ex:
        #     self.__loggingObj.AppException("__ProcessTime", str(ex))

        
    def __degreeMinute2degree(self, cordinate):
        deg = int(cordinate / 100)
        minute = cordinate % 100
        return float(deg) + float(minute) / 60