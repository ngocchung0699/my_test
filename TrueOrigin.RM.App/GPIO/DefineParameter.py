from enum import Enum
from pickle import TRUE
from re import X

#Thông số của động cơ
class ParaStepMotor(Enum) :
    Model           = 'Nema 17'
    FrameSize       = [42, 42]#mm
    BodyLength      = 40    #mm
    ShaftDiameter   = 5     #mm
    ShaftLength     = 23    #mm
    DcutLength      = 21    #mm
    NumberOfLeads   = 4
    LeadLength      = 1000  #mm
    Weight          = 310   #g

    RatedCurrent    = 2     #A
    PhaseResistance = 1.1   #ohms
    Voltage         = 12    #Volts

    MicrostepResolution = 0.0625 #che do cua motor - vi buoc
    StepAngle       = 1.8   #deg
    MaxSpeed        = 20   #vong/phut

class ParaSensorMetal(Enum):
    Model           = 'LJ18A3-8-Z/BX'
    AppearanceType  = 'Thread cylindrical'
    Voltage         = 'DC 6-36V'
    CurrentOutput   = '300mA'
    OutputPolarity  = 'NPN NO(Normal Open)'
    DetectObject    = 'Magnetic metal'
    DiameterOfSensorColumn  = '18 mm'
    LengthOfSensorColumn    = '6.8 mm'
    DetectingDistance       = '8 mm'
    TotalLength     = '1.2 m/47 Inch'
    Protectionlevel = 'IP65'
    ExternalMaterial= 'Alloy(Nickel plated brass),Detection surface is ABS'
    WireType        = 'DC 3 Wires-Brown(positive electrode),Black(output signal), Blue(negative electrode)'

    PositiveLevel   = 0     #0=Low, 1=High - Mức tích cực của cảm biến
    TimeResponse    = 0.001 #s - thời gian đáp ung của sensor
    AntiJamming     = 3     #Tham số chống nhiễu cho sensor- Nếu nhận được tích cực của sensor bằng số AntiJamming liên tiếp mới tính là tích cực có giá trị
class ParaButton(Enum) :
    PositiveLevel   = 0     #0=Low, 1=High - Mức tích cực của cảm biến
    TimeResponse    = 0.001 #s - thời gian đáp ung của sensor
    AntiJamming     = 10     #Tham số chống nhiễu cho sensor- Nếu nhận được tích cực của sensor bằng số AntiJamming liên tiếp mới tính là tích cực có giá trị

class ParaStamp(Enum):
    Distance2Stamp      = 24.0  #mm - Khoảng cách giữa 2 tem
    WidthStamp          = 12.3  #mm - chiều rộng tem
    LengthStamp         = 32.4  #mm - chiều dài tem

class ParaMachine(Enum):
    NUM_SEAL_TRY        = 5
    COUNT_NEXT_STAMP    = 100
    INTERVAL_BAR        = 5
    COUNT_BAR_TO        = 5 * INTERVAL_BAR
    LANG_DEFAULT        = 'en'
    SYSTEM              = 'linux' # 'win32' or 'linux' 

    URL_SERVER          = "https://trueorigin.info/api/releaser1/"

    RUN_OFFLINE         = False  # máy chạy offline, ko có liên kết với server
    RELEASE_ORDER_EMULATOR  = [  # Dữ liệu offline cho máy
        {
            "id": 1,
            "id_user": 23,
            "name": "1",
            "id_batch": "15",
            "total_seri": 65535,
            "start_seri": 0,
            "current_seri": 0,
            "status": 0,
            "created_at": "2022-06-07 08:57:17",
            "updated_at": "2022-06-07 08:57:17",
            "id_production_batch": "2",
            "id_producer": "2",
            "id_product": "65538",
            "product_name": "Kiosk lấy số thứ tự - STD-T317W",
            "producer_name": "Công ty cổ phần công nghệ thông minh"
        },
        {
            "id": 2,
            "id_user": 23,
            "name": "1",
            "id_batch": "1",
            "total_seri": 500,
            "start_seri": 0,
            "current_seri": 0,
            "status": 0,
            "created_at": "2022-06-07 08:57:17",
            "updated_at": "2022-06-07 08:57:17",
            "id_production_batch": "1",
            "id_producer": "4354",
            "id_product": "1",
            "product_name": "THẦN TÀI MAY MẮN SBJ LOẠI 1.0 CHỈ",
            "producer_name": "Sacombank-SBJ"
        }
    ]

    # Ước tính khoảng thời gian động cơ chạy giữa 2 tem - Khác với thời gian check giữa 2 tem(thời gian check có tính cả quá trình ghi tem-full tiến trình)
    # Khoảng thời gian này sẽ phụ thuộc vào thông số của tem: khoảng cách 2 tem, chiều rộng của tem
    INTERVAL_2_STAMP    = (ParaStamp.Distance2Stamp.value + ParaStamp.WidthStamp.value)/60 # s - 
    OFFSET_SPEED_MOTOR  = 0.2   # % - Khoảng bù vận tốc mỗi khi Time interval khác với yêu cầu (Nếu Time nhanh thì giảm tốc -OFFSET, nếu Time chậm thì tăng tốc +OFFSET)
   
#Các biến tính toán
class ParaCalculation():
    MAX_SPEED_MOTOR     = 25    # Tốc độ tối đa của động cơ
    MIN_SPEED_MOTOR     = 3     # Tốc độ tối thiểu của động cơ

    TDetectStamp        = 0     # Biến lưu thời điểm bắt đầu phát hiện được tem (Phát hiện bằng cảm biến kim loại)

    DeltaTime           = 0     # Chênh lệch giữa 2 lần IntervalStamp liên tiếp
