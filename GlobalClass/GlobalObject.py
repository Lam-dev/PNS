import random
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from Audio.AudioPlay import AudioPlay
from BuildSendAndProcessRecipt.BuildFrameSendToServer import BuildFrameSendToServer
from ControlPower.ControlPower import ControlPower
from DatabaseAccess.TableEntities import AnhLuu, PhienLaiXeRepo, ThongTinGiaoVien, ThongTinKhoaThi, PhienLaiXe, ThongTinThiSinh
from GetSettingFromJSON     import GetSetting, SaveSetting
from CryptData.CryptData    import  RC4
from datetime  import datetime
import pytz
from DatetimeConverter.DatetimeConverter  import  DatetimeConverter
import os
from GlobalClass.GlobalClass    import  DataGPS, DoWhatOvertimeNight
from DatabaseAccess.TableEntities   import  *
import threading
from GlobalClass.ConfigModel import ConfigModel
from HistoryScreen.CalculateTimeIn24h  import  CalculateTimeIn24h
from Logger.LogHelper import Logging
from LoginLogoutManager.TeacherLoginLogout import TeacherLoginLogout
from MainScreen.NetworkAndConnectNotify import NetworkAndConnectNotify
from MakeError.MakeError  import   MakeError
from FileHelper.FileHelper  import   FileHelper
from MainScreen.ControlTextNotification  import LockReason
from RFID.ControlRFmodule import ControlRFmodule

class GlobalObject(QObject):
    SignalGPIOisSet = pyqtSignal()
    SignalRFcardPowerReset = pyqtSignal()
    SignalFakeGPS = pyqtSignal(bool)
    SignalOnOffRFmodulePower = pyqtSignal(bool)
    SignalTimeUpdated = pyqtSignal(datetime)
    SignalConfigChange = pyqtSignal()
    SignalChangeShutdownIcon = pyqtSignal()
    SignalUserConfirmedLoginOrLogoutImage = pyqtSignal(bool, AnhLuu)
    SignalRequestConfirmLoginLogoutImage = pyqtSignal(object, int, object)
    SignalSendSampleImage = pyqtSignal(object)
    SignalContinueEndlessSession = pyqtSignal(PhienLaiXe, ThongTinThiSinh, ThongTinGiaoVien)
    SignalServerRequestLogout = pyqtSignal()
    SignalDownloadedIdentImage = pyqtSignal()
    SignalDeleteAteacher = pyqtSignal(ThongTinGiaoVien)
    SignalUnlockLogin = pyqtSignal()
    SignalNotifyRemainTimeAcceptNotUpToSTDcam = pyqtSignal(int)

    SignalScreenError = pyqtSignal()
    SignalEnableAndDisableLS = pyqtSignal(bool)
    SignalLSTOU = pyqtSignal()
    
    def __init__(self, mainScreen):
        from MainScreen.MainScreen  import MainScreenUI
        QObject.__init__(self)
        self.__gpioObj = None
        self.manualImeiSetting = GetSetting.GetImeiSet()
        self.loggingObj:Logging = None
        self.nowDateID = 0
        self.dateIsNew = False
        self.__rfObj:Optional[ControlRFmodule] = None
        self.currentLocation:Optional[DataGPS] = None
        self.student = None
        self.mainWindow:MainScreenUI = mainScreen
        self.fakeGPS:bool = False
        self.powerControl:Optional[ControlPower] = None
        self.fingerprintObj = None
        self.exchangeDataObj = None 
        self.sendRoadAdminObj = None
        self.networkAndConnectNotifyObj:Optional[NetworkAndConnectNotify] = None
        self.teacherLoginLogout:Optional[TeacherLoginLogout]
        self.buildFrameObj:Optional[BuildFrameSendToServer] = None
        self.isOnRFID = True
        self.isOn4G = True
        self.timeAtStartup = None
        self.timeUpdated = False
        self.imei:List[int] = self.__getImei()
        self.imeiStr = self.__getImeiStr()
        self.mac = self.__ConvertImeiToMacStr(self.imeiStr)
        self.currentStudent:Optional[ThongTinThiSinh] = None
        self.currentTeacher:Optional[ThongTinGiaoVien] = None
        self.listStudents:list[ThongTinThiSinh] = []
        self.listTeachers:list[ThongTinGiaoVien] = []
        self.soundObj:AudioPlay = AudioPlay()
        self.isSendingDataToServer = False
        self.autoShutdownIsEnabled = False
        self.carSpeed:float = 0
        self.waitingUserConfirmImage = False
        self.lockRFcard = False
        self.sessionEnoungh4hOr10h = False
        self.stopCountBecauseOutsizeTheTimeRunAtNight = False
        self.isNight = False
        self.ShowFaceRecResultCallBack:Optional[function] = None
        
        self.packFrameObj = None
        self.calculateTimeIn24h = CalculateTimeIn24h()
        self.databaseErrorNotifyIsShow = False
        self.checkHaveSendAllLocationMessageFunc = None
        self.addGPSlocationMessageForResendFunc = None
        self.confirmedLoginFace = False
        self.serverIP = ''
        self.serverPort = ''
        self.__ReadIPportFromConfigFile()
        
        self.cameraNotUpToStandard = False   #cờ chặn thông báo yêu cầu đăng nhập khi cam không đúng loại và hết thời gian cho phép. 
        self.thisCamNotUpToSTD = False       #= True khi gắn camera không đúng loại. Để check xem đã bắt đầu đếm ngược thòi gian cho phép chưa.
        self.numberHourAcceptNotUTSTDcam = 120
        self.dontAcceptNotUpToSTDcam = FileHelper.CheckExist("../Setting/DontAcceptCam.bin") | (not FileHelper.CheckExist("../Setting/FirstTimeCam.txt"))   # check đã hết thời gian cho phép sử dụng cam ko đúng hay chưa. 
        self.LSspk:bool = False
        self.LSrfc:bool = False
        self.LSscr:bool = False
        self.LS4G:bool = False

        self.LS_NG:bool = False  #Không bật module. Quay liên tục. 
        self.LS_DV:bool = False  # Định vị đỏ.
        self.LS_GP:bool = False  # không GPS
        self.LS_GT:bool = False  # chấm than
        self.LS_LS:bool = False  # không nhân sim
        self.LS_NMH:bool = False  # nháy màn hình.
        self.LS_TOU:bool = False  # không cảm ứng.
        self.LS_CAM:bool = False # không nhận cam.
        # self.currentSessionIsContinueFromEndlessSession = False   # biến xác định phiên hiện tại có phải nối phiên hay không để quyết định update thời gian đăng nhập khi có giờ chuẩn. 

        self.rc4 = RC4()
        self.rc4.SetStringKey("cT_Bhe^jiUAuf%Bk;Ko7")
        self.GetTimeAtStartup()
        self.actionSettings = GetSetting.GetActionSetting()
        self.config:ConfigModel = GetSetting.GetEncConfig()
        self.centerSettings = GetSetting.GetCenterSetting()
        self.GetFaceParam()
        self.makeError = MakeError(self)
        self.lockReasonCode = LockReason.Unknown
        self.lockLogin = self.config.lockLogin | self.centerSettings['dvLock']
        if(self.centerSettings['dvLock']):
            self.lockReasonCode = LockReason.CenterLock

    def __ConvertImeiToMacStr(self, stringImei):
        strMac = stringImei[2:4]+':'+stringImei[4:6]+':'+stringImei[6:8]+':'+stringImei[8:10]+':'+stringImei[10:12]+':'+stringImei[12:14]
        return strMac

    def UnsentSession(self):
        unsentSessionPercent = self.config.unsentSession
        if(unsentSessionPercent == 0):
            return False
        else:
            randomNumber = random.randint(0, 100)
            unsent = randomNumber <= unsentSessionPercent
            # print("Ket qua random : ", randomNumber, unsent)
            return unsent
        
    def __CheckTimeAcceptNotUpToStardardCamera(self):
        if(not FileHelper.CheckExist("../Setting/DontAcceptCam.bin")):
            if(FileHelper.CheckExist("../Setting/FirstTimeCam.txt")):
                haveFile, fileContent = FileHelper.ReadAllLines("../Setting/FirstTimeCam.txt")
                if(len(fileContent) != 1):
                    FileHelper.CreateFile("../Setting/DontAcceptCam.bin")
                    return
                firstTimeCam = DatetimeConverter.GetDatetimeFromString(fileContent[0], '%d/%m/%y %H:%M:%S')
                delta = DatetimeConverter.GetNow() - firstTimeCam
                self.numberHourAcceptNotUTSTDcam  = 120 - int(delta.total_seconds()/3600)
                if(self.numberHourAcceptNotUTSTDcam <= 0):
                    FileHelper.CreateFile("../Setting/DontAcceptCam.bin")
                else:
                    if(self.thisCamNotUpToSTD):
                        self.SignalNotifyRemainTimeAcceptNotUpToSTDcam.emit(False)
            else:

                if(self.thisCamNotUpToSTD):
                    nowStr = DatetimeConverter.GetDatetimeStringFromNow('%d/%m/%y %H:%M:%S')
                    FileHelper.WriteAllData("../Setting/FirstTimeCam.txt", nowStr)
                    self.SignalNotifyRemainTimeAcceptNotUpToSTDcam.emit(True)

    def __ReadIPportFromConfigFile(self):
        setting_dict  = GetSetting.LoadSettingFromFile()
        try:
            self.serverIP = setting_dict["serverIP"]
            self.serverPort = int(setting_dict["serverPort"])
        except:
            self.serverIP = "0.0.0.0"
            self.serverPort = 0

    # def LoadListCurrentStudentAndTeacher(self):
    #     self.listStudents = list(ThongTinThiSinhRepo().GetListAllColumn())
    #     self.listTeachers = list(ThongTinGiaoVienRepo().GetListAllColumn())

    def LoadListAllStudentAndTeacher(self):
        self.listStudents = list(ThongTinThiSinhRepo().GetList(["ID", "SoCMTND", "MaDK", "HoVaTen", "NgaySinh"]))
        self.listTeachers = list(ThongTinGiaoVienRepo().GetListAllColumn())
        pass

    def GetFaceParam(self):
        self.allowUsingRunningThresholdDaytime = self.config.doUseRunningThrhDaytime
        self.allowUsingRunningThresholdNight = self.config.doUseRunningThrhDayNight
        self.nightThreshold = self.config.nightThreshold  # Ngưỡng nhận diện ban đêm.
        self.runningNightThreshold = self.config.runningNightThreshold # Ngưỡng nhận diện ban đêm khi chạy
        self.rescueThreshold = 0.5   #self.personalSetting['rescueThreshold']   # chưa dùng chưa đọc
        self.allowRescue = False #self.personalSetting['allowRescue']
        self.threshold = self.config.faceRecThreshold  # ngưỡng nhận diện ban ngày
        self.runningThreshold = self.config.runningThreshold  # ngưỡng nhận diện ban ngày khi chạy.
        self.distanceScaleFactor = self.config.distaceScaleFactor/ 100
        self.compareWithLoginFace = self.config.compareWithLoginImage
        self.withLoginFaceRatio = self.config.loginImageRatio
        beginAndEndNightSplit = self.config.beginEndNightTime.split(',')
        self.beginEndNightTime = [int(beginAndEndNightSplit[0]), int(beginAndEndNightSplit[1])]
        self.doWhatOvertimeNight = DoWhatOvertimeNight(self.config.doWhatOvertimeNight)

    def SetCenterSetting(self, centerSetting):
        self.centerSettings = centerSetting
        self.__CheckLockLogin()

    def SetConfig(self, reciptedConfig:ConfigModel) -> None:
        self.config = reciptedConfig
        self.distanceScaleFactor = reciptedConfig.distaceScaleFactor / 100
        self.GetFaceParam()
        self.loggingObj.GetLogConfig(reciptedConfig)
        self.SignalConfigChange.emit()
        self.__CheckLockLogin()
    
    def __CheckLockLogin(self):
        if(self.lockLogin):
            self.lockLogin = self.config.lockLogin | self.centerSettings['dvLock']
            if(not self.lockLogin):
                self.SignalUnlockLogin.emit()
        else:
            self.lockLogin = self.config.lockLogin | self.centerSettings['dvLock']
        if(self.centerSettings['dvLock']):
            self.lockReasonCode = LockReason.CenterLock
        else:
            self.lockReasonCode = self.config.lockCode

    def FindStudentMatchRegisCodeStr(self, regisCodeStr):
        for _student in self.listStudents:
            if(_student.MaDK == regisCodeStr):
                return _student
        return None

    def FindStudentMatchID(self, ID):
        for _student in self.listStudents:
            if(_student.ID == ID):
                return _student
        return None

    def FindTeacherMatchID(self, ID):
        for _teacher in self.listTeachers:
            if(_teacher.ID == ID):
                return _teacher
        return None

    def FindTeacherMatchCode(self, teacherCode):
        for _teacher in self.listTeachers:
            if(_teacher.MaGV == teacherCode):
                return _teacher
        return None

    def GetTimeAtStartup(self):
        self.timeAtStartup = DatetimeConverter.GetNow()

    def UpdateTimeFromGPS(self, time, date):
        if(not self.timeUpdated):
            self.__CheckTimeAcceptNotUpToStardardCamera()
            datetimePreUpdate = DatetimeConverter.GetNow()
            os.system('date +%Y/%m/%d -s ' + '"%s"'%(date))
            os.system('date +%T -s ' +'"%s"'%(time))
            self.__TimeUpdated(datetimePreUpdate)
            self.timeUpdated = True
   
    def UpdateTime(self, timeString):
        if(not self.timeUpdated):
            self.__CheckTimeAcceptNotUpToStardardCamera()
            datetimePreUpdate = DatetimeConverter.GetNow()
            os.system('date ' + timeString)
            self.__TimeUpdated(datetimePreUpdate)
            self.timeUpdated = True

    def __TimeUpdated(self, datetimePreUpdate):
        """Thoi gian chuan da duoc cap nhat tu internet hoac GPS.
        Args:
            datetimePreUpdate (datetime): Thoi gian ngay truoc khi cap nhat thoi gian chuan
        """
        self.LoadListAllStudentAndTeacher()
        tz_HCM = pytz.timezone('Asia/Ho_Chi_Minh')
        currentTrueTime = datetime.now(tz_HCM)
        deltaTimeFromStartupToNow = datetimePreUpdate - self.timeAtStartup    # khoang thoi gian tu khi khoi dong thiet bi den khi cap nhat duoc thoi gian chuan
        trueTimeAtStartup = currentTrueTime - deltaTimeFromStartupToNow    #tru de tinh duoc thoi gian chuan khi khoi dong thiet bi
        self.SignalTimeUpdated.emit(trueTimeAtStartup)

    def enableOrDisableFakeGPS(self, enable):
        if(enable):
            self.SignalFakeGPS.emit(True)
        else:
            self.SignalFakeGPS.emit(False)

    def __getImeiStr(self) -> str:
        return bytes(self.imei).decode("utf-8")

    def __getImei(self) -> List[int]:
        """truoc khi lay duoc imei tu module sim. Doc imei da luu
        """
        imei = [0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30]
        if(self.manualImeiSetting["usingManualImei"]):
            imeiStr = self.manualImeiSetting["manualImei"]
            imei = list(imeiStr.encode('utf-8'))
        else:  
            imei = GetSetting.GetRealImei()
        return imei

    @property
    def rfObj(self):
        return self.__rfObj
    @rfObj.setter
    def rfObj(self, rfObj):
        self.__rfObj = rfObj
        self.__rfObj.SignalResetRFcardPower.connect(self.SignalRFcardPowerReset.emit)

    @property
    def gpioObj(self):
        return self.__gpioObj

    @gpioObj.setter
    def gpioObj(self, gpio):
        self.__gpioObj = gpio
        self.SignalGPIOisSet.emit()

    


    