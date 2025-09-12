from dataclasses import dataclass, asdict
from pydantic import BaseModel

class ConfigModel(BaseModel):
    class Config:
        extra = "allow"
    crVer: int = 0
    directAddSample: bool = False
    loginByIDnumber: bool = False
    openTestScreen: bool = True
    openImeiSet: bool = False
    usingRealImei: bool = True
    manualSetFaceRecParam: bool = False
    faceRecThreshold: float = 0.45
    faceRecCycle: int = 10
    faceRecNumberTimeFalse: int = 30
    countDaTwhenFaceRecFalse: bool = True
    countDaTwhenFaceRecFalseNight: bool = True
    changeServerAddress: bool = True
    autoChangeCenterByCode: bool = True
    scName: str = "EcoTek"
    cenName: str = "EcoTek"
    logTemperature: bool = False
    logAppException: bool = False
    logWarning: bool = False
    logSendSessionToServer: bool = False
    distaceScaleFactor: int = 0
    send5pImage: bool = True
    courseExistanceTime: int = 360
    imagePeriodically: bool = False   #gửi ảnh theo chu kỳ. 
    imagePeriodicallyCycleTime: int = 240 # chu kỳ gửi ảnh (s)
    doUseRunningThrhDaytime: bool = False  # sử dụng 1 ngưỡng khác khi xe đang chạy ban ngày. 
    doUseRunningThrhDayNight: bool = False # sử dụng 1 ngưỡng khác khi xe đang chạy ban đêm
    runningThreshold: float = 0.48 # ngưỡng khi đang chạy. Ban ngày. 
    writeCardODvTeacher: bool = True # ghi thẻ tực tiếp giáo viên. 
    writeCardODvStudent: bool = True # ghi thẻ trực tiếp học viên. 
    getFGPoDv: bool = True # lấy vân tay trực tiếp. 
    getFFtODv: bool = True # lấy khuôn mặt trực tiếp. 
    allowDeteleAllData: bool = True
    pauseWhenDisconnectServer: bool = False # khi không có kết nối máy chủ quá 1 thời gian thì ko được chạy. 
    loginByName: bool = True # đăng nhập bằng tên
    deteleSortSession: bool = True # xoá những phiên ngắn < 300m
    usingPulse: bool = False # sử dụng tín hiệu xung.
    confirmInOutImage: bool = True # xác nhận ảnh đăng nhập, đăng xuất. 
    countTimeWhenStop: bool = True # tính thời gian khi xe dừng.
    nightModeStartTime: int = 17 # Thời gian bắt đầu chế độ ban đêm. 
    nightThreshold: float = 0.48 # ngưỡng ban đêm. 
    runningNightThreshold: float = 0.5 # ngưỡng khi chạy vào ban đêm.  
    lockLogin: bool = False  # khoá thiết bị. 
    compareWithLoginImage: bool = True # so sánh với đặc trưng của ảnh đăng nhập. để nhận diện. -> ảnh đăng nhập thường đúng.
    loginImageRatio: int = 30 # % tỉ lệ sử dụng ảnh đăng nhập. 
    doWhatOvertimeNight: int = 0 # làm gì khi quá thời gian ban đêm. 0:không làm gì, 1:thông báo, 2:Thông báo và dừng tính quãng đường. 
    beginEndNightTime: str = "18,23" # Thời gian bắt đầu và kết thúc chế độ đêm.
    numberHourNight: int = 10 # số giờ phải chạy ban đêm
    checkCamMode: int = 0
    LSenable: bool = False
    LSthreshold: int = 1000
    LSlist: str = ""
    WL: str = ""
    BL: str = ""
    lockCode: int = 0
    hotline: str = "0981.298.296"
    autoDeleteTrainer: bool = False
    autoDetectShapeMode: bool = False
    blockServerConnect: bool = False
    notifyAtStart: int = 0
    notiImgName: str = ""
    routeFileToCenterServer: bool = False
    unsentSession: int = False
    allowSessionStartBeforeNight: bool = True # khi 1 phiên bắt đầu chạy trước giờ ban đêm. Cắt lấy phần thời gian ban đêm để tính giờ. 
    showInputPhone:bool = False  # hiển thị màn hình yêu cập nhật sđt khi khởi động. 
    lockDvChangeImei:bool = False # khoá thiết bị khi phát hiện thay đổi imei. 

    showTrueVersion:bool = True
    versionShowOnMainScn:str = "8.5.5"

    showFaceRecProcess:bool = True # thanh nhỏ bên dưới khung camera.

    nonDaTmode:bool = False    #chế độ luôn bật cho GPS24
    allowHideInputPhone:bool = True
    detectInShape:bool = False  # xác định xe chạy trong hình hay đường trường.
    listShapeVer:int = 1  #phiên bản của danh sách sân. Khi phiên bản này khác với phiên bản trong danh sách sân thì sẽ kết nối server để tải ds sân mới. 
    numberTimeManualLogin:int = 0  # số lần cho phép đăng nhập bằng tên. 
    usingECCmodule:bool = True  # có cho phiép sử dụng ECC module ko.
    identFaceAuthen:bool = True  # lấy ảnh từ căn cước để nhận diện.

    allowRescue:bool = False
    rescueThreshold:float = 0.5
    loginOnlyGPSavailable:bool = False

    checkCabinLesson:bool = True
    cabinLessonPort:str = "8088"