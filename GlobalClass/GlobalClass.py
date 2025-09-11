from typing import List, Tuple
from dataclasses import dataclass
import enum
@dataclass
class DataGPS:
    lat:float
    long:float
    speed:float
    direction:int

class FaceRecScore:
    haveFace:bool = False
    haveSampled:bool = False
    withSampled:float = 1
    haveLoginFace:bool = False
    withLoginFace:float = 1
    haveIdentCardImage = False
    withIdentCardImage:float = 1         

class DefineWriteCardNotify():
    def __init__(self):
        self.waitCard = 1
        self.written = 2

class AddDataResult():
    def __init__(self):
        self.faceAdded = bool
        self.FGPadded = bool
        self.numberFGPadded = int
        self.cardWritten = bool

class Step(enum.Enum):
    Login = 0
    CountTime = 1
    StopAll = 2

class RequestFromTakeSample(enum.Enum):
    Reset = 1
    Shutdown = 2
    Restore = 3
    UpdateFW = 4
    DelAllTeacher = 5
    CheckVersion = 6

class CalDistanceMode(enum.Enum):
    GPS = 0
    Pulse = 1
    GPSandPulse = 2

#region enum cho log
class Warning(enum.Enum):
    NotRecFGP = 0
    NotDriver = 1
    DriverIncorect = 2
    LoginSuccess = 3

class ComputeDistanceMode(enum.Enum):
    GPS = 0
    Pulse = 1
    GPSandPulse = 2

class DeviceLogID(enum.Enum):
    SimModule = 0,
    Camera = 1
    RFcardModule = 2
    Screen = 3

class ConnectOrDisconnect(enum.Enum):
    Connect = 0
    Disconnect = 1

class LogConnectType(enum.Enum):
    Server = 0
    GPS = 1
    Internet = 2
    
class ShutdownType(enum.Enum):
    ByButton = 0
    AutoShutdown = 1
    AppError = 2
    PowerOff = 3

class TimeGetLog(enum.Enum):
    oneDayAgo = 0
    threeDayAgo = 3
    sevenDayAgo = 7
    twoWeekAgo = 14
    oneMonthAgo = 30

class LogID(enum.Enum):
    AppError = 0
    ConnectStatus = 1
    HardwareLog = 2
    AppException = 3
    Shutdown = 4

class NetwordMode(enum.Enum):
    Mode_No = 0
    Mode_2G = 1
    Mode_2G5= 2
    Mode_3G = 3
    Mode_4G = 4
    
class FaceRecResult(enum.Enum):
    FaceTrue = 0
    FaceFalse = 1
    NotFace = 2
    NotSample = 3
#endregion

class DataCode(enum.Enum):
    SendVersionInfo = 18
    ServerReciptedGPS = 1   # Code ban tin GPS
    RequestAddStudent = 2  # Them hoc vien
    RequestAddCourse = 3   # Them khoa hoc
    RequestAddFGP = 5      # them dac trung van tay 
    RequestAddFace = 6     # them dac trung khuon mat
    RequestAddTeacher = 17 # Them giao vien
    AddImage = 7           # them anh hoc vien
    StudentSyncData = 8    # Dong bo du lieu cua cac hoc vien khac
    ServerReciptedPhoto = 11        #Gui anh chup hoc vien len server
    DeleteStudentOrCourse = 14      # Xoa hoc vien hay khoa hoc
    SendCurrentGPS = 16             # Gui ban tin GPS hien tai khi van con dang gui du lieu GPS cu
    SendTripToServer = 19           #Gui phien hoc len server
    SendRequestShutdown = 20        #Server yeu cau tat thiet bi
    SendLog = 21                    #gui log file len server
    ChangeSetting = 13              #Cai dat tu xa
    ListCourseClass = 24
    ResentSession = 25
    SetUpdateServer = 26
    SetLicensePalateNum = 27
    DeleteAllData = 30
    ServerRequestAllSessionData = 31
    ServerSetSettingPassword = 32
    ServerRequestResendImage = 33
    LoggedInOnAnotherCar = 34
    ServerRequestLogout = 35
    ServerUpdateSettings = 36
    AppRequest = 37

class AppRequestCode(enum.Enum):
    ResendSession = 1
    ResendImage = 2
    DeleteCourse = 3
    DeleteTeacher = 4
    
    
class DialogType(enum.Enum):
    Warning = 0
    Question = 1
    Delete = 2

class DialogResult(enum.Enum):
    Yes = 0
    No = 1

class SettingCode(enum.Enum):
    Language = 0
    Brightness = 1
    NightMode = 2
    NumberPulseFor50m = 3
    ComputeDistanceMode = 4
    AutoShutdown = 5
    AutoShutdownTime = 6
    TimeGetSpeed = 7
    SpeedWrong = 8
    FaceRecCycleTime = 9
    NumberRecognize = 10
    FaceRecThreshold = 11
    TotalSample = 12
    Volume = 13
    ServerIplen = 14
    RoadAdminLink = 15

class DoWhatOvertimeNight(enum.Enum):
    Nothing = 0
    Warning = 1
    WarningAndStopCount = 2