class ConvertHelper:
    @staticmethod
    def Convert3bytesToHexString(dayMonthYear3bytes):
        result = ""
        for i in dayMonthYear3bytes:
            hexStr = '{:x}'.format(i)
            if(len(hexStr) == 1):
                result = f"{result}0{hexStr}"
            else:
                result = f"{result}{hexStr}"
        return result