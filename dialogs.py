import tkinter as tk
import customtkinter as ctk
import webbrowser

class DialogsMixin:
    def show_popup_menu(self, widget, menu):
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + widget.winfo_height()
        menu.post(x, y)

    def show_custom_dialog(self, title, content):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("550x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        # Modeless dialog - do not grab_set
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width / 2) - (550 / 2)
        y = (screen_height / 2) - (400 / 2)
        dialog.geometry(f"550x400+{int(x)}+{int(y)}")

        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=30, pady=30)

        label_title = ctk.CTkLabel(frame, text=title.upper(), font=ctk.CTkFont(size=18, weight="bold"), text_color="#3b82f6")
        label_title.pack(pady=(0, 20))

        text_widget = tk.Text(frame, font=("Inter", 12), wrap="word", bg="#2b2b2b", fg="#d1d5db", 
                              borderwidth=0, highlightthickness=0, height=10)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both")

        close_btn = ctk.CTkButton(dialog, text="ĐÓNG", command=dialog.destroy, 
                                  width=120, height=35, fg_color="#3b82f6", hover_color="#2563eb",
                                  font=ctk.CTkFont(weight="bold"))
        close_btn.pack(pady=(0, 20))

    def show_update_popup(self, version, url, changelog):
        """Hiện bảng thông báo cập nhật chuyên nghiệp với thanh tiến trình"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Hệ thống cập nhật tự động")
        dialog.geometry("500x420")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)
        y = (screen_height / 2) - (420 / 2)
        dialog.geometry(f"500x420+{int(x)}+{int(y)}")

        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=30, pady=25)

        self.upd_title = ctk.CTkLabel(frame, text=f"PHIÊN BẢN MỚI v{version}", 
                                   font=ctk.CTkFont(size=20, weight="bold"), text_color="#fbbf24")
        self.upd_title.pack(pady=(0, 15))

        self.upd_log_frame = ctk.CTkFrame(frame, fg_color="#1e1e1e", corner_radius=10)
        self.upd_log_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        log_text = tk.Text(self.upd_log_frame, font=("Inter", 11), wrap="word", bg="#1e1e1e", fg="#e5e7eb", 
                           borderwidth=0, highlightthickness=0, padx=10, pady=10, height=8)
        log_text.insert("1.0", f"Nội dung cập nhật:\n\n{changelog}")
        log_text.config(state="disabled")
        log_text.pack(expand=True, fill="both")

        # Khung chứa nút bấm
        self.upd_btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.upd_btn_frame.pack(fill="x", side="bottom")

        # Khung chứa thanh tiến trình (ẩn lúc đầu)
        self.upd_progress_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(self.upd_progress_frame, width=400, height=12)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        self.progress_label = ctk.CTkLabel(self.upd_progress_frame, text="Đang chuẩn bị tải xuống...", font=("Inter", 11))
        self.progress_label.pack()

        def start_download():
            self.upd_btn_frame.pack_forget() # Ẩn nút bấm
            self.upd_progress_frame.pack(fill="x", side="bottom") # Hiện thanh tiến trình
            self.start_smart_update(url, dialog) # Gọi hàm tải bên updater.py

        # Thêm phương thức cập nhật tiến trình cho cửa sổ dialog
        def update_progress(p):
            self.progress_bar.set(p / 100)
            self.progress_label.configure(text=f"Đang tải bản cập nhật: {p}%")
        
        def show_error(err):
            self.progress_label.configure(text=f"Lỗi: {err}", text_color="#ef4444")
            self.upd_btn_frame.pack(fill="x", side="bottom")

        dialog.update_progress = update_progress
        dialog.show_error = show_error

        download_btn = ctk.CTkButton(self.upd_btn_frame, text="CẬP NHẬT NGAY", command=start_download,
                                     fg_color="#3b82f6", hover_color="#2563eb", width=160, height=40,
                                     font=ctk.CTkFont(weight="bold"))
        download_btn.pack(side="left", padx=(30, 10))

        later_btn = ctk.CTkButton(self.upd_btn_frame, text="ĐỂ SAU", command=dialog.destroy,
                                   fg_color="#4b5563", hover_color="#374151", width=120, height=40,
                                   font=ctk.CTkFont(weight="bold"))
        later_btn.pack(side="left", padx=10)

    def show_history_dialog(self):
        from tkinter import filedialog
        from data import load_user_stats
        
        stats = load_user_stats()
        history = stats.get("history", [])
        best = stats.get("best_wpm", 0)
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Lịch sử luyện tập")
        dialog.geometry("750x600")
        dialog.resizable(True, True)
        dialog.transient(self)
        # Modeless dialog - do not grab_set
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"750x600+{int(sw/2-375)}+{int(sh/2-300)}")
        dialog.configure(fg_color="#2b2b2b")

        # === HEADER ===
        hdr = ctk.CTkFrame(dialog, fg_color="#2b2b2b", corner_radius=0, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        ctk.CTkLabel(hdr, text="LỊCH SỬ LUYỆN TẬP",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#ffffff").pack(side="left", padx=25, pady=20)

        stats_right = ctk.CTkFrame(hdr, fg_color="transparent")
        stats_right.pack(side="right", padx=25)
        ctk.CTkLabel(stats_right, text="KỶ LỤC",
                     font=ctk.CTkFont(size=11), text_color="#9ca3af").pack(anchor="e")
        ctk.CTkLabel(stats_right, text=f"{best} WPM",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#3b82f6").pack(anchor="e")

        # === SEARCH BAR ===
        search_frame = ctk.CTkFrame(dialog, fg_color="#2b2b2b", corner_radius=0, height=45)
        search_frame.pack(fill="x")
        search_frame.pack_propagate(False)

        ctk.CTkLabel(search_frame, text="Tìm kiếm:",
                     font=ctk.CTkFont(size=13), text_color="#9ca3af").pack(side="left", padx=(20,8), pady=10)
        search_var = tk.StringVar()
        ctk.CTkEntry(search_frame, textvariable=search_var, width=240, height=28,
                     fg_color="#2b2b2b", border_color="#3b82f6", border_width=1,
                     text_color="#ffffff", placeholder_text="Ngày, WPM...").pack(side="left", pady=8)
        total_label = ctk.CTkLabel(search_frame, text=f"Tổng: {len(history)} phiên",
                                   font=ctk.CTkFont(size=12), text_color="#6b7280")
        total_label.pack(side="right", padx=20)

        # === TABLE HEADER ===
        col_frame = ctk.CTkFrame(dialog, fg_color="#2b2b2b", corner_radius=0, height=36)
        col_frame.pack(fill="x")
        col_frame.pack_propagate(False)
        col_frame.grid_columnconfigure(0, weight=0, minsize=60)
        col_frame.grid_columnconfigure(1, weight=1, minsize=220)
        col_frame.grid_columnconfigure(2, weight=0, minsize=160)
        col_frame.grid_columnconfigure(3, weight=0, minsize=140)
        for i, col in enumerate(["#", "Ngày & Giờ", "Tốc độ (WPM)", "Độ chính xác"]):
            ctk.CTkLabel(col_frame, text=col,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#3b82f6", anchor="center").grid(row=0, column=i, padx=5, pady=6, sticky="ew")

        # === SCROLLABLE TABLE ===
        table = ctk.CTkScrollableFrame(dialog, fg_color="#2b2b2b", corner_radius=0)
        table.pack(fill="both", expand=True)
        table.grid_columnconfigure(0, weight=0, minsize=60)
        table.grid_columnconfigure(1, weight=1, minsize=220)
        table.grid_columnconfigure(2, weight=0, minsize=160)
        table.grid_columnconfigure(3, weight=0, minsize=140)

        # === MINI GRAPH ===
        graph_label = ctk.CTkLabel(dialog, text="Nhấn vào một phiên để xem biểu đồ WPM",
                                   font=ctk.CTkFont(size=11), text_color="#6b7280")
        graph_label.pack(pady=(5, 0))
        mini_graph = tk.Canvas(dialog, height=120, bg="#2b2b2b", highlightthickness=0, bd=0)
        mini_graph.pack(fill="both", expand=False, padx=20, pady=(0, 5))

        dialog.current_graph_data = None
        dialog.current_session_info = ""
        dialog.history_rows = []

        def draw_mini_graph(graph_data=None, session_info=None):
            if graph_data is not None:
                dialog.current_graph_data = graph_data
                dialog.current_session_info = session_info

            data = dialog.current_graph_data
            info = dialog.current_session_info

            mini_graph.delete("all")
            w = mini_graph.winfo_width()
            h = mini_graph.winfo_height()
            
            if not data:
                if w > 10:
                    mini_graph.create_text(w // 2, h // 2,
                        text="Không có dữ liệu biểu đồ", fill="#6b7280", font=("Inter", 11))
                return
                
            if w < 100: w = 700
            mx, my = 40, 15
            gw, gh = w - 2 * mx, h - 2 * my
            points = [(p[0], p[1]) for p in data]
            max_wpm = max([p[1] for p in points] + [40])
            max_words = points[-1][0] if points else 1
            # Lưới ngang
            for i in range(0, max_wpm + 20, 20):
                y = h - my - (i / max_wpm * gh)
                mini_graph.create_line(mx, y, w - mx, y, fill="#333333", dash=(2, 4))
                mini_graph.create_text(mx - 18, y, text=str(i), fill="#666666", font=("Inter", 7))
            # Đường WPM
            coords = []
            for word_num, wpm in points:
                px = mx + (word_num / max_words * gw)
                py = h - my - (wpm / max_wpm * gh)
                coords.extend([px, py])
            if len(coords) >= 4:
                area = [mx, h - my] + coords + [coords[-2], h - my]
                mini_graph.create_polygon(area, fill="#1e293b", outline="")
                mini_graph.create_line(coords, fill="#3b82f6", width=2, smooth=True)
                for j in range(0, len(coords), 2):
                    mini_graph.create_oval(coords[j]-2, coords[j+1]-2, coords[j]+2, coords[j+1]+2,
                                           fill="#60a5fa", outline="#1e293b")
            graph_label.configure(text=f"Biểu đồ WPM - {info}")

        def on_graph_resize(event):
            if dialog.current_graph_data:
                draw_mini_graph()

        mini_graph.bind("<Configure>", on_graph_resize)

        def populate(data):
            for widget in getattr(dialog, "history_rows", []):
                try:
                    widget.destroy()
                except:
                    pass
            dialog.history_rows = []
            if not data:
                ctk.CTkLabel(table, text="Chưa có dữ liệu lịch sử.",
                             text_color="#6b7280", font=ctk.CTkFont(size=14)).grid(
                             row=0, column=0, columnspan=4, pady=40)
                return
            for i, s in enumerate(reversed(data)):
                wpm = s.get("wpm", 0)
                acc = s.get("acc", 0)
                stt = len(data) - i
                bg = "#2b2b2b"
                if wpm == best and best > 0: fg_wpm = "#3b82f6"
                elif wpm >= best * 0.8:      fg_wpm = "#4ade80"
                else:                        fg_wpm = "#e5e7eb"

                row_f = ctk.CTkFrame(table, fg_color=bg, corner_radius=0, height=32)
                row_f.grid(row=i, column=0, columnspan=4, sticky="ew")
                dialog.history_rows.append(row_f)
                row_f.grid_propagate(False)
                row_f.grid_columnconfigure(0, weight=0, minsize=60)
                row_f.grid_columnconfigure(1, weight=1, minsize=220)
                row_f.grid_columnconfigure(2, weight=0, minsize=160)
                row_f.grid_columnconfigure(3, weight=0, minsize=140)

                ctk.CTkLabel(row_f, text=str(stt), font=ctk.CTkFont(size=12),
                             text_color="#6b7280", anchor="center").grid(row=0, column=0, padx=5, sticky="ew")
                ctk.CTkLabel(row_f, text=s.get("date",""), font=ctk.CTkFont(size=12),
                             text_color="#d1d5db", anchor="center").grid(row=0, column=1, padx=5, sticky="ew")
                ctk.CTkLabel(row_f, text=f"{wpm} WPM", font=ctk.CTkFont(size=12, weight="bold"),
                             text_color=fg_wpm, anchor="center").grid(row=0, column=2, padx=5, sticky="ew")
                ctk.CTkLabel(row_f, text=f"{acc:.1f}%", font=ctk.CTkFont(size=12),
                             text_color="#9ca3af", anchor="center").grid(row=0, column=3, padx=5, sticky="ew")
                
                # Click vào dòng để xem biểu đồ
                graph_data = s.get("graph", [])
                info = f"{s.get('date','')} | {wpm} WPM | {acc:.1f}%"
                def on_click(e, gd=graph_data, si=info):
                    draw_mini_graph(gd, si)
                row_f.bind("<Button-1>", on_click)
                for child in row_f.winfo_children():
                    child.bind("<Button-1>", on_click)

        def filter_data(*_):
            q = search_var.get().lower()
            filtered = [s for s in history if q in s.get("date","").lower()
                        or q in str(s.get("wpm","")) or q in str(s.get("acc",""))]
            populate(filtered)
            total_label.configure(text=f"Hiện thị: {len(filtered)}/{len(history)} phiên")

        search_var.trace_add("write", filter_data)
        populate(history)

        # === BOTTOM BUTTONS ===
        btn_frame = ctk.CTkFrame(dialog, fg_color="#2b2b2b", corner_radius=0, height=56)
        btn_frame.pack(fill="x", side="bottom")
        btn_frame.pack_propagate(False)

        def export_csv():
            path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"),("Text","*.txt"),("All","*.*")],
                initialfile="wordpro_history.csv", title="Xuất lịch sử ra file"
            )
            if not path: return
            try:
                with open(path, "w", encoding="utf-8-sig", newline="") as f:
                    f.write("STT,Ngày & Giờ,Tốc độ (WPM),Độ chính xác (%)\n")
                    for i, s in enumerate(history, 1):
                        f.write(f"{i},{s.get('date','')},{s.get('wpm',0)},{s.get('acc',0):.1f}\n")
                self.show_message_dialog("Xuất thành công", f"Xuất {len(history)} phiên ra file:\n{path}")
            except Exception as e:
                self.show_message_dialog("Lỗi", str(e), is_error=True)

        def clear_history():
            def do_clear():
                from data import save_user_stats
                stats["history"] = []
                save_user_stats(stats)
                history.clear()
                populate([])
                total_label.configure(text="Tổng: 0 phiên")
            self.show_confirm_dialog(
                "Xóa lịch sử",
                "Bạn có chắc muốn xóa TOÀN BỘ lịch sử không?\nKhông thể hoàn tác!",
                do_clear
            )

        ctk.CTkButton(btn_frame, text="Xuất ra CSV (Excel)", command=export_csv,
                      fg_color="#3b82f6", hover_color="#2563eb", height=36, width=180,
                      font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(20,10), pady=10)
        ctk.CTkButton(btn_frame, text="Xóa lịch sử", command=clear_history,
                      fg_color="#374151", hover_color="#4b5563", height=36, width=130,
                      text_color="#f87171",
                      font=ctk.CTkFont(weight="bold")).pack(side="left", pady=10)
        ctk.CTkButton(btn_frame, text="ĐÓNG", command=dialog.destroy,
                      fg_color="transparent", hover_color="#333333", height=36, width=100,
                      border_width=1, border_color="#4b5563",
                      font=ctk.CTkFont(weight="bold")).pack(side="right", padx=20, pady=10)

    def show_help(self):
        help_text = "QUY TẮC LUYỆN TẬP:\n\n1. Gõ chính xác..."
        self.show_custom_dialog("Hướng dẫn luyện tập", help_text)

    def show_shortcuts(self):
        shortcuts = "PHÍM TẮT HỆ THỐNG:\n\n• [Esc]: Làm mới..."
        self.show_custom_dialog("Danh sách phím tắt", shortcuts)

    def show_about(self):
        try: from main import VERSION
        except: VERSION = "1.7.0"
        about_text = f"Word Pro - Phiên bản {VERSION}\n..."
        self.show_custom_dialog("Về Word Pro", about_text)

    def show_overlay(self, message, start_cooldown=False, is_update=False, url=""):
        self.overlay_label.configure(text=message)
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        if start_cooldown: self.start_cooldown_timer(5)
        else: self.cooldown_label.configure(text="")
        self.overlay_frame.bind("<Button-1>", lambda e: self.skip_cooldown())

    def start_cooldown_timer(self, seconds):
        if hasattr(self, 'cooldown_timer_id') and self.cooldown_timer_id: self.after_cancel(self.cooldown_timer_id)
        if seconds > 0:
            self.is_cooldown = True
            self.cooldown_label.configure(text=f"Có thể bắt đầu lại sau {seconds}s...")
            self.cooldown_timer_id = self.after(1000, lambda: self.start_cooldown_timer(seconds - 1))
        else:
            self.is_cooldown = False
            self.cooldown_label.configure(text="Sẵn sàng! Nhấn phím bất kỳ để tiếp tục")

    def skip_cooldown(self):
        if hasattr(self, 'cooldown_timer_id') and self.cooldown_timer_id: self.after_cancel(self.cooldown_timer_id)
        self.is_cooldown = False
        self.hide_overlay()
        if hasattr(self, 'reset_test'): self.reset_test()

    def hide_overlay(self):
        if hasattr(self, 'overlay_frame'): self.overlay_frame.place_forget()

    def open_add_sentence_dialog(self):
        dialog = ctk.CTkInputDialog(text="Nhập câu mới bạn muốn thêm:", title="Thêm câu mẫu")
        new_sentence = dialog.get_input()
        if new_sentence:
            from data import add_custom_sentence
            add_custom_sentence(new_sentence)
            self.show_overlay("Đã thêm câu mới thành công!")

    def show_message_dialog(self, title, content, is_error=False):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("450x220")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = (sw / 2) - (450 / 2)
        y = (sh / 2) - (220 / 2)
        dialog.geometry(f"450x220+{int(x)}+{int(y)}")
        dialog.configure(fg_color="#2b2b2b")
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=25, pady=20)
        
        title_color = "#ef4444" if is_error else "#3b82f6"
        lbl_title = ctk.CTkLabel(frame, text=title.upper(), font=ctk.CTkFont(size=16, weight="bold"), text_color=title_color)
        lbl_title.pack(pady=(0, 10))
        
        lbl_content = ctk.CTkLabel(frame, text=content, font=ctk.CTkFont(size=13), text_color="#d1d5db", wraplength=400)
        lbl_content.pack(expand=True, fill="both", pady=(0, 15))
        
        btn = ctk.CTkButton(dialog, text="ĐỒNG Ý", command=dialog.destroy,
                            width=100, height=32, fg_color=title_color, hover_color="#2563eb" if not is_error else "#dc2626",
                            font=ctk.CTkFont(weight="bold"))
        btn.pack(pady=(0, 15))

    def show_confirm_dialog(self, title, content, on_confirm):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("450x220")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = (sw / 2) - (450 / 2)
        y = (sh / 2) - (220 / 2)
        dialog.geometry(f"450x220+{int(x)}+{int(y)}")
        dialog.configure(fg_color="#2b2b2b")
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=25, pady=20)
        
        lbl_title = ctk.CTkLabel(frame, text=title.upper(), font=ctk.CTkFont(size=16, weight="bold"), text_color="#fbbf24")
        lbl_title.pack(pady=(0, 10))
        
        lbl_content = ctk.CTkLabel(frame, text=content, font=ctk.CTkFont(size=13), text_color="#d1d5db", wraplength=400)
        lbl_content.pack(expand=True, fill="both", pady=(0, 15))
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(0, 15))
        
        def handle_confirm():
            dialog.destroy()
            on_confirm()
            
        yes_btn = ctk.CTkButton(btn_frame, text="ĐỒNG Ý", command=handle_confirm,
                                 fg_color="#ef4444", hover_color="#dc2626", width=100, height=32,
                                 font=ctk.CTkFont(weight="bold"))
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(btn_frame, text="HỦY BỎ", command=dialog.destroy,
                               fg_color="#4b5563", hover_color="#374151", width=100, height=32,
                               font=ctk.CTkFont(weight="bold"))
        no_btn.pack(side="left", padx=10)
