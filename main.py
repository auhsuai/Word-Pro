import tkinter as tk
from tkinter import messagebox  
import customtkinter as ctk
import time
import random
import os
import sys
import json
import threading
import ctypes
try:
    import winreg
except ImportError:
    winreg = None # For non-windows platforms if needed
from data import get_random_words, get_random_sentence, add_custom_sentence, get_all_sentences, resource_path
from audio import AudioMixin
from graph import GraphMixin
from auth import AuthMixin
from logic import LogicMixin
from dialogs import DialogsMixin
from updater import UpdaterMixin

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

VERSION = "1.8.1"
# Link "Raw" dẫn đến file version.json trên GitHub của bạn
UPDATE_URL = "https://raw.githubusercontent.com/auhsuai/Word-Pro/main/version.json"

class WordProApp(ctk.CTk, AudioMixin, GraphMixin, AuthMixin, LogicMixin, DialogsMixin, UpdaterMixin):
    def __init__(self):
        super().__init__()

        self.title(f"Word Pro v{VERSION} - Luyện gõ tiếng Việt")
        self.geometry("1100x750")
        self.minsize(900, 600)
        
        # Set Window Icon
        try:
            from data import resource_path
            icon_path = resource_path("app_icon.ico")
            if os.path.exists(icon_path):
                self.after(200, lambda: self.iconbitmap(icon_path))
        except:
            pass

        # Hide main window initially
        self.withdraw()
        
        # Delay check to prevent crash on startup
        self.after(100, self.check_activation)

        self.time_limit = 60 # Default
        self.time_left = 60
        self.timer_id = None
        self.mode = "words" # words or sentences
        self.difficulty = "Vừa" # Dễ, Vừa, Khó
        self.selected_sentence_option = "Ngẫu nhiên"
        
        self.target_words = [] # List of target words
        self.typed_words = [] # List of confirmed words
        self.current_typed = "" # Current word being typed
        self.last_type_time = time.time()
        self.accuracy_threshold = 0.4 # 40% minimum accuracy
        self.min_chars_to_check = 20
        self.inactivity_limit = 10 # seconds
        self.can_undo_space = False # New state to allow going back exactly once
        
        self.consecutive_ime_errors = 0
        self.ime_warning_active = False
        self.is_cooldown = False
        self.cooldown_timer_id = None
        
        self.setup_ui()
        self.reset_test()
        
        # Stats & Sound Settings
        self.sound_enabled = True
        from data import load_user_stats
        user_stats = load_user_stats()
        self.best_wpm = user_stats.get("best_wpm", 0)
        self.wpm_history = []
        
        # Check for updates in background
        import threading
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def setup_ui(self):
        # Configure root grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Menu bar row
        self.grid_rowconfigure(1, weight=1) # Main content row

        # 1. Custom Dark Menu Bar
        self.menu_bar = ctk.CTkFrame(self, height=35, fg_color="#1a1a1a", corner_radius=0)
        self.menu_bar.grid(row=0, column=0, sticky="ew")
        
        # Define Dark Menu Styles
        menu_style = {"bg": "#2b2b2b", "fg": "#ffffff", "activebackground": "#3b82f6", "activeforeground": "#ffffff", "tearoff": 0, "bd": 0}

        # Open File Button (far LEFT of menu bar)
        self.open_file_btn = ctk.CTkButton(self.menu_bar, text="Mở file", width=100, height=25,
                                           fg_color="transparent", hover_color="#333333",
                                           command=self.open_file_mode)
        self.open_file_btn.pack(side="left", padx=5, pady=5)

        # System Menu
        self.sys_menu_popup = tk.Menu(self, **menu_style)
        self.sys_menu_popup.add_command(label="Làm mới (Esc)", command=self.reset_test)
        self.sys_menu_popup.add_command(label="Xem lịch sử & Kỷ lục", command=self.show_history_dialog)
        self.sys_menu_popup.add_separator()
        self.sys_menu_toggle_sound = tk.BooleanVar(value=True)
        self.sys_menu_popup.add_checkbutton(label="Âm thanh khi gõ", variable=self.sys_menu_toggle_sound, 
                                            command=self.toggle_sound)
        self.sys_menu_popup.add_separator()
        self.sys_menu_popup.add_command(label="Thoát", command=self.quit)
        
        self.sys_btn = ctk.CTkButton(self.menu_bar, text="Hệ thống", width=100, height=25,
                                     fg_color="transparent", hover_color="#333333",
                                     command=lambda: self.show_popup_menu(self.sys_btn, self.sys_menu_popup))
        self.sys_btn.pack(side="left", padx=5, pady=5)

        # Help Menu
        self.help_menu_popup = tk.Menu(self, **menu_style)
        self.help_menu_popup.add_command(label="Cách luyện tập", command=self.show_help)
        self.help_menu_popup.add_command(label="Danh sách phím tắt", command=self.show_shortcuts)
        
        self.help_btn = ctk.CTkButton(self.menu_bar, text="Hướng dẫn", width=100, height=25,
                                      fg_color="transparent", hover_color="#333333",
                                      command=lambda: self.show_popup_menu(self.help_btn, self.help_menu_popup))
        self.help_btn.pack(side="left", padx=5, pady=5)

        # Info Menu
        self.info_menu_popup = tk.Menu(self, **menu_style)
        self.info_menu_popup.add_command(label="Kiểm tra cập nhật", command=self.check_for_updates_manual)
        self.info_menu_popup.add_separator()
        self.info_menu_popup.add_command(label="Về Word Pro", command=self.show_about)
        
        self.info_btn = ctk.CTkButton(self.menu_bar, text="Thông tin", width=100, height=25,
                                      fg_color="transparent", hover_color="#333333",
                                      command=lambda: self.show_popup_menu(self.info_btn, self.info_menu_popup))
        self.info_btn.pack(side="left", padx=5, pady=5)

        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure root to be responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Configure main_container to be responsive
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(4, weight=1) # Give the text display area the most weight

        # Main Header / Toolbar (Positioned at the very top)
        self.toolbar_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.toolbar_frame.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        self.toolbar_frame.grid_columnconfigure(1, weight=1)

        # Left: Reset Button
        self.reset_btn = ctk.CTkButton(self.toolbar_frame, text="Làm mới (Esc)", command=self.reset_test, 
                                      fg_color="#3b82f6", hover_color="#2563eb", height=45, width=150,
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.reset_btn.grid(row=0, column=0, padx=10)

        # Left-Center: Difficulty
        self.difficulty_selector = ctk.CTkSegmentedButton(self.toolbar_frame, values=["Dễ", "Vừa", "Khó"],
                                                        command=self.change_difficulty, height=45, 
                                                        font=ctk.CTkFont(size=16))
        self.difficulty_selector.set("Vừa")
        self.difficulty_selector.grid(row=0, column=1, padx=10, sticky="w")

        # Right: Mode & Time
        self.ctrl_subframe = ctk.CTkFrame(self.toolbar_frame, fg_color="transparent")
        self.ctrl_subframe.grid(row=0, column=2, padx=10)

        self.time_selector = ctk.CTkSegmentedButton(self.ctrl_subframe, values=["30s", "60s", "120s"],
                                                   command=self.change_time_limit, height=45,
                                                   font=ctk.CTkFont(size=16))
        self.time_selector.set("60s")
        self.time_selector.pack(side="left", padx=5)

        self.mode_selector = ctk.CTkSegmentedButton(self.ctrl_subframe, values=["Từ ngẫu nhiên", "Câu có sẵn", "Từ hay sai"],
                                                   command=self.change_mode, height=45,
                                                   font=ctk.CTkFont(size=16))
        self.mode_selector.set("Từ ngẫu nhiên")
        self.mode_selector.pack(side="left", padx=5)

        self.sentence_dropdown = ctk.CTkOptionMenu(self.ctrl_subframe, values=["Ngẫu nhiên", "Xáo trộn tất cả"],
                                                   command=self.change_sentence_selection, width=200, height=45,
                                                   font=ctk.CTkFont(size=14))
        self.sentence_dropdown.pack(side="left", padx=5)
        self.sentence_dropdown.pack_forget()

        # Add Button (for sentences mode)
        self.add_btn = ctk.CTkButton(self.toolbar_frame, text="+", command=self.open_add_sentence_dialog,
                                    fg_color="#4b5563", hover_color="#374151", height=45, width=45, 
                                    font=ctk.CTkFont(size=20, weight="bold"))
        self.add_btn.grid(row=0, column=3, padx=10)
        self.add_btn.grid_remove()

        # Stats Area (Below Toolbar)
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, pady=(0, 10))
        self.stats_frame.grid_remove()

        self.wpm_label = ctk.CTkLabel(self.stats_frame, text="WPM: 0", font=ctk.CTkFont(size=24, weight="bold"), text_color="#4ade80")
        self.wpm_label.pack(side="left", padx=20)

        self.acc_label = ctk.CTkLabel(self.stats_frame, text="Accuracy: 0%", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3b82f6")
        self.acc_label.pack(side="left", padx=20)

        # Graph Area (Below Stats)
        self.graph_canvas = tk.Canvas(self.main_container, height=150, bg="#1e1e1e", 
                                      highlightthickness=0, bd=0)
        self.graph_canvas.grid(row=5, column=0, sticky="ew", padx=40, pady=(0, 20))
        self.graph_canvas.grid_remove() # Hide initially
        
        # Make graph responsive to resizing
        self.graph_canvas.bind("<Configure>", lambda e: self.draw_wpm_graph())

        # Timer Display (Centered)

        # Timer Display (Centered)
        self.timer_label = ctk.CTkLabel(self.main_container, text="60s", font=ctk.CTkFont(size=48, weight="bold"), text_color="#3b82f6")
        self.timer_label.grid(row=2, column=0, pady=(10, 20))

        # Text Display Container (Sleek horizontal bar style)
        self.text_frame = ctk.CTkFrame(self.main_container, fg_color="#2b2b2b", corner_radius=15, height=150)
        self.text_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_propagate(False)

        self.text_display = tk.Text(self.text_frame, font=("Inter", 28), wrap="none", 
                                   bg="#2b2b2b", fg="#888888", insertofftime=0, 
                                   height=1, padx=40, borderwidth=0, highlightthickness=0)
        self.text_display.grid(row=0, column=0, sticky="ew", pady=55)
        self.text_display.tag_config("correct", foreground="#4ade80")
        self.text_display.tag_config("incorrect", foreground="#f87171")
        self.text_display.tag_config("current", background="#4b5563", foreground="#9ca3af")
        self.text_display.config(state="disabled")
        self.text_display.bind("<Configure>", lambda e: self.update_display())

        # Message Overlay (Initially hidden)
        self.overlay_frame = ctk.CTkFrame(self.text_frame, fg_color="#1e1e1e", corner_radius=15)
        self.overlay_label = ctk.CTkLabel(self.overlay_frame, text="", font=ctk.CTkFont(size=22, weight="bold"), 
                                         text_color="#9ca3af", wraplength=600)
        self.overlay_label.pack(expand=True, pady=(15, 5))
        
        self.cooldown_label = ctk.CTkLabel(self.overlay_frame, text="", font=ctk.CTkFont(size=13), text_color="#3b82f6")
        self.cooldown_label.pack(pady=(0, 5))

        self.overlay_subtext = ctk.CTkLabel(self.overlay_frame, text="Nhấn phím bất kỳ hoặc click để bắt đầu lại", 
                                           font=ctk.CTkFont(size=13), text_color="#6b7280")
        self.overlay_subtext.pack(pady=(0, 15))
        
        self.control_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.control_frame.grid(row=5, column=0, pady=(20, 0))
        self.control_frame.grid_remove() # Hide the bottom frame entirely

        self.ime_toast = ctk.CTkLabel(self.main_container, text="⚠️ Hình như bạn chưa bật bộ gõ tiếng Việt?", 
                                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#facc15")
        self.ime_toast.grid(row=6, column=0, pady=10)
        self.ime_toast.grid_remove()

        # Fixed-height container for warnings to prevent layout shift and overlap
        self.warning_container = ctk.CTkFrame(self.main_container, fg_color="transparent", width=600, height=40)
        self.warning_container.grid(row=3, column=0)
        self.warning_container.pack_propagate(False) # Lock the height and width for packed children

        self.caps_warning = ctk.CTkLabel(self.warning_container, text="KIỂM TRA LẠI CAPS LOCK!", 
                                         text_color="#facc15", font=ctk.CTkFont(size=16, weight="bold"))
        self.caps_warning.pack(expand=True)
        self.caps_warning.pack_forget()
        
        # IME Warning Toast (Subtle)

        # Input logic
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.handle_input_change)
        
        self.input_entry = ctk.CTkEntry(self, width=0, height=0, textvariable=self.input_var)
        self.input_entry.place(x=-1000, y=-1000)
        self.input_entry.bind("<Key>", self.handle_keypress)
        self.input_entry.bind("<FocusIn>", self.on_focus_in)
        self.input_entry.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Escape>", lambda e: self.reset_test())
        self.bind("<Button-1>", lambda e: self.input_entry.focus_set())
        self.input_entry.focus_set()
        self.bind("<KeyPress>", self.check_capslock)
        self.bind("<KeyRelease>", self.check_capslock)
        self.bind("<FocusIn>", lambda e: self.check_capslock())

    def set_display_focus(self, focused: bool):
        if focused:
            self.text_display.config(fg="#888888")
            self.text_display.tag_config("correct", foreground="#4ade80")
            self.text_display.tag_config("incorrect", foreground="#f87171")
            self.text_display.tag_config("current", background="#3b82f6", foreground="white")
        else:
            self.text_display.config(fg="#444444")
            self.text_display.tag_config("correct", foreground="#2e7d32")
            self.text_display.tag_config("incorrect", foreground="#993333")
            self.text_display.tag_config("current", background="#374151", foreground="#9ca3af")

    def on_focus_in(self, event=None):
        self.set_display_focus(True)
        self.check_capslock()

    def on_focus_out(self, event=None):
        self.set_display_focus(False)

    def check_capslock(self, event=None):
        is_on = False
        if event is not None and hasattr(event, "state"):
            is_on = bool(event.state & 0x0002)
        else:
            try:
                import ctypes
                # 0x14 is VK_CAPITAL
                is_on = bool(ctypes.windll.user32.GetKeyState(0x14) & 1)
            except:
                pass
        try:
            if is_on:
                self.caps_warning.pack(expand=True)
            else:
                self.caps_warning.pack_forget()
        except:
            pass

    def change_time_limit(self, value):
        self.time_limit = int(value.replace("s", ""))
        self.reset_test()

    def open_file_mode(self):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="Chọn file từ vựng",
            filetypes=[("Text/CSV files", "*.txt *.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse: split by comma, newline, or semicolon
            import re
            words = re.split(r"[\n,;]+", content)
            words = [w.strip() for w in words if w.strip()]

            if not words:
                self.show_custom_dialog("Lỗi", "Không tìm thấy từ nào trong file này!\nVui lòng kiểm tra định dạng file.")
                return

            # Save to self for use in load_new_text
            self.custom_file_words = words
            self.mode = "file"

            # Reset test with new word list
            self.reset_test()
            self.open_file_btn.configure(fg_color="#3b82f6") # Highlight to show active
            self.show_custom_dialog(
                "Đã nạp file",
                f"Nạp thành công {len(words)} từ từ file:\n{filepath.split('/')[-1]}\n\nLàm mới bài tập để bắt đầu luyện tập!"
            )
        except Exception as e:
            self.show_custom_dialog("Lỗi đọc file", f"Không thể đọc file này.\n\nChi tiết: {str(e)}")

    def change_mode(self, value):
        if value == "Từ hay sai":
            self.mode = "mistakes"
        else:
            self.mode = "words" if value == "Từ ngẫu nhiên" else "sentences"
        
        self.open_file_btn.configure(fg_color="#4b5563") # Reset file btn highlight
        if self.mode == "sentences":
            self.sentence_dropdown.pack(side="left", padx=5)
            self.difficulty_selector.grid_remove()
            self.add_btn.grid()
            self.update_sentence_dropdown()
        else:
            self.sentence_dropdown.pack_forget()
            self.difficulty_selector.grid()
            self.add_btn.grid_remove()
        self.reset_test()

    def change_difficulty(self, value):
        self.difficulty = value
        self.reset_test()

    def change_sentence_selection(self, value):
        self.selected_sentence_option = value
        self.reset_test()

    def update_sentence_dropdown(self):
        sentences = get_all_sentences()
        # Create display names for sentences (first 30 chars)
        display_options = ["Ngẫu nhiên", "Xáo trộn tất cả"]
        for i, s in enumerate(sentences):
            short = (s[:30] + "..") if len(s) > 30 else s
            display_options.append(f"{i+1}. {short}")
        
        self.sentence_dropdown.configure(values=display_options)
        if self.selected_sentence_option not in display_options:
            self.sentence_dropdown.set("Ngẫu nhiên")
            self.selected_sentence_option = "Ngẫu nhiên"


if __name__ == "__main__":
    app = WordProApp()
    app.mainloop()
