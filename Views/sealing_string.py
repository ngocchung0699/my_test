class Sealing_string:
    statusRO = ["Sẵn sàng", "Đang phát hành", "Hoàn thành", "Tạm dừng", "Dừng", "Đang chờ"]
    statusBar = {
            "INIT":"  Lựa chọn lệnh phát hành",
            "ACTION":"  Đang hoạt động",
            "UPDATE":"  Đã cập nhật",
            "EXPORT":"  Đã xuất báo cáo",
            "CHANGE_RO":"  Đã gửi yêu cầu, Chờ phê duyệt",
            "ERROR_SERVER":"  Kết nối server thất bại",
            "ERROR_NFC":"  Lỗi NFC, Hệ thống dừng hoạt động",
            "PAUSE":"  Máy đang tạm dừng",
            "READY":"  Sẵn sàng hoạt động",
        }
    
    message_login = {
            "INIT":"",
            "LOGIN_FAIL":"Tài khoản hoặc mật khẩu sai, Đăng nhập thất bại!",
            "ERROR_SERVER":"Lỗi kết nối tới server. Đăng nhập thất bại",
            "APPROVALED":"Phê duyệt thành công",
            "LOGIN_SUCCESS":"Đăng nhập thành công, Chờ phê duyệt của quản lý"
        }

    progress_fn = {
            "INIT":"Đang phát hành",
            "PAUSE_PUSH":"Phát hiện tem thành công",
            "TRY_COUNT":"Phát hành thất bại, Đang thử lại",
            "ALARM_STOPSS":"Phát hành thất bại, Hãy kiểm tra lại tem",
        }

    btn_select = {
            "INIT_RO_SELECT":"Lệnh đang thực hiện: ID ",
            "PRODUCER":"Tên nhà sản xuất: ",
            "PRODUCT":"Tên sản phẩm: ",
            "PRODUCE_ID":"Mã sản phẩm: ",
            "PRODUCTION_ID":"ID lệnh phát hành: ",
            "TOTAL_SERI":"Tổng số seri: ",
            "START_SERI":"Số seri bắt đầu: ",
            "CURRENT_SERI":"Số hiện tại: ",
            "STATUS":"Trạng thái: ",
        }