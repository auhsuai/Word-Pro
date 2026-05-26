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
    "hydro", "nitơ", "ánh", "sáng", "bóng", "tối", "âm", "thanh", "im", "lặng", "tiếng", "động", 
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
EXTRA_WORDS_FILE = "extra_words.json"
if os.path.exists(EXTRA_WORDS_FILE):
    try:
        with open(EXTRA_WORDS_FILE, "r", encoding="utf-8") as f:
            extra = json.load(f)
            # Merge and remove duplicates
            VIETNAMESE_WORDS = list(dict.fromkeys(VIETNAMESE_WORDS + extra))
    except:
        pass

VIETNAMESE_SENTENCES = [
    "Tiếng Việt là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.",
    "Học gõ mười ngón giúp bạn tăng tốc độ soạn thảo văn bản và bảo vệ sức khỏe.",
    "Việt Nam là một quốc gia nằm ở phía đông bán đảo Đông Dương thuộc khu vực Đông Nam Á.",
    "Công nghệ thông tin đang thay đổi thế giới một cách nhanh chóng và hiệu quả.",
    "Bánh mì và phở là hai món ăn nổi tiếng nhất của Việt Nam trên bản đồ ẩm thực thế giới."
]

def get_random_words(count=100, difficulty="Vừa"):
    unique_words = list(dict.fromkeys(VIETNAMESE_WORDS))
    
    def get_difficulty_score(word):
        # A simple score based on length and presence of complex characters
        score = len(word)
        # Add points for complex Vietnamese vowels/consonants
        complex_chars = "đưỡượơuôâê"
        score += sum(2 for c in word if c in complex_chars)
        return score

    # Easy: Score < 5
    # Medium: 5 <= Score < 8
    # Hard: Score >= 8
    
    if difficulty == "Dễ":
        pool = [w for w in unique_words if get_difficulty_score(w) < 5]
    elif difficulty == "Khó":
        pool = [w for w in unique_words if get_difficulty_score(w) >= 8]
    else: # Vừa
        pool = [w for w in unique_words if 4 <= get_difficulty_score(w) < 8]
        
    # If pool is too small, fallback
    if len(pool) < 20: pool = unique_words
        
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
