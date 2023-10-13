class Define_V0000():
    Size_ID = 16  #bytes
    Size_Sign = 32  #bytes
    Size_Quickcode = 32  #bytes

    StartPage_ID = 8  #vị trí page đầu tiên của ID
    StartPage_Sign = 10  #vị trí page đầu tiên của Sign
    StartPage_Quickcode = 18  #vị trí page đầu tiên của Quickcode
    
class Define_V0001():
    Size_ID = 8  #bytes
    Size_Sign = 32  #bytes
    Size_Quickcode = 32  #bytes = 8bytes Quick + 4bytes Count (số dếm để biết số lần check)

    StartPage_ID = 4  #vị trí page đầu tiên của ID

    StartPage_Sign_Pack1 = 6  #vị trí page đầu tiên của Sign
    StartPage_Quickcode_Pack1 = 14  #vị trí page đầu tiên của Quickcode

    StartPage_Sign_Pack2 = 22  #vị trí page đầu tiên của Sign - Lưu Sign dự phòng
    StartPage_Quickcode_Pack2 = 30  #vị trí page đầu tiên của Quickcode- lưu Quickcode dự phòng

class Define_V0002():
    Size_ID = 8  #bytes
    Size_Sign = 32  #bytes
    Size_Quickcode = 12  #bytes = 8bytes Quick + 4bytes Count (số dếm để biết số lần check)

    StartPage_ID = 4  #vị trí page đầu tiên của ID

    StartPage_Sign_Pack1 = 6  #vị trí page đầu tiên của Sign
    StartPage_Quickcode_Pack1 = 14  #vị trí page đầu tiên của Quickcode

    StartPage_Sign_Pack2 = 17  #vị trí page đầu tiên của Sign - Lưu Sign dự phòng
    StartPage_Quickcode_Pack2 = 25  #vị trí page đầu tiên của Quickcode- lưu Quickcode dự phòng

class Define_V0003():
    Size_ID = 8  #bytes
    Size_Sign = 32  #bytes
    Size_Quickcode = 12  #bytes = 8bytes Quick + 4bytes Count (số dếm để biết số lần check)

    StartPage_ID = 4  #vị trí page đầu tiên của ID

    StartPage_Sign_Pack1 = 6  #vị trí page đầu tiên của Sign
    StartPage_Quickcode_Pack1 = 14  #vị trí page đầu tiên của Quickcode

    StartPage_Sign_Pack2 = 17  #vị trí page đầu tiên của Sign - Lưu Sign dự phòng
    StartPage_Quickcode_Pack2 = 25  #vị trí page đầu tiên của Quickcode- lưu Quickcode dự phòng

class Define_V1001():
    Size_Url = 40  #bytes
    Size_ID = 8  #bytes
    Size_Sign = 32  #bytes
    Size_Quickcode = 12  #bytes = 8bytes Quick + 4bytes Count (số dếm để biết số lần check)

    StartPage_Url = 4  #vị trí page đầu tiên của url 

    StartPage_ID = 14  #vị trí page đầu tiên của ID

    StartPage_Sign_Pack1 = 16  #vị trí page đầu tiên của Sign
    StartPage_Quickcode_Pack1 = 24  #vị trí page đầu tiên của Quickcode

    StartPage_Sign_Pack2 = 27  #vị trí page đầu tiên của Sign - Lưu Sign dự phòng
    StartPage_Quickcode_Pack2 = 35  #vị trí page đầu tiên của Quickcode- lưu Quickcode dự phòng

class Define_Ver():
    PAGE_HASH = 38 #page lưu version
    PAGE_VERSION = 39 #page lưu version