import os
import glob
import subprocess
import shlex
class InitQmi:

    # @staticmethod
    # def initQmi():
    #     """khoi tao ket noi qmi
    #     """
    #     cdcFile = InitQmi.findCdcFileName()
    #     providerName = InitQmi.GetHomeNetworkProvider(cdcFile)
    #     cmdPart1 = "sudo qmicli -d %s --dms-set-operating-mode='online'\nqmicli -d %s --dms-get-operating-mode\nqmicli -d %s --nas-get-signal-strength\nqmicli -d %s --nas-get-home-network"%(cdcFile, cdcFile, cdcFile, cdcFile)
    #     os.system(cmdPart1)
    #     QmiFolderName = InitQmi.findQmiFolderName()
    #     if(QmiFolderName != None):
    #         cmdPart2 = "sudo ip link set %s down\necho 'Y' | sudo tee /sys/class/net/%s/qmi/raw_ip\nsudo ip link set %s up\nqmicli -p -d %s --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network='apn='m3-world',username='mms',password='mms',ip-type=4' --client-no-release-cid\nsudo udhcpc -i %s -n\nip r s"%(QmiFolderName, QmiFolderName, QmiFolderName, cdcFile, QmiFolderName)
    #         os.system(cmdPart2)
    #     # self.__flagInit4GmoduleFinish = True
    #     # providerName = InitQmi.GetHomeNetworkProvider(cdcFile)
    #     return providerName

    @staticmethod
    def initQmi():
        """khoi tao ket noi qmi
        """
        cdcFile = InitQmi.findCdcFileName()
        if(cdcFile == None):
            return False, ""
        providerName = InitQmi.GetHomeNetworkProvider(cdcFile)
        apn, user, password = InitQmi.GetAPN(providerName)
        cmdPart1 = "sudo qmicli -d %s --dms-set-operating-mode='online'\nqmicli -d %s --dms-get-operating-mode\nqmicli -d %s --nas-get-signal-strength\nqmicli -d %s --nas-get-home-network"%(cdcFile, cdcFile, cdcFile, cdcFile)
        os.system(cmdPart1)
        QmiFolderName = InitQmi.findQmiFolderName()
        if(QmiFolderName != None):
            cmdPart2 = f"sudo ip link set {QmiFolderName} down\necho 'Y' | sudo tee /sys/class/net/{QmiFolderName}/qmi/raw_ip\nsudo ip link set {QmiFolderName} up\nqmicli -p -d {cdcFile} --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network='apn='{apn}',username='{user}',password='{password}',ip-type=4' --client-no-release-cid\nsudo udhcpc -i {QmiFolderName} -n\nip r s"
            os.system(cmdPart2)
        return True, providerName

    @staticmethod
    def GetAPN(spn):
        spn = spn.upper()
        if(spn.__contains__("MOBIFONE")):
            return "m-wap", "mms", "mms"
        else:
            return "m3-world", "mms", "mms"

    @staticmethod
    def GetHomeNetworkProvider(cdcFile):
        try:
            command = shlex.split(f'sudo qmicli -d {cdcFile} --nas-get-home-network')
            output = subprocess.check_output(command)
            for line in output.splitlines():
                strLine = line.decode('utf-8')
                if(strLine.__contains__("Description")):
                    providerName = strLine.split(':')[1]
                    providerName = providerName[2:(len(providerName) - 1)]
                    return providerName
            return ""
        except Exception as ex:
            print(ex)
            return ""

    @staticmethod
    def findCdcFileName():
        lstCdcFile = glob.glob("/dev/cdc-wdm*")
        # if(len(lstCdcFile) == 0):
        #     return "/dev/cdc-wdm0"
        # else:
        if(len(lstCdcFile) > 0):
            return lstCdcFile[0]
        else:
            return None
            
    @staticmethod
    def findQmiFolderName():
        listDir = os.listdir("/sys/class/net/")
        for dir in listDir:
            if(dir.__contains__("ww")):
                return dir
        return None

    # def FindCdcFileName(self):
    #     lstCdcFile = glob.glob("/dev/cdc-wdm*")
    #     if(len(lstCdcFile) == 0):
    #         return "/dev/cdc-wdm0"
    #     else:
    #         return lstCdcFile[0]

    # def FindQmiFolderName(self):
    #     listDir = os.listdir("/sys/class/net/")
    #     for dir in listDir:
    #         if(dir.__contains__("ww")):
    #             return dir
    #     return None
