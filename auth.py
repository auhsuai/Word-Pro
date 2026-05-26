import tkinter as tk
import customtkinter as ctk
try:
    import winreg
except ImportError:
    winreg = None

class AuthMixin:
    def show_key_dialog(self):
        self.key_dialog = ctk.CTkToplevel(self)
        self.key_dialog.title("Kích hoạt Word Pro")
        self.key_dialog.geometry("400x250")
        self.key_dialog.resizable(False, False)
        self.key_dialog.attributes("-topmost", True)
        
        # Center the dialog
        screen_width = self.key_dialog.winfo_screenwidth()
        screen_height = self.key_dialog.winfo_screenheight()
        x = (screen_width / 2) - (400 / 2)
        y = (screen_height / 2) - (250 / 2)
        self.key_dialog.geometry(f"400x250+{int(x)}+{int(y)}")

        label = ctk.CTkLabel(self.key_dialog, text="Vui lòng nhập Key để sử dụng", 
                             font=ctk.CTkFont(size=16, weight="bold"))
        label.pack(pady=(30, 10))

        self.key_entry = ctk.CTkEntry(self.key_dialog, width=300, height=40, placeholder_text="Nhập Key tại đây...",
                                      justify="center", font=ctk.CTkFont(size=14))
        self.key_entry.pack(pady=10)
        self.key_entry.bind("<Return>", lambda e: self.verify_key())

        verify_btn = ctk.CTkButton(self.key_dialog, text="KÍCH HOẠT", command=self.verify_key,
                                   width=200, height=40, fg_color="#3b82f6", hover_color="#2563eb",
                                   font=ctk.CTkFont(weight="bold"))
        verify_btn.pack(pady=10)

        self.key_status_label = ctk.CTkLabel(self.key_dialog, text="", text_color="#f87171", font=ctk.CTkFont(size=12))
        self.key_status_label.pack()

        # If window closed without key, quit app
        self.key_dialog.protocol("WM_DELETE_WINDOW", self.quit)

    def check_activation(self):
        if self.is_activated():
            self.deiconify()
        else:
            self.show_key_dialog()

    def is_activated(self):
        if not winreg: return False
        try:
            # Mở khóa Registry của Word Pro
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\WordProVietnamese", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "LicenseKey")
            winreg.CloseKey(key)
            return value == "WORDPRO1139392026"
        except:
            return False

    def verify_key(self):
        entered_key = self.key_entry.get().strip()
        CORRECT_KEY = "WORDPRO1139392026" 

        if entered_key == CORRECT_KEY:
            # Lưu trạng thái kích hoạt vào Registry
            if winreg:
                try:
                    # Tạo hoặc mở khóa
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\WordProVietnamese")
                    winreg.SetValueEx(key, "LicenseKey", 0, winreg.REG_SZ, CORRECT_KEY)
                    winreg.CloseKey(key)
                except Exception as e:
                    print(f"Registry Error: {e}")
            
            # Hiển thị thông báo thành công màu xanh
            self.key_status_label.configure(text="Đã kích hoạt thành công! Vui lòng chờ ứng dụng phản hồi...", text_color="#4ade80")
            self.key_entry.configure(state="disabled") 
            
            # Đợi một chút rồi mới nạp dữ liệu thật
            self.after(800, self.start_real_loading)
        else:
            self.key_status_label.configure(text="Key không chính xác, vui lòng thử lại!", text_color="#f87171")
            self.key_entry.delete(0, tk.END)
            self.key_entry.focus_set()
            # Tự động xóa thông báo lỗi sau 4 giây
            self.after(4000, lambda: self.key_status_label.configure(text=""))

    def start_real_loading(self):
        # Đây là nơi ứng dụng thực sự xử lý chuẩn bị
        # Chúng ta giả lập hoặc thực hiện các tác vụ nặng ở đây
        self.load_new_text() # Nạp từ vựng
        self.calculate_stats() # Reset chỉ số
        
        # Sau khi mọi thứ đã "OK hết", mới chính thức vào app
        self.finish_activation()

    def finish_activation(self):
        if hasattr(self, "key_dialog"):
            self.key_dialog.destroy()
        self.deiconify() # Hiện app chính
        self.input_entry.focus_set() # Tự động focus vào ô gõ chữ
