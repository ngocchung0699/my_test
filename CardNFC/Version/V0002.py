'''
Sử dụng tem Version 2:
1. v2 có sự thay đổi lớn về kích thước của giữ liệu (số byte Quick giảm từ 32 -> 12) so với v1, điều này dẫn đến việc vị trí các byte trong thẻ cũng bị thay đổi theo -> tiết kiệm được không gian free của tem
2. Mật khẩu của v2 là mật khẩu riêng phần, nghĩa là mỗi tem sẽ có 1 mật khẩu riêng không giống nhau, điều đó là cần thiết vì nếu như 1 tem bị lộ mk thì các tem khác vẫn an toàn
'''