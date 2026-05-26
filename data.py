import random
import json
import os
import sys
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Đường dẫn file lưu câu tùy chỉnh
CUSTOM_SENTENCES_FILE = resource_path("custom_sentences.json")
EXTRA_WORDS_FILE = resource_path("extra_words.json")

VIETNAMESE_WORDS = [
    "người", "đi", "học", "làm", "nhà", "con", "cái", "có", "không", "và", "một", "những", "được", "trong", "cho", "đến", 
    "với", "từ", "khi", "viễn", "thông", "linh", "kiện", "mạch", "điện", "tín", "hiệu", "vi", "mạch", "điện", "trở", "tụ", 
    "điện", "mạng", "lưới", "anten", "thuật", "toán", "dữ", "liệu", "phần", "mềm", "ứng", "dụng", "biến", "số", "hàm", 
    "số", "lập", "trình", "hệ", "thống", "máy", "chủ", "bóng", "đá", "trọng", "tài", "bàn", "thắng", "tấn", "công", 
    "phòng", "ngự", "tiền", "đạo", "thủ", "môn", "ngoằn", "ngoèo", "khuỷu", "tay", "thuở", "ấy", "rượi", "bưởi", "nhễ", 
    "nhại", "lững", "lờ", "thiên", "nhiên", "hòa", "bình", "giáo", "dục", "sáng", "tạo", "thực", "tế", "thành", "công", 
    "rực", "rỡ", "mênh", "mông", "sản", "xuất", "xuất", "sắc", "lỏng", "lẻo", "nơm", "nớp", "truyền", "thống", "chương", 
    "trình", "khuyến", "khích", "tương", "lai", "gia", "đình", "công", "nghệ", "tri", "thức", "hạnh", "phúc", "xử", 
    "lý", "giao", "diện", "máy", "tính", "bàn", "phím", "tốc", "độ", "trò", "chơi", "điện", "tử", "trực", "tuyến", 
    "kết", "nối", "thông", "tin", "phát", "triển", "cơ", "sở", "hạ", "tầng", "thiết", "kế", "kỹ", "thuật", "phân", 
    "tích", "logic", "vận", "hành", "thông", "minh", "linh", "hoạt", "hiệu", "quả", "chính", "xác", "bền", "bỉ", 
    "thời", "gian", "không", "gian", "vũ", "trụ", "khám", "phá", "trải", "nghiệm", "tuyệt", "vời", "nỗ", "lực", 
    "kiên", "trì", "đam", "mê", "khát", "vọng", "tự", "do", "quốc", "gia", "thực", "hành", "kiểm", "tra", "kết", 
    "quả", "đồng", "bộ", "tối", "ưu", "tự", "động", "hoàn", "thiện", "rèn", "luyện", "kiên", "định", "mục", "tiêu", 
    "ý", "tưởng", "giải", "pháp", "đóng", "góp", "cống", "hiến", "giá", "trị", "bền", "vững", "lan", "tỏa", "cảm", 
    "hứng", "vui", "vẻ", "nhiệt", "huyết", "tập", "trung", "bình", "tĩnh", "tự", "tin", "quyết", "đoán", "chân", 
    "thành", "tử", "tế", "thân", "thiện", "đoàn", "kết", "gắn", "bó", "chia", "sẻ", "thấu", "hiểu", "trân", "trọng", 
    "biết", "ơn", "khiêm", "tốn", "học", "hỏi", "tiến", "bộ", "không", "ngừng", "mây", "gió", "nắng", "mưa", "sông", 
    "suối", "núi", "rừng", "hoa", "cỏ", "lá", "cành", "biển", "đảo", "cát", "đá", "bão", "tuyết", "lửa", "đất", 
    "mèo", "chó", "gà", "vịt", "bò", "lợn", "chim", "cá", "hổ", "báo", "hươu", "nai", "thỏ", "rùa", "rắn", "ếch", 
    "ong", "bướm", "kiến", "sâu", "bàn", "ghế", "giường", "tủ", "bát", "đũa", "cốc", "chén", "áo", "quần", "mũ", 
    "giày", "bút", "thước", "sách", "vở", "cửa", "tường", "gạch", "ngói", "đỏ", "cam", "vàng", "lục", "lam", 
    "chàm", "tím", "trắng", "đen", "xám", "nâu", "hồng", "bạc", "son", "thắm", "chạy", "nhảy", "đứng", "ngồi", 
    "ăn", "uống", "ngủ", "nghỉ", "nhanh", "chậm", "cao", "thấp", "dài", "ngắn", "to", "nhỏ", "nóng", "lạnh", 
    "vui", "buồn", "ngoằn", "ngoèo", "khuỷu", "oằn", "xoáy", "loay", "hoay", "rượi", "bưởi", "nhuyễn", "quỵt", 
    "huýt", "suýt", "tuyệt", "truyền", "luyện", "chuối", "nhuần", "rực", "rỡ", "lẫm", "liệt", "nhễ", "nhại", 
    "hủ", "tiếu", "lững", "lờ", "sừng", "sững", "bỡ", "ngỡ", "hẫng", "hụt", "chênh", "vênh", "lảo", "đảo", 
    "nghễu", "nghện", "khệnh", "khạng", "mặn", "ngọt", "chua", "cay", "đắng", "chát", "nồng", "gắt", "thơm", 
    "thối", "hôi", "tanh", "tròn", "vuông", "méo", "thẳng", "cong", "lệch", "phẳng", "nhám", "nhẵn", "mềm", 
    "cứng", "dẻo", "dai", "giòn", "xốp", "mỏng", "dày", "rộng", "hẹp", "xa", "gần", "trái", "phải", "trên", 
    "dưới", "trước", "sau", "trong", "ngoài", "giữa", "cạnh", "quanh", "chổi", "quét", "dọn", "giặt", "giũ", 
    "nấu", "nướng", "tưới", "bón", "cắt", "tỉa", "xây", "đắp", "đào", "bới", "gánh", "gồng", "khuân", "vác", 
    "đẩy", "kéo", "xoay", "vặn", "mở", "khóa", "đóng", "sập", "vấp", "ngã", "trượt", "chân", "leo", "trèo", 
    "bơi", "lội", "lặn", "ngụp", "bay", "lượn", "bò", "sát", "nhai", "nuốt", "nhả", "nhổ", "khóc", "cười", 
    "nói", "hát", "kêu", "la", "hét", "thầm", "thì", "im", "lặng", "lắng", "nghe", "quan", "sát", "nhìn", 
    "ngó", "liếc", "mắt", "mỉm", "cười", "gật", "đầu", "lắc", "tay", "xua", "đuổi", "đón", "chào", "tạm", 
    "biệt", "hẹn", "gặp", "lại", "bình", "minh", "hoàng", "hôn", "ban", "ngày", "buổi", "tối", "đêm", 
    "khuya", "sáng", "sớm", "trưa", "hè", "chiều", "thu", "đông", "tàn", "xuân", "mới", "thời", "gian", 
    "không", "gian", "ranh", "giới", "khoảng", "cách", "tâm", "hồn", "ý", "nghĩ", "cảm", "xúc", "bâng", 
    "khuâng", "xao", "xuyến", "bồi", "hồi", "nao", "nức", "rạo", "rực", "thẫn", "thờ", "ngơ", "ngác", 
    "vội", "vã", "thong", "thả", "chậm", "rãi", "nhẹ", "nhàng", "êm", "ái", "xù", "xì", "thô", "ráp", 
    "mấp", "mô", "gập", "ghềnh", "khúc", "khuỷu", "oai", "nghiêm", "hùng", "vĩ", "thơ", "mộng", "hữu", 
    "tình", "hoang", "sơ", "kỳ", "bí", "cổ", "kính", "hiện", "đại", "xa", "hoa", "giản", "dị", "mộc", 
    "mạc", "chân", "quê", "thanh", "cao", "quý", "phái", "sang", "trọng", "lộng", "lẫy", "kiêu", "sa", 
    "nhút", "nhát", "rụt", "rè", "mạnh", "dạn", "tự", "tin", "ngang", "bướng", "bướng", "bỉnh", "hiền", 
    "lành", "độc", "ác", "tốt", "bụng", "xấu", "xa", "tham", "lam", "ích", "kỷ", "rộng", "lượng", 
    "bao", "dung", "tha", "thứ", "trân", "trọng", "nâng", "niu", "gìn", "giữ", "bảo", "vệ", "xây", 
    "dựng", "phá", "hủy", "thay", "đổi", "giữ", "nguyên", "bắt", "đầu", "kết", "thúc", "vĩnh", "viễn", 
    "tạm", "thời", "thường", "xuyên", "hiếm", "khi", "đôi", "lúc", "thỉnh", "thoảng", "hàng", "ngày", 
    "mỗi", "tuần", "tháng", "năm", "thế", "kỷ", "thiên", "niên", "kỷ", "vũ", "trụ", "thiên", "hà", 
    "vì", "sao", "hành", "tinh", "trăng", "sao", "mặt", "trời", "trái", "đất", "không", "khí", "oxy", 
    "hydro", "ánh", "sáng", "bóng", "tối", "âm", "thanh", "im", "lặng", "tiếng", "động", 
    "ồn", "ào", "náo", "nhiệt", "vắng", "vẻ", "tĩnh", "mịch", "yên", "ả", "trong", "lành", "mát", 
    "mẻ", "ấm", "áp", "oi", "bức", "nồng", "nặc", "nhạt", "nhẽo", "đậm", "đà", "thơm", "lừng", 
    "nức", "nở", "nghẹn", "ngào", "sung", "sướng", "hạnh", "phúc", "khổ", "đau", "buồn", "rầu", 
    "lo", "lắng", "sợ", "hãi", "giận", "dữ", "bình", "tĩnh", "kiên", "nhẫn", "vội", "vàng", 
    "hấp", "tấp", "cẩn", "thận", "đo", "đàng", "khéo", "léo", "vụng", "về", "đảm", "đang", 
    "tháo", "vát", "lười", "biếng", "chăm", "chỉ", "cần", "cù", "siêng", "năng", "sáng", "tạo", 
    "thông", "minh", "ngớ", "ngẩn", "ngây", "ngô", "khờ", "dại", "tỉnh", "táo", "say", "sưa", 
    "mơ", "màng", "mộng", "mị", "thức", "tỉnh", "đời", "thực", "chiêm", "bao", "ảo", "giác", 
    "sự", "thật", "giả", "dối", "thật", "thà", "trung", "thực", "gian", "xảo", "lọc", "lừa", 
    "ngay", "thẳng", "công", "bằng", "chính", "trực", "liêm", "khiết", "đức", "hạnh", "phẩm", 
    "giá", "uy", "tín", "danh", "dự", "vinh", "quang", "nhục", "nhã", "thất", "bại", "thành", 
    "công", "nỗ", "lực", "cố", "gắng", "kiên", "trì", "nhẫn", "nại", "vượt", "qua", "chinh", 
    "phục", "khám", "phá", "trải", "nghiệm", "hành", "trình", "con", "đường", "lối", "đi", 
    "ngõ", "nhỏ", "phố", "lớn", "làng", "quê", "thị", "xã", "thành", "phố", "thủ", "đô", 
    "biên", "giới", "hải", "đảo", "cao", "nguyên", "đồng", "bằng", "rừng", "rậm", "sa", 
    "mạc", "thung", "lũng", "vực", "thẳm", "đỉnh", "núi", "mây", "mù", "sương", "khói", 
    "hơi", "nước", "giọt", "lệ", "mồ", "hôi", "máu", "thịt", "xương", "cốt", "hơi", "thở", 
    "nhịp", "đập", "trái", "tim", "bộ", "não", "trí", "nhớ", "hồi", "ức", "tương", "lai", 
    "hiện", "tại", "quá", "khứ", "kỷ", "niệm", "ước", "mơ", "hy", "vọng", "niềm", "tin", 
    "lý", "tưởng", "hoài", "bão", "khát", "khao", "đam", "mê", "sở", "thích", "thói", 
    "quen", "tính", "cách", "số", "phận", "may", "mắn", "rủi", "ro", "tình", "cờ", 
    "ngẫu", "nhiên", "sắp", "đặt", "định", "mệnh", "nhân", "duyên", "gặp", "gỡ", "chia", 
    "ly", "xa", "cách", "gần", "gũi", "thân", "thuộc", "lạ", "lẫm", "mới", "mẻ", "cũ", 
    "kỹ", "lạc", "hậu", "cổ", "hủ", "lỗi", "thời", "tiên", "tiến", "hiện", "đại", "hóa", 
    "tự", "động", "hóa", "công", "nghiệp", "hóa", "đô", "thị", "hóa", "toàn", "cầu", 
    "hóa", "thiên", "nhiên", "môi", "trường", "sinh", "thái", "đa", "dạng", "phong", 
    "phú", "dồi", "dào", "khan", "hiếm", "quý", "hiếm", "phổ", "biến", "tràn", "lan", 
    "dày", "đặc", "thưa", "thớt", "rải", "rác", "tập", "trung", "phân", "tán", "mở", 
    "rộng", "thu", "hẹp", "nâng", "cao", "hạ", "thấp", "tăng", "cường", "giảm", "bớt", 
    "duy trì", "ổn", "định", "phát", "triển", "bền", "vững", "tiến", "bộ", "văn", 
    "minh", "giàu", "có", "nghèo", "đói", "no", "đủ", "thiếu", "thốn", "ấm", "no", 
    "tự", "do", "bình", "đẳng", "bác", "ái", "nhân", "đạo", "hòa", "bình", "xung", 
    "đột", "chiến", "tranh", "hữu", "nghị", "hợp", "tác", "giao", "lưu", "liên", 
    "kết", "kết", "nối", "chia", "sẻ", "giúp", "đỡ", "ủng", "hộ", "đồng", "tình", 
    "phản", "đối", "tranh", "luận", "bàn", "bạc", "thảo", "luận", "thống", "nhất", 
    "bất", "đồng", "mâu", "thuẫn", "giải", "quyết", "xử", "lý", "khắc", "phục", 
    "cải", "thiện", "đổi", "mới", "sáng", "tạo", "đột", "phá", "dẫn", "đầu", 
    "tiên", "phong", "theo", "kịp", "vượt", "mặt", "đuổi", "theo", "tìm", "kiếm", 
    "phát", "hiện", "nghiên", "cứu", "phân", "tích", "tổng", "hợp", "đánh", "giá", 
    "nhận", "xét", "phê", "bình", "khen", "ngợi", "cổ", "vũ", "động", "viên", 
    "an", "ủi", "vỗ", "về", "yêu", "thương", "quý", "mến", "ghét", "bỏ", "hận", 
    "thù", "tha", "thứ", "bao", "dung", "nhân", "ái", "hiền", "hậu", "đức", 
    "độ", "mẫu", "mực", "uy", "nghiêm", "oai", "phong", "lẫm", "liệt", "hào", 
    "hùng", "tráng", "lệ", "lung", "linh", "rực", "rỡ", "óng", "ánh", "lấp", 
    "lánh", "mờ", "ảo", "ảo", "diệu", "kỳ", "diệu", "tuyệt", "vời", "tuyệt", 
    "mỹ", "hoàn", "hảo", "xuất", "sắc", "xuất", "chúng", "tài", "năng", "thiên", 
    "tài", "thông", "thái", "uyên", "bác", "sâu", "sắc", "rộng", "lớn", "bao", 
    "la", "vô", "tận", "vô", "biên", "vĩnh", "cửu", "trường", "tồn", "bất", "diệt"
]

# Nạp thêm từ vựng từ file extra_words.json (Trang 2 Excel)
THEME_WORDS = {
    'Công nghệ & Khoa học': [
        "mạch", "tụ", "anten", "logic", "oxy", "hydro", "bán dẫn", "bình nóng lạnh",
        "băng thông", "chip", "chuyển đổi số", "chuỗi khối", "cáp quang", "cảm biến", "di động", "dây điện",
        "dữ liệu lớn", "hệ điều hành", "học máy", "không dây", "kinh tế số", "kết nối", "kỹ sư", "lò vi sóng",
        "lập trình", "lập trình viên", "máy chủ", "máy giặt", "máy hút bụi", "máy lọc nước", "máy sấy tóc", "mã hóa",
        "mã nguồn mở", "mạch tích hợp", "năng lượng xanh", "phần cứng", "phần mềm", "quỹ đạo", "robot", "thuật toán",
        "thực tế ảo", "trí tuệ nhân tạo", "tường lửa", "tự hành", "tự động hóa", "vi xử lý", "vi điều khiển", "viễn thông",
        "vô tuyến", "vạn vật", "vệ tinh", "xe điện", "xử lý ảnh", "y tế số", "điều hòa", "đường truyền",
        "ứng dụng"
    ],
    'Thiên nhiên & Địa lý': [
        "đá", "mây", "gió", "nắng", "mưa", "sông", "suối", "núi",
        "rừng", "biển", "đảo", "bão", "tuyết", "lửa", "đất", "sao",
        "trăng", "trời", "An Giang", "Bình Dương", "Bình Phước", "Bình Thuận", "Bình Định", "Bạc Liêu",
        "Bắc Ninh", "Bến Tre", "Cao Bằng", "Châu Đốc", "Cà Mau", "Cần Thơ", "Cửa Lò", "Gia Lai",
        "Huế", "Hà Nội", "Hà Tĩnh", "Hòa Bình", "Hưng Yên", "Hải Dương", "Hải Phòng", "Hậu Giang",
        "Hội An", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Long An", "Lào Cai", "Lâm Đồng", "Lạng Sơn",
        "Mũi Né", "Nam Định", "Nghệ An", "Nha Trang", "Ninh Bình", "Ninh Thuận", "Phan Thiết", "Phong Nha",
        "Phú Quốc", "Phú Thọ", "Phú Yên", "Quy Nhơn", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Trị",
        "Sài Gòn", "Sóc Trăng", "Sơn La", "Sầm Sơn", "Thanh Hóa", "Thái Bình", "Thái Nguyên", "Tiền Giang",
        "Trà Vinh", "Tuyên Quang", "Tây Ninh", "Vĩnh Long", "Vĩnh Phúc", "Vũng Tàu", "Yên Bái", "huế",
        "thác", "Điện Biên", "Đà Lạt", "Đà Nẵng", "Đắk Lắk", "Đắk Nông", "Đồng Nai", "Đồng Tháp"
    ],
    'Động thực vật & Ẩm thực': [
        "bưởi", "hành", "quả", "tiêu", "hoa", "cỏ", "lá", "cành",
        "mèo", "chó", "gà", "vịt", "bò", "lợn", "chim", "cá",
        "hổ", "báo", "nai", "thỏ", "rùa", "rắn", "ếch", "ong",
        "bướm", "kiến", "sâu", "cam", "chuối", "đường", "thịt", "cà chua",
        "bánh canh", "bánh chưng", "bánh cuốn", "bánh giầy", "bánh in", "bánh mì", "bánh pía", "bánh tét",
        "bánh xèo", "bún bò", "bún chả", "bắp cải", "canh măng", "chè bưởi", "chè thạch", "chôm chôm",
        "chả quế", "cà phê", "cà rốt", "cá rán", "cây", "cơm tấm", "dâu tây", "dưa chuột",
        "dưa hấu", "dứa", "dừa", "giò lụa", "giò thủ", "hành tây", "hủ tiếu", "kem bơ",
        "khoai tây", "lẩu gà", "muối", "mâm xôi", "mì quảng", "măng cụt", "măng tây", "mật",
        "nem rán", "nhãn vải", "nước mía", "nấm hương", "phở bò", "rau", "sinh tố", "súp lơ",
        "sầu riêng", "sữa chua", "thanh long", "thịt kho", "trà chanh", "trà sữa", "việt quất", "xôi gấc",
        "đu đủ"
    ],
    'Cảm xúc & Con người': [
        "người", "con", "vui", "buồn", "hiền", "độc", "ác", "tốt",
        "xấu", "tham", "ích", "lo", "sợ", "giận", "yêu", "thương",
        "ghét", "hận", "biên tập viên", "bác sĩ", "bảo vệ", "ca sĩ", "chuyên viên", "chủ tịch",
        "công chứng viên", "công nhân", "cộng tác viên", "diễn viên", "dược sĩ", "dịch giả", "giám đốc", "giáo viên",
        "họa sĩ", "kiến trúc sư", "kiểm toán viên", "luật sư", "lối đi", "nha sĩ", "nhiếp ảnh gia", "nhà báo",
        "nhà văn", "nhạc sĩ", "phi công", "phi hành gia", "phục vụ", "quản lý", "thu ngân", "thư ký",
        "thẩm phán", "thợ may", "tiếp viên", "tài xế", "y tá", "đại sứ", "đạo diễn", "đầu bếp"
    ],
    'Đời sống & Đồ vật': [
        "đi", "học", "làm", "nhà", "cái", "có", "không", "và",
        "một", "những", "được", "trong", "cho", "đến", "với", "từ",
        "khi", "viễn", "thông", "linh", "kiện", "điện", "tín", "hiệu",
        "vi", "trở", "mạng", "lưới", "thuật", "toán", "dữ", "liệu",
        "phần", "mềm", "ứng", "dụng", "biến", "số", "hàm", "lập",
        "trình", "hệ", "thống", "máy", "chủ", "bóng", "trọng", "tài",
        "bàn", "thắng", "tấn", "công", "phòng", "ngự", "tiền", "đạo",
        "thủ", "môn", "ngoằn", "ngoèo", "khuỷu", "tay", "thuở", "ấy",
        "rượi", "nhễ", "nhại", "lững", "lờ", "thiên", "nhiên", "hòa",
        "bình", "giáo", "dục", "sáng", "tạo", "thực", "tế", "thành",
        "rực", "rỡ", "mênh", "mông", "sản", "xuất", "sắc", "lỏng",
        "lẻo", "nơm", "nớp", "truyền", "chương", "khuyến", "khích", "tương",
        "lai", "gia", "đình", "nghệ", "tri", "thức", "hạnh", "phúc",
        "xử", "lý", "giao", "diện", "tính", "phím", "tốc", "độ",
        "trò", "chơi", "tử", "trực", "tuyến", "kết", "nối", "tin",
        "phát", "triển", "cơ", "sở", "hạ", "tầng", "thiết", "kế",
        "kỹ", "phân", "tích", "vận", "minh", "hoạt", "chính", "xác",
        "bền", "bỉ", "thời", "gian", "vũ", "trụ", "khám", "phá",
        "trải", "nghiệm", "tuyệt", "vời", "nỗ", "lực", "kiên", "trì",
        "đam", "mê", "khát", "vọng", "tự", "do", "quốc", "kiểm",
        "tra", "đồng", "bộ", "tối", "ưu", "động", "hoàn", "thiện",
        "rèn", "luyện", "định", "mục", "ý", "tưởng", "giải", "pháp",
        "đóng", "góp", "cống", "hiến", "giá", "trị", "vững", "lan",
        "tỏa", "cảm", "hứng", "vẻ", "nhiệt", "huyết", "tập", "trung",
        "tĩnh", "quyết", "đoán", "chân", "thân", "đoàn", "gắn", "bó",
        "chia", "sẻ", "thấu", "hiểu", "trân", "biết", "ơn", "khiêm",
        "tốn", "hỏi", "tiến", "ngừng", "cát", "hươu", "ghế", "giường",
        "tủ", "bát", "đũa", "cốc", "chén", "áo", "quần", "mũ",
        "giày", "bút", "thước", "sách", "vở", "cửa", "tường", "gạch",
        "ngói", "đỏ", "vàng", "lục", "lam", "chàm", "tím", "trắng",
        "đen", "xám", "nâu", "hồng", "bạc", "son", "thắm", "chạy",
        "nhảy", "đứng", "ngồi", "ăn", "uống", "ngủ", "nghỉ", "nhanh",
        "chậm", "cao", "thấp", "dài", "ngắn", "to", "nhỏ", "nóng",
        "lạnh", "oằn", "xoáy", "loay", "hoay", "nhuyễn", "quỵt", "huýt",
        "suýt", "nhuần", "lẫm", "liệt", "hủ", "tiếu", "sừng", "sững",
        "bỡ", "ngỡ", "hẫng", "hụt", "chênh", "vênh", "lảo", "nghễu",
        "nghện", "khệnh", "khạng", "mặn", "ngọt", "chua", "cay", "đắng",
        "chát", "nồng", "gắt", "thơm", "thối", "hôi", "tanh", "tròn",
        "vuông", "méo", "thẳng", "cong", "lệch", "phẳng", "nhám", "nhẵn",
        "cứng", "dẻo", "dai", "giòn", "xốp", "mỏng", "dày", "rộng",
        "hẹp", "xa", "gần", "trái", "phải", "trên", "dưới", "trước",
        "sau", "ngoài", "giữa", "cạnh", "quanh", "chổi", "quét", "dọn",
        "giặt", "giũ", "nấu", "nướng", "tưới", "bón", "cắt", "tỉa",
        "xây", "đắp", "đào", "bới", "gánh", "gồng", "khuân", "vác",
        "đẩy", "kéo", "xoay", "vặn", "mở", "khóa", "sập", "vấp",
        "ngã", "trượt", "leo", "trèo", "bơi", "lội", "lặn", "ngụp",
        "bay", "lượn", "sát", "nhai", "nuốt", "nhả", "nhổ", "khóc",
        "cười", "nói", "hát", "kêu", "la", "hét", "thầm", "thì",
        "im", "lặng", "lắng", "nghe", "quan", "nhìn", "ngó", "liếc",
        "mắt", "mỉm", "gật", "đầu", "lắc", "xua", "đuổi", "đón",
        "chào", "tạm", "biệt", "hẹn", "gặp", "lại", "hoàng", "hôn",
        "ban", "ngày", "buổi", "đêm", "khuya", "sớm", "trưa", "hè",
        "chiều", "thu", "đông", "tàn", "xuân", "mới", "ranh", "giới",
        "khoảng", "cách", "tâm", "hồn", "nghĩ", "xúc", "bâng", "khuâng",
        "xao", "xuyến", "bồi", "hồi", "nao", "nức", "rạo", "thẫn",
        "thờ", "ngơ", "ngác", "vội", "vã", "thong", "thả", "rãi",
        "nhẹ", "nhàng", "êm", "ái", "xù", "xì", "thô", "ráp",
        "mấp", "mô", "gập", "ghềnh", "khúc", "oai", "nghiêm", "hùng",
        "vĩ", "thơ", "mộng", "hữu", "tình", "hoang", "sơ", "kỳ",
        "bí", "cổ", "kính", "hiện", "đại", "giản", "dị", "mộc",
        "mạc", "quê", "thanh", "quý", "phái", "sang", "lộng", "lẫy",
        "kiêu", "sa", "nhút", "nhát", "rụt", "rè", "mạnh", "dạn",
        "ngang", "bướng", "bỉnh", "lành", "bụng", "kỷ", "lượng", "bao",
        "dung", "tha", "thứ", "nâng", "niu", "gìn", "giữ", "bảo",
        "vệ", "dựng", "hủy", "thay", "đổi", "nguyên", "bắt", "thúc",
        "vĩnh", "thường", "xuyên", "hiếm", "đôi", "lúc", "thỉnh", "thoảng",
        "hàng", "mỗi", "tuần", "tháng", "năm", "thế", "niên", "hà",
        "vì", "tinh", "mặt", "khí", "ánh", "âm", "tiếng", "ồn",
        "ào", "náo", "vắng", "mịch", "yên", "ả", "mát", "mẻ",
        "ấm", "áp", "oi", "bức", "nặc", "nhạt", "nhẽo", "đậm",
        "đà", "lừng", "nở", "nghẹn", "ngào", "sung", "sướng", "khổ",
        "đau", "rầu", "hãi", "nhẫn", "hấp", "tấp", "cẩn", "thận",
        "đo", "đàng", "khéo", "léo", "vụng", "về", "đảm", "đang",
        "tháo", "vát", "lười", "biếng", "chăm", "chỉ", "cần", "cù",
        "siêng", "năng", "ngớ", "ngẩn", "ngây", "ngô", "khờ", "dại",
        "tỉnh", "táo", "say", "sưa", "mơ", "màng", "mị", "đời",
        "chiêm", "ảo", "giác", "sự", "thật", "giả", "dối", "thà",
        "xảo", "lọc", "lừa", "ngay", "bằng", "liêm", "khiết", "đức",
        "phẩm", "uy", "danh", "dự", "vinh", "quang", "nhục", "nhã",
        "thất", "bại", "cố", "gắng", "nại", "vượt", "qua", "chinh",
        "phục", "lối", "ngõ", "phố", "lớn", "làng", "thị", "xã",
        "đô", "biên", "hải", "rậm", "thung", "lũng", "vực", "thẳm",
        "đỉnh", "mù", "sương", "khói", "hơi", "nước", "giọt", "lệ",
        "mồ", "máu", "xương", "cốt", "thở", "nhịp", "đập", "tim",
        "não", "trí", "nhớ", "ức", "tại", "quá", "khứ", "niệm",
        "ước", "hy", "niềm", "hoài", "khao", "thích", "thói", "quen",
        "phận", "may", "mắn", "rủi", "ro", "cờ", "ngẫu", "sắp",
        "đặt", "mệnh", "nhân", "duyên", "gỡ", "ly", "gũi", "thuộc",
        "lạ", "cũ", "lạc", "hậu", "lỗi", "tiên", "hóa", "nghiệp",
        "toàn", "cầu", "môi", "trường", "sinh", "thái", "đa", "dạng",
        "phong", "phú", "dồi", "dào", "khan", "phổ", "tràn", "đặc",
        "thưa", "thớt", "rải", "rác", "tán", "tăng", "cường", "giảm",
        "bớt", "duy trì", "ổn", "văn", "giàu", "nghèo", "đói", "no",
        "đủ", "thiếu", "thốn", "đẳng", "bác", "xung", "đột", "chiến",
        "tranh", "nghị", "hợp", "tác", "lưu", "liên", "giúp", "đỡ",
        "ủng", "hộ", "phản", "đối", "luận", "thảo", "nhất", "bất",
        "mâu", "thuẫn", "khắc", "cải", "dẫn", "theo", "kịp", "tìm",
        "kiếm", "nghiên", "cứu", "tổng", "đánh", "nhận", "xét", "phê",
        "khen", "ngợi", "viên", "an", "ủi", "vỗ", "mến", "bỏ",
        "thù", "mẫu", "mực", "hào", "tráng", "lung", "óng", "lấp",
        "lánh", "mờ", "diệu", "mỹ", "hảo", "chúng", "uyên", "vô",
        "tận", "cửu", "tồn", "diệt", "Hạ", "Pa", "Sa", "ba",
        "ban công", "bi", "bida", "bin", "biệt thự", "bu", "buốt", "bàn chông",
        "bàn là", "bàng", "béo", "bên", "bìa", "bình hoa", "bông", "bùi",
        "bùng", "búp", "bưu điện", "bạch", "bảng", "bảo tàng", "bấm", "bẩn",
        "bập", "bắc", "bến xe", "bếp ga", "bềnh", "bể", "bệnh viện", "bị",
        "bọ", "bối", "bốn", "bồ", "bồn", "bồng", "cao ốc", "chiếp",
        "chiếu", "choàng", "chu", "chung cư", "chuyền", "chuyện", "chuồn", "chán",
        "châu", "chì", "chìa khóa", "chùi", "chúc", "chạng", "chải", "chấn",
        "chấu", "chậu rửa", "chồn", "chợ búa", "chụp", "chữ", "co", "compa",
        "cravat", "cua", "cung", "cuống", "cuồng", "cài", "cánh", "cáo",
        "cáu", "cân", "câu", "công trình", "công tắc", "công viên", "cùm", "cú",
        "cúc", "căm", "cưa", "cưng", "cưới", "cạn", "cạp", "cấp",
        "cầu thang", "cầu vượt", "cẩu", "cận", "cặp", "cột đèn", "cửa cuốn", "cửa hàng",
        "cự", "da", "diều", "duy", "dán", "dây", "dã", "dép",
        "dính", "dương", "dưỡng", "dạ", "dạo", "dấu", "dập", "dẹp",
        "dẻ", "dề", "dềnh", "ghen", "ghim", "ghé", "ghém", "ghề",
        "giá treo", "giông", "giấy", "giếng trời", "gác", "gò", "góc", "gói",
        "gót", "gôm", "gông", "găng", "gương soi", "gấm", "gấp", "gấu",
        "gầm", "gầy", "gồ", "gỗ", "hang", "hanh", "hao", "heo",
        "hiu", "hiên nhà", "hiệu thuốc", "hoan", "hoen", "hoét", "huơ", "hàng rào",
        "hái", "hám", "hán", "hân", "hình", "hô", "hôm", "hùm",
        "hăng", "hơn", "hướng", "hạc", "hại", "hạn", "hả", "hầm chui",
        "hầm gửi xe", "hắc", "hằng", "hến", "họp", "hỏa", "hố", "hối",
        "hồ", "hội", "hộp", "hớt", "hừng", "internet", "jean", "keng",
        "keo", "khoeo", "khoác", "khoảnh", "khoắt", "khuynh", "khuyên", "khuây",
        "khuýp", "khuất", "khuỵu", "khách sạn", "khét", "khô", "khú", "khăn",
        "khẩu", "khắm", "khế", "khỏe", "khởi", "kim", "kè", "két sắt",
        "kìm", "kẹp", "kẻ", "kế toán", "kệ", "kịch", "kỵ", "lang",
        "lao", "lau nhà", "len", "leng", "loa đài", "loét", "loảng", "lu",
        "lái xe", "lát", "lân", "lê", "lít", "líu", "lô", "lũ",
        "lưa", "lưng", "lưu trữ", "lược", "lằn", "lẹt", "lịm", "lọ",
        "lốc", "lối thoát hiểm", "lốp", "lồng", "lổn", "lỗ", "lớp", "lợp",
        "lụt", "lừ", "lửng", "mai", "mang", "men", "mi", "mua",
        "muống", "mà", "mái ngói", "mét", "mít", "móc áo", "môi giới", "mùa",
        "mượt", "mận", "mập", "mệt", "mỏi", "mốc", "mồm", "nam",
        "nay", "nga", "ngan", "nghêu", "nghịu", "ngoác", "ngoạc", "ngoại",
        "ngoạm", "ngoảnh", "nguyệt", "nguệch", "nguội", "ngát", "ngân hàng", "ngã tư",
        "ngùng", "ngượng", "ngạc", "ngạt", "ngần", "ngẫm", "ngậy", "ngắt",
        "ngọc", "nham", "nho", "nhoàng", "nhoáng", "nhung", "nhà ga", "nhà hát",
        "nhà kho", "nhà máy", "nhà nghỉ", "nhà thi đấu", "nhà xe", "nháp", "nhím", "nhô",
        "nhạnh", "nhấp", "nhật", "nhặt", "nhện", "nhổn", "nhở", "nhợt",
        "nhừ", "nuôi", "nuối", "nàn", "nòng", "nón", "nông", "nản",
        "nảy", "nắn", "nặng", "nề", "nồi cơm", "nợ", "nữa", "nực",
        "oại", "oải", "pa", "phanh", "phin", "phía", "phích cắm", "phông",
        "phùn", "phương", "phấn", "phụ", "quyển", "quán cà phê", "quạ", "quạng",
        "quạt máy", "quảng trường", "quờ", "ran", "rách", "râm", "rã", "rèm cửa",
        "rén", "rét", "rêu", "rì", "rình", "róc", "rón", "rơi",
        "rưới", "rạng", "rập", "rết", "rệu", "rối", "rời", "san",
        "sen", "siêu thị", "su", "suy", "suốt", "sáo", "sân bay", "sét",
        "sò", "sóc", "sói", "săm", "săng", "sơn", "sạch", "sấm",
        "sầm", "sắm", "sặc", "sẽ", "sỏi", "sổ", "sờ", "sỡ",
        "sợi", "sứa", "sửa", "tai", "tam", "than", "thang máy", "thao",
        "thiền", "thoang", "thoi", "thoại", "thuyền", "thính", "thít", "thú",
        "thút", "thăm", "thư viện", "thướt", "thưởng", "thượng", "thảm", "thần kinh",
        "thẫm", "thập", "thắt", "thằn", "thể", "thỉu", "thị giác", "thỏm",
        "thổ", "thủy", "tivi", "tiếc", "tiết", "tiệm ăn", "trang", "tranh ảnh",
        "treo tường", "triều", "triển lãm", "tro", "trùng", "trăm", "trường học", "trại",
        "trạm xe buýt", "trải sàn", "trồng", "trừ", "tuyền", "tuộc", "tà", "tê",
        "tía", "tòa nhà", "tôm", "tú", "túi", "tơ", "tươi", "tưởi",
        "tượng đài", "tạ", "tạp", "tất", "tần", "tẩy", "tắm", "tắp",
        "tết", "tỉ", "tị", "tọa", "tới", "tủ lạnh", "tủ thuốc", "tức",
        "uế", "uốn", "ve", "vest", "viết", "voi", "vu", "vách",
        "váy", "vân", "ví", "vòi nước", "vòng", "vôi", "vương", "vạng",
        "vạt", "vằn", "vẹo", "vẹt", "vẽ", "vỉa hè", "vị", "vữa",
        "xem", "xi", "xiên", "xoa", "xoài", "xoảng", "xuýt", "xà",
        "xách", "xè", "xích", "xòe", "xó", "xô", "xôn", "xơ",
        "xưa", "xưởng phim", "xếp", "yoga", "yến", "âu", "ô", "đan",
        "đeo", "đinh", "điểu", "điệp", "đoạn", "đám mây", "đèn bàn", "đê",
        "đùi", "đơn", "đượm", "đại lý", "đầm", "đậu", "đằng", "đẽo",
        "đế", "đọc", "đố", "đồ", "đỗ", "đới", "đờ", "đục",
        "đừ", "ưng", "ướt", "ấm siêu tốc", "ẩm", "ổ cắm", "ổi", "ở"
    ],
}

# Định nghĩa lại VIETNAMESE_WORDS từ danh sách tĩnh đã chuẩn hóa
VIETNAMESE_WORDS = []
for words in THEME_WORDS.values():
    VIETNAMESE_WORDS.extend(words)
VIETNAMESE_WORDS = list(dict.fromkeys(VIETNAMESE_WORDS))

THEME_DICTIONARIES = {
    "Công nghệ & Khoa học": {
        "compounds": {
            "phần mềm", "phần cứng", "ứng dụng", "lập trình", "hệ thống", "máy chủ", "viễn thông", 
            "mạng lưới", "băng thông", "cáp quang", "dữ liệu", "thuật toán", "vi mạch", "mạch điện", 
            "tín hiệu", "điện trở", "tụ điện", "chuyển đổi số", "chuỗi khối", "trí tuệ nhân tạo", 
            "ảo hóa", "khoa học", "kỹ thuật", "công nghệ", "nghiên cứu", "phát minh", "sáng chế", 
            "thiết kế", "giao diện", "tốc độ", "máy tính", "bàn phím", "trực tuyến", "kết nối", 
            "tin học", "logic", "kinh tế số", "học máy", "hệ điều hành", "tự động hóa", "công nghiệp hóa",
            "kỹ sư", "lập trình viên", "công nghệ thông tin", "mã hóa", "mã nguồn mở", "bán dẫn", 
            "máy giặt", "máy hút bụi", "máy lọc nước", "máy sấy tóc", "lò vi sóng", "không dây", 
            "bình nóng lạnh", "dữ liệu lớn", "thiết bị", "kỹ thuật số", "di động", "dây điện",
            "cảm biến", "mạch tích hợp", "tường lửa", "vi xử lý", "vi điều khiển", "xe điện",
            "y tế số", "thực tế ảo", "xử lý ảnh", "năng lượng xanh", "quỹ đạo", "tự hành",
            "vô tuyến", "vạn vật", "vệ tinh", "điều hòa", "đường truyền"
        },
        "singles": {
            "anten", "web", "data", "code", "chip", "robot", "server", "logic", "oxy", "hydro", 
            "helium", "nitơ", "tụ", "mạch"
        }
    },
    "Thiên nhiên & Địa lý": {
        "compounds": {
            "hoàng hôn", "bình minh", "vũ trụ", "hành tinh", "môi trường", "sinh thái", "thiên hà", 
            "cao nguyên", "đồng bằng", "thung lũng", "vực thẳm", "địa lý", "quốc gia", "thành phố", 
            "thị xã", "làng quê", "phố xá", "đường sá", "biên giới", "hải đảo", "đại dương", 
            "khí hậu", "thời tiết", "thiên nhiên", "không gian", "ánh sáng", "bóng tối", "không khí", 
            "sa mạc", "đỉnh núi", "vùng vịnh", "mây mù", "sương khói", "nước biển", "gió bão",
            "an giang", "bình dương", "bình phước", "bình thuận", "bình định", "bạc liêu", 
            "bắc ninh", "bến tre", "cao bằng", "châu đốc", "cà mau", "cần thơ", "cửa lò", 
            "gia lai", "huế", "hà nội", "hà tĩnh", "hòa bình", "hưng yên", "hải dương", 
            "hải phòng", "hậu giang", "hội an", "khánh hòa", "kiên giang", "kon tum", 
            "long an", "lào cai", "lâm đồng", "lạng sơn", "mũi né", "nam định", "nghệ an", 
            "nha trang", "ninh bình", "ninh thuận", "phan thiết", "phong nha", "phú quốc", 
            "phú thọ", "phú yên", "quy nhơn", "quảng bình", "quảng nam", "quảng ngãi", 
            "quảng trị", "sài gòn", "sóc trăng", "sơn la", "sầm sơn", "thanh hóa", 
            "thái bình", "thái nguyên", "tiền giang", "trà vinh", "tuyên quang", "tây ninh", 
            "vĩnh long", "vĩnh phúc", "vũng tàu", "yên bái", "điện biên", "đà lạt",
            "đà nẵng", "đắk lắk", "đắk nông", "đồng nai", "đồng tháp"
        },
        "singles": {
            "mây", "mưa", "gió", "nắng", "sông", "biển", "đảo", "núi", "rừng", "suối", "thác", 
            "bão", "tuyết", "đất", "đá", "lửa", "trời", "sao", "trăng", "vịnh"
        }
    },
    "Động thực vật & Ẩm thực": {
        "compounds": {
            "bông sen", "hoa hồng", "hoa lan", "hoa mai", "hoa cúc", "hoa đào", "ẩm thực", 
            "món ăn", "ăn uống", "nấu nướng", "gia vị", "cà phê", "cà chua", "cà rốt", 
            "dâu tây", "dưa chuột", "dưa hấu", "măng cụt", "măng tây", "bắp cải", "nem rán", 
            "hủ tiếu", "bánh canh", "bánh chưng", "bánh cuốn", "bánh giầy", "bánh in", 
            "bánh mì", "bánh pía", "bánh tét", "bánh xèo", "bún bò", "bún chả", "chả quế", 
            "lẩu gà", "giò lụa", "giò thủ", "chè bưởi", "chè thạch", "kem bơ", "mâm xôi", 
            "mì quảng", "cá rán", "hành tây", "khoai tây", "rau quả", "trà sữa", "nước ngọt",
            "động vật", "thực vật", "cây cối", "hoa quả", "chôm chôm", "bún riêu", "bánh bao",
            "đậu hũ", "đậu phụ", "nước mắm", "hạt tiêu", "củ tỏi", "củ hành", "rau cải",
            "canh măng", "cơm tấm", "nước mía", "nấm hương", "phở bò", "sinh tố", "súp lơ",
            "sầu riêng", "sữa chua", "thanh long", "thịt kho", "trà chanh", "việt quất",
            "xôi gấc", "đu đủ", "nhãn vải"
        },
        "singles": {
            "mèo", "chó", "gà", "vịt", "bò", "lợn", "chim", "cá", "hổ", "báo", "nai", "thỏ", 
            "rùa", "rắn", "ếch", "ong", "bướm", "kiến", "sâu", "hoa", "cỏ", "lá", "cành", "cây", "chuối", 
            "bưởi", "cam", "quýt", "măng", "dưa", "tây", "tiêu", "ớt", "tỏi", "hành", "chanh", 
            "muối", "đường", "mật", "sữa", "trà", "bia", "rượu", "dứa", "dừa", "rau", "quả", 
            "kẹo", "mứt", "thịt", "cơm", "phở", "bún", "canh", "bánh"
        }
    },
    "Cảm xúc & Con người": {
        "compounds": {
            "chân thành", "tử tế", "thân thiện", "đoàn kết", "gắn bó", "chia sẻ", "thấu hiểu", 
            "trân trọng", "biết ơn", "khiêm tốn", "học hỏi", "tiến bộ", "chăm chỉ", "siêng năng", 
            "cần cù", "lười biếng", "thông minh", "ngớ ngẩn", "ngây ngô", "khờ dại", "tỉnh táo", 
            "say sưa", "mơ màng", "mộng mị", "thức tỉnh", "đời thực", "chiêm bao", "ảo giác", 
            "sự thật", "giả dối", "trung thực", "gian xảo", "lọc lừa", "ngay thẳng", "công bằng", 
            "chính trực", "liêm khiết", "đức hạnh", "phẩm giá", "uy tín", "danh dự", "vinh quang", 
            "nhục nhã", "thất bại", "thành công", "nỗ lực", "cố gắng", "kiên trì", "nhẫn nại", 
            "vượt qua", "chinh phục", "khám phá", "trải nghiệm", "hành trình", "con đường", 
            "lối đi", "ngẫu nhiên", "nhân duyên", "gặp gỡ", "chia ly", "xa cách", "gần gũi", 
            "thân thuộc", "lạ lẫm", "hạnh phúc", "đau khổ", "bình tĩnh", "tự tin", "quyết đoán", 
            "bao dung", "tha thứ", "nâng niu", "gìn giữ", "bảo vệ", "cảm hứng", "nhiệt huyết", 
            "tập trung", "nơm nớp", "lo lắng", "sợ hãi", "giận dữ", "vui vẻ", "bồi hồi", 
            "xao xuyến", "bâng khuâng", "nao nức", "rạo rực", "thẫn thờ", "ngơ ngác", "vội vã", 
            "thong thả", "chậm rãi", "nhẹ nhàng", "êm ái", "nhút nhát", "rụt rè", "mạnh dạn", 
            "ngang bướng", "bướng bỉnh", "hiền lành", "độc ác", "tốt bụng", "xấu xa", "tham lam", 
            "ích kỷ", "rộng lượng", "yêu thương", "quý mến", "ghét bỏ", "hận thù", "tha thứ", 
            "hiền hậu", "đức độ", "mẫu mực", "uy nghiêm", "oai phong", "lẫm liệt", "hào hùng", 
            "kỳ diệu", "tuyệt vời", "tuyệt mỹ", "hoàn hảo", "xuất sắc", "xuất chúng", "tài năng", 
            "thiên tài", "thông thái", "uyên bác", "sâu sắc", "người học", "gia đình", "trò chơi", 
            "biên tập viên", "bác sĩ", "chuyên viên", "công chứng viên", "công nhân", "công tác viên", 
            "chủ tịch", "diễn viên", "dược sĩ", "dịch giả", "giám đốc", "giáo viên", "họa sĩ", 
            "kiến trúc sư", "kiểm toán viên", "luật sư", "lập trình viên", "nhiếp ảnh gia", "nha sĩ", 
            "ca sĩ", "nhạc sĩ", "nhà văn", "nhà thơ", "phi công", "phóng viên", "tài xế", "thủ khoa", 
            "thạc sĩ", "tiến sĩ", "trọng tài", "tiền đạo", "thủ môn", "vận động viên", "hướng dẫn viên", 
            "nghệ sĩ", "người thân", "đồng nghiệp", "bạn bè", "cha mẹ", "ông bà", "anh em", "chị em",
            "tình cảm", "yêu đương", "tự hào", "kiêu hãnh", "thất vọng", "tuyệt vọng", "đam mê",
            "cộng tác viên", "nhà báo", "phi hành gia", "thu ngân", "thư ký", "thẩm phán", 
            "thợ may", "tiếp viên", "y tá", "đại sứ", "đạo diễn", "đầu bếp", "phục vụ", "quản lý"
        },
        "singles": {
            "vui", "buồn", "lo", "sợ", "giận", "thương", "yêu", "ghét", "hận", "độc", "ác", "tốt", 
            "xấu", "tham", "ích", "hiền", "dũng", "người", "con", "mẹ", "cha", "anh", "em", "chị",
            "ông", "bà", "tớ", "cậu", "ta", "mình"
        }
    }
}

def get_precise_category(word):
    word_lower = word.lower().strip()
    for cat, dicts in THEME_DICTIONARIES.items():
        if word_lower in dicts["compounds"]:
            return cat
        if " " not in word_lower:
            if word_lower in dicts["singles"]:
                return cat
    return "Đời sống & Đồ vật"

import re
EXTRA_WORDS_FILE = "extra_words.json"
if os.path.exists(EXTRA_WORDS_FILE):
    try:
        with open(EXTRA_WORDS_FILE, "r", encoding="utf-8") as f:
            extra = json.load(f)
        for w in extra:
            w_clean = w.strip()
            w_clean = re.sub(r'^[.,!?;:"\']+|[.,!?;:"\']+$', '', w_clean).strip()
            if not w_clean:
                continue
            w_lower = w_clean.lower()
            if w_lower in ["từ vựng input", "stt", "độ dài (ký tự)", "độ dài", "ký tự", "input"]:
                continue
            if re.match(r'^[0-9\W_]+$', w_clean):
                continue
            
            # Check if already present
            found = False
            for cat, words in THEME_WORDS.items():
                if w_clean in words:
                    found = True
                    break
            if not found:
                cat = get_precise_category(w_clean)
                THEME_WORDS[cat].append(w_clean)
        
        # Update VIETNAMESE_WORDS
        VIETNAMESE_WORDS = []
        for words in THEME_WORDS.values():
            VIETNAMESE_WORDS.extend(words)
        VIETNAMESE_WORDS = list(dict.fromkeys(VIETNAMESE_WORDS))
    except Exception as e:
        pass

VIETNAMESE_SENTENCES = [
    "Tiếng Việt là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.",
    "Học gõ mười ngón giúp bạn tăng tốc độ soạn thảo văn bản và bảo vệ sức khỏe.",
    "Việt Nam là một quốc gia nằm ở phía đông bán đảo Đông Dương thuộc khu vực Đông Nam Á.",
    "Công nghệ thông tin đang thay đổi thế giới một cách nhanh chóng và hiệu quả.",
    "Bánh mì và phở là hai món ăn nổi tiếng nhất của Việt Nam trên bản đồ ẩm thực thế giới."
]

def get_random_words(count=100, difficulty="Vừa", topic="Tất cả"):
    if topic == "Tất cả" or topic not in THEME_WORDS:
        pool_words = list(dict.fromkeys(VIETNAMESE_WORDS))
    else:
        pool_words = list(dict.fromkeys(THEME_WORDS[topic]))
        
    def get_difficulty_score(word):
        score = len(word)
        complex_chars = "đưỡượơuôâê"
        score += sum(2 for c in word if c in complex_chars)
        return score

    if difficulty == "Dễ":
        pool = [w for w in pool_words if get_difficulty_score(w) < 5]
    elif difficulty == "Khó":
        pool = [w for w in pool_words if get_difficulty_score(w) >= 8]
    else: # Vừa
        pool = [w for w in pool_words if 4 <= get_difficulty_score(w) < 8]
        
    if not pool:
        pool = pool_words
    if not pool:
        pool = list(dict.fromkeys(VIETNAMESE_WORDS))

    if len(pool) < count:
        multiplier = (count // len(pool)) + 1
        pool = pool * multiplier
        
    random.shuffle(pool)
    return " ".join(pool[:count])

def get_random_sentence():
    sentences = VIETNAMESE_SENTENCES.copy()
    if os.path.exists(CUSTOM_SENTENCES_FILE):
        try:
            with open(CUSTOM_SENTENCES_FILE, "r", encoding="utf-8") as f:
                custom = json.load(f)
                sentences.extend(custom)
        except:
            pass
    return random.choice(sentences)

# --- Persistence & Stats ---
def get_stats_file():
    # Store in local app data or current dir (for portable)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_stats.json")

def load_user_stats():
    path = get_stats_file()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"history": [], "best_wpm": 0, "mistakes": {}}

def save_user_stats(stats):
    try:
        with open(get_stats_file(), "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
    except: pass

def record_session(wpm, accuracy, wpm_history=None):
    stats = load_user_stats()
    session = {
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "wpm": wpm,
        "acc": accuracy,
        "graph": wpm_history or []
    }
    if "history" not in stats: stats["history"] = []
    stats["history"].append(session)
    
    current_best = stats.get("best_wpm", 0)
    if wpm > current_best:
        stats["best_wpm"] = wpm
        is_new_record = True
    else:
        is_new_record = False
    
    save_user_stats(stats)
    return is_new_record, stats["best_wpm"]

def add_mistake(word):
    if not word or len(word) < 2: return
    stats = load_user_stats()
    if "mistakes" not in stats: stats["mistakes"] = {}
    mistakes = stats["mistakes"]
    mistakes[word] = mistakes.get(word, 0) + 1
    save_user_stats(stats)

def get_mistake_words(count=50):
    stats = load_user_stats()
    mistakes = stats.get("mistakes", {})
    if not mistakes: return []
    # Sort by frequency of mistakes
    sorted_mistakes = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)
    words = [item[0] for item in sorted_mistakes[:count]]
    return words

def get_all_sentences():
    sentences = VIETNAMESE_SENTENCES.copy()
    if os.path.exists(CUSTOM_SENTENCES_FILE):
        try:
            with open(CUSTOM_SENTENCES_FILE, "r", encoding="utf-8") as f:
                custom = json.load(f)
                sentences.extend(custom)
        except:
            pass
    return sentences

def add_custom_sentence(text):
    if not text.strip(): return
    custom = []
    if os.path.exists(CUSTOM_SENTENCES_FILE):
        try:
            with open(CUSTOM_SENTENCES_FILE, "r", encoding="utf-8") as f:
                custom = json.load(f)
        except:
            pass
    custom.append(text.strip())
    with open(CUSTOM_SENTENCES_FILE, "w", encoding="utf-8") as f:
        json.dump(custom, f, ensure_ascii=False, indent=4)
