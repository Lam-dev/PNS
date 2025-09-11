class ImeiSeriConverter:
    @staticmethod
    def GetImeiAndSeriString(imei):
        """lay imei va seri string

        Args:
            imei (byte[]): 15 byte imei.

        Returns:
            str, str: imei and seri
        """
        imeiStr = bytes(imei).decode("utf8")
        seriStr = ImeiSeriConverter.ConvertImeiToSeri(imei)
        return imeiStr, seriStr
        
    @staticmethod
    def ConvertImeiToSeri(imei):
        seri = ""
        imeiString = bytes(imei).decode("utf8")
        seri += ImeiSeriConverter.__ToHex8bit(int(imeiString[8:10], 16) ^ 69)
        seri += ImeiSeriConverter.__ToHex8bit(int(imeiString[10:12], 16) ^ 69)
        seri += ImeiSeriConverter.__ToHex8bit(int(imeiString[12:14], 16) ^ 69)
        return seri
        
    @staticmethod
    def __ToHex8bit(number):
        hexStr = hex(number)[2:]
        if(len(hexStr) == 1):
            return "0"+ hexStr
        else:
            return hexStr