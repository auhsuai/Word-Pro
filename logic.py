import tkinter as tk
import time
import random
from data import get_random_words, get_all_sentences

class LogicMixin:
    def load_new_text(self):
        if self.mode == "file" and hasattr(self, "custom_file_words") and self.custom_file_words:
            words = self.custom_file_words.copy()
            random.shuffle(words)
            self.target_text = " ".join(words[:100])
        elif self.mode == "mistakes":
            from data import get_mistake_words
            words = get_mistake_words(50)
            if not words:
                self.show_custom_dialog("Thông báo", "Bạn chưa có từ nào gõ sai để luyện tập!\nHãy luyện tập các chế độ khác trước.")
                self.mode_selector.set("Từ ngẫu nhiên")
                self.mode = "words"
                self.target_text = get_random_words(200, difficulty=self.difficulty, topic=self.topic)
            else:
                random.shuffle(words)
                self.target_text = " ".join(words)
        elif self.mode == "words":
            self.target_text = get_random_words(200, difficulty=self.difficulty, topic=self.topic)
        else:
            sentences = get_all_sentences()
            if self.selected_sentence_option == "Ngẫu nhiên":
                self.target_text = random.choice(sentences)
            elif self.selected_sentence_option == "Xáo trộn tất cả":
                random.shuffle(sentences)
                self.target_text = " ".join(sentences)
            else:
                try:
                    idx = int(self.selected_sentence_option.split(".")[0]) - 1
                    self.target_text = sentences[idx]
                except:
                    self.target_text = random.choice(sentences)
            
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", self.target_text)
        self.text_display.config(state="disabled")
        self.target_words = self.target_text.split()
        self.typed_words = []
        self.current_typed = ""
        self.start_time = None
        self.is_running = False
        self.total_typed = 0
        self.correct_chars = 0
        self.last_type_time = time.time()
        self.time_left = self.time_limit
        self.can_undo_space = False
        self.timer_label.grid()
        self.timer_label.configure(text=f"{self.time_left}s", text_color="#3b82f6")
        self.stats_frame.grid_remove()
        self.graph_canvas.grid_remove()
        self.wpm_history = []
        self.calculate_stats()
        if hasattr(self, 'timer_id') and self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Reset ô nhập liệu
        self.input_entry.delete(0, tk.END)
        self.update_display()
        self.input_entry.focus_set()

    def handle_keypress(self, event):
        """Xử lý các phím chức năng (Space, Backspace)"""
        self.check_capslock()
        
        if getattr(self, 'is_cooldown', False):
            return "break"

        if hasattr(self, "overlay_frame") and self.overlay_frame.winfo_viewable():
            self.hide_overlay()
            self.reset_test()
            return "break"

        # Bắt đầu tính giờ khi gõ phím đầu tiên
        if not self.is_running and event.char and event.char.isprintable():
            self.start_time = time.time()
            self.last_type_time = time.time()  # Reset để tránh timeout ngay lập tức
            self.is_running = True
            self.run_countdown()
            self.stats_frame.grid_remove()

        # 1. Xử lý phím BACKSPACE khi ô nhập liệu trống (để quay lại từ trước)
        if event.keysym == "BackSpace":
            if self.input_entry.get() == "" and self.can_undo_space and len(self.typed_words) > 0:
                self.current_typed = self.typed_words.pop()
                if hasattr(self, 'wpm_history') and len(self.wpm_history) > 0:
                    self.wpm_history.pop() # Xóa luôn điểm dữ liệu đã vẽ
                self.input_entry.insert(0, self.current_typed)
                self.can_undo_space = False
                self.update_display()
                return "break" # Chặn để không xóa ký tự cuối của từ vừa quay lại
            return # Để mặc định xóa ký tự trong ô nhập

        # 2. Xử lý phím SPACE (Chốt từ)
        elif event.keysym == "space":
            self.play_typing_sound("space")
            current_content = self.input_entry.get()
            
            if len(self.typed_words) < len(self.target_words):
                current_target = self.target_words[len(self.typed_words)]
                # Chỉ tính lỗi sai nếu người dùng có gõ chữ nhưng gõ sai (không phải bỏ qua từ)
                if current_content != current_target and current_content != "":
                    from data import add_mistake
                    add_mistake(current_target)
                
                self.typed_words.append(current_content)
                self.current_typed = ""
                self.input_entry.delete(0, tk.END) # Xóa ô nhập để gõ từ mới
                self.can_undo_space = True
                self.update_display()
                wpm_now, _ = self.calculate_stats()
                # Ghi lại WPM tại từng từ đã gõ
                self.wpm_history.append((len(self.typed_words), wpm_now))
                
                # Kiểm tra hoàn thành bài tập
                if len(self.typed_words) == len(self.target_words):
                    self.finish_test()
            return "break" # Chặn không cho dấu cách lọt vào ô nhập mới

        # Để các phím khác tự do trôi vào ô nhập liệu
        return

    def handle_input_change(self, *args):
        """Được gọi mỗi khi nội dung ô nhập liệu thay đổi (Hỗ trợ tốt nhất cho Unikey)"""
        if not hasattr(self, 'input_entry'): return
        
        new_content = self.input_entry.get()
        
        # Ghi nhận thời gian gõ cuối để kiểm tra inactivity
        self.last_type_time = time.time()
        
        # Cảnh báo bộ gõ (IME Warning): chỉ cảnh báo khi có chuỗi Telex thô VÀ không có ký tự Việt
        co_telex_tho = any(seq in new_content.lower() for seq in ["aw", "aa", "ee", "oo", "ow", "uw", "dd", "as", "af", "ax", "ar", "aj"])
        co_ky_tu_viet = any(ord(c) > 127 for c in new_content)
        if co_telex_tho and not co_ky_tu_viet:
            self.consecutive_ime_errors = getattr(self, "consecutive_ime_errors", 0) + 1
            if self.consecutive_ime_errors >= 3:
                if hasattr(self, "ime_toast"): self.ime_toast.grid()
                self.ime_warning_active = True
        elif co_ky_tu_viet:
            self.reset_ime_warning()
            
        # Âm thanh khi gõ (Chỉ kêu khi có thêm ký tự mới)
        if len(new_content) > len(self.current_typed):
            self.play_typing_sound("click")
        
        self.current_typed = new_content
        self.can_undo_space = False
        
        # Cập nhật hiển thị và thống kê
        self.update_display()
        self.calculate_stats()
        
        # Tự động kết thúc nếu gõ xong từ cuối cùng mà không cần Space
        if len(self.typed_words) == len(self.target_words) - 1:
            if self.current_typed == self.target_words[-1]:
                self.typed_words.append(self.current_typed)
                self.current_typed = ""
                self.finish_test()

    def update_display(self):
        if not hasattr(self, 'text_display'): return
        if not hasattr(self, 'target_words') or not self.target_words: return
        
        self.text_display.config(state="normal")
        
        current_idx = len(self.typed_words)
        # Bắt đầu hiển thị từ trước đó tối đa 5 từ để người dùng có thể thấy lỗi và sửa
        start_idx = max(0, current_idx - 5)
        # Kết thúc hiển thị ở xa để lấp đầy dòng
        end_idx = min(len(self.target_words), current_idx + 20)
        
        display_words = []
        all_typed = self.typed_words + [self.current_typed]
        
        for i in range(start_idx, end_idx):
            target_word = self.target_words[i]
            if i < len(all_typed):
                typed_word = all_typed[i]
                display_word = typed_word
                if len(typed_word) < len(target_word):
                    display_word += target_word[len(typed_word):]
                display_words.append(display_word)
            else:
                display_words.append(target_word)
        
        full_display_text = " ".join(display_words)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", full_display_text)
        
        # Thiết lập Font đo đạc
        if not hasattr(self, 'display_font'):
            from tkinter import font as tkfont
            self.display_font = tkfont.Font(family="Inter", size=28)
        f = self.display_font
        
        # Đo độ rộng của phần văn bản phía trước từ hiện tại
        left_words = display_words[:current_idx - start_idx]
        left_text = " ".join(left_words)
        
        if left_text:
            active_start_px = f.measure(left_text) + f.measure(" ")
        else:
            active_start_px = 0
            
        total_width_px = f.measure(full_display_text)
        
        char_ptr = 0
        for i in range(start_idx, end_idx):
            word_start = char_ptr
            typed_word = all_typed[i] if i < len(all_typed) else None
            target_word = self.target_words[i]
            
            if typed_word is not None:
                display_len = max(len(typed_word), len(target_word))
                for j in range(display_len):
                    char_idx = word_start + j
                    if j < len(typed_word):
                        if j < len(target_word):
                            if typed_word[j] == target_word[j]:
                                self.text_display.tag_add("correct", f"1.0 + {char_idx} chars", f"1.0 + {char_idx+1} chars")
                            else:
                                self.text_display.tag_add("incorrect", f"1.0 + {char_idx} chars", f"1.0 + {char_idx+1} chars")
                        else:
                            self.text_display.tag_add("incorrect", f"1.0 + {char_idx} chars", f"1.0 + {char_idx+1} chars")
                    else:
                        # Ký tự bị thiếu/bỏ qua khi người dùng đã chuyển sang từ tiếp theo
                        if i < len(self.typed_words):
                            self.text_display.tag_add("incorrect", f"1.0 + {char_idx} chars", f"1.0 + {char_idx+1} chars")
                
                space_idx = word_start + display_len
                if i < len(self.typed_words):
                    # Chỉ đánh dấu dấu cách là đúng nếu từ đó được gõ hoàn toàn chính xác
                    if typed_word == target_word:
                        self.text_display.tag_add("correct", f"1.0 + {space_idx} chars", f"1.0 + {space_idx+1} chars")
                    else:
                        self.text_display.tag_add("incorrect", f"1.0 + {space_idx} chars", f"1.0 + {space_idx+1} chars")
                
                # Tag từ đang gõ hiện tại
                if i == current_idx:
                    cursor_idx = word_start + len(typed_word)
                    if cursor_idx < len(full_display_text):
                        self.text_display.tag_add("current", f"1.0 + {cursor_idx} chars", f"1.0 + {cursor_idx+1} chars")
                
                char_ptr += display_len + 1
            else:
                char_ptr += len(target_word) + 1

        self.text_display.config(state="disabled")
        self.text_display.update_idletasks()
        
        # Cố định từ hiện tại ở toạ độ x=250px của widget (210px tính từ lề trong)
        target_x = 250
        if total_width_px > 0:
            scroll_offset = active_start_px - (target_x - 40)
            if scroll_offset < 0:
                fraction = 0.0
            else:
                fraction = scroll_offset / total_width_px
            self.text_display.xview_moveto(fraction)

    def run_countdown(self):
        if getattr(self, 'is_running', False) and self.time_left > 0:
            if time.time() - self.last_type_time > getattr(self, 'inactivity_limit', 15):
                self.finish_test(reason="Dừng do không hoạt động quá lâu!")
                return
            self.time_left -= 1
            self.timer_label.configure(text=f"{self.time_left}s")
            if self.time_left <= 10:
                self.timer_label.configure(text_color="#f87171")
            self.timer_id = self.after(1000, self.run_countdown)
        elif getattr(self, 'is_running', False) and self.time_left <= 0:
            self.finish_test(reason="Hết giờ!")

    def calculate_stats(self):
        self.correct_chars = 0
        self.total_typed = 0
        all_typed = getattr(self, 'typed_words', []) + [getattr(self, 'current_typed', "")]
        for i, target_word in enumerate(getattr(self, 'target_words', [])):
            if i < len(all_typed):
                typed_word = all_typed[i]
                if i < len(self.typed_words):
                    # Từ đã chốt: Tính tổng độ dài tối đa giữa từ đích và từ đã gõ + 1 dấu cách
                    self.total_typed += max(len(typed_word), len(target_word)) + 1
                else:
                    # Từ hiện tại: Chỉ tính số ký tự thực tế đang gõ
                    self.total_typed += len(typed_word)
                
                for j in range(min(len(typed_word), len(target_word))):
                    if typed_word[j] == target_word[j]:
                        self.correct_chars += 1
                if i < len(self.typed_words) and typed_word == target_word:
                    self.correct_chars += 1
        if getattr(self, 'start_time', None) is not None:
            elapsed = max(time.time() - self.start_time, 1.0)
        else:
            elapsed = 1.0
        wpm = round((self.correct_chars / 5) / (elapsed / 60))
        acc = round((self.correct_chars / max(1, self.total_typed) * 100))
        if hasattr(self, 'wpm_label'):
            self.wpm_label.configure(text=f"WPM: {wpm}")
            self.acc_label.configure(text=f"Accuracy: {acc}%")
        return wpm, acc

    def finish_test(self, reason="Hoàn thành!"):
        self.is_running = False
        if hasattr(self, 'timer_label'): self.timer_label.grid_remove()
        if hasattr(self, 'timer_id') and self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        wpm, accuracy = self.calculate_stats()
        from data import record_session
        is_new_best, current_best = record_session(wpm, accuracy, self.wpm_history)
        self.best_wpm = current_best
        if is_new_best: msg = f"KỶ LỤC MỚI: {wpm} WPM!\n(Chính xác: {accuracy}%)"
        elif reason == "Hoàn thành!": msg = f"CHÚC MỪNG!\nTốc độ: {wpm} WPM | Độ chính xác: {accuracy}%"
        else: msg = f"{reason}\nTốc độ: {wpm} WPM | Độ chính xác: {accuracy}%"
        self.show_overlay(msg, start_cooldown=True)
        if hasattr(self, 'stats_frame'):
            self.stats_frame.grid()
            self.graph_canvas.grid()
        self.draw_wpm_graph()

    def reset_test(self):
        self.load_new_text()

    # Các hàm IME warning giữ nguyên...
    def reset_ime_warning(self):
        self.consecutive_ime_errors = 0
        if hasattr(self, "ime_toast"): self.ime_toast.grid_remove()
        self.ime_warning_active = False
