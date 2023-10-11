from enum import Enum


class PIDMode(Enum):
    MANUAL      =   0
    AUTOMATIC   =   1

class PIDDirection(Enum):
    DIRECT      =   0
    REVERSE     =   1

class PIDControl:
    # Đầu vào Bộ điều khiển PID 
    input:float
    
    # Đầu vào trước đó cho Bộ điều khiển PID
    lastInput:float

    # Đầu ra của Bộ điều khiển PID
    output:float
     
    # Nhận các giá trị không đổi do người dùng chuyển
    # Đây là những mục đích hiển thị
    dispKp:float
    dispKi:float
    dispKd:float
    
    # Nhận các giá trị không đổi mà bộ điều khiển thay đổi để sử dụng riêng
    alteredKp:float
    alteredKi:float
    alteredKd:float
    
    # Điều khoản tích hợp
    iTerm:float
    
    # Khoảng thời gian (tính bằng giây) mà bộ điều khiển PID sẽ được gọi
    sampleTime:float
    
    # Các giá trị mà đầu ra sẽ bị hạn chế
    outMin:float
    outMax:float
    
    # Người dùng đã chọn điểm hoạt động
    setpoint:float
    
    # Ý thức về hướng của bộ điều khiển
    # DIRECT: Điểm đặt dương cho đầu ra dương
    # REVERSE: Điểm đặt dương cho đầu ra âm
    controllerDirection:PIDDirection
    
    # Cho biết bộ điều khiển sẽ phản hồi như thế nào nếu người dùng đã tiếp quản điều khiển thủ công hay không
    # MANUAL:   Bộ điều khiển PID đang tắt.
    # AUTOMATIC:  Bộ điều khiển PID đang bật
    mode:PIDMode