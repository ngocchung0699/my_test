'''
Sử dụng tem Version 3:
1. Các vị trí lưu giữ liệu (ID, Sign, Quick, ReSign, ReQuick) vẫn giữ nguyên vị trí và số lượng byte như version 2
2. Thay đổi: v3 sẽ có thêm Hash ở page 38 nhằm mục đích định danh tem, mỗi tem chỉ tồn tại duy nhất 1 mã hash định danh chính nó -> nếu copy giữ liệu sang tem khác sẽ bị phát hiện -> báo tem giả luôn
'''