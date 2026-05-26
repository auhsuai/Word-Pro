import tkinter as tk

class GraphMixin:
    def draw_wpm_graph(self):
        if not hasattr(self, 'graph_canvas'): return
        
        self.graph_canvas.delete("all")
        if not hasattr(self, 'wpm_history') or not self.wpm_history: return
        
        # Sync widget to get correct size
        self.update_idletasks()
        w = self.graph_canvas.winfo_width()
        h = self.graph_canvas.winfo_height()
        if w < 100: w = 800  # Fallback
        
        points = self.wpm_history  # Mỗi phần tử: (số_từ, wpm)
        max_wpm = max([p[1] for p in points] + [40])  # Tối thiểu 40 cho scale
        max_words = points[-1][0] if points else 1  # Tổng số từ đã gõ
        
        # Margins
        mx, my = 50, 20
        gw, gh = w - 2 * mx, h - 2 * my
        
        # Vẽ lưới ngang (WPM)
        for i in range(0, max_wpm + 20, 20):
            y = h - my - (i / max_wpm * gh)
            self.graph_canvas.create_line(mx, y, w - mx, y, fill="#333333", dash=(2, 4))
            self.graph_canvas.create_text(mx - 20, y, text=str(i), fill="#666666", font=("Inter", 8))
        
        # Nhãn trục Y
        self.graph_canvas.create_text(15, h / 2, text="WPM", fill="#555555", font=("Inter", 8), angle=90)
        
        # Vẽ đường WPM
        coords = []
        for word_num, wpm in points:
            px = mx + (word_num / max_words * gw)
            py = h - my - (wpm / max_wpm * gh)
            coords.extend([px, py])
            
        if len(coords) >= 4:
            # Vùng mờ bên dưới đường
            area_coords = [mx, h - my] + coords + [coords[-2], h - my]
            self.graph_canvas.create_polygon(area_coords, fill="#1e293b", outline="")
            # Đường chính
            self.graph_canvas.create_line(coords, fill="#3b82f6", width=3, smooth=True)
            # Các điểm tròn
            for i in range(0, len(coords), 2):
                self.graph_canvas.create_oval(
                    coords[i] - 3, coords[i + 1] - 3,
                    coords[i] + 3, coords[i + 1] + 3,
                    fill="#60a5fa", outline="#1e293b"
                )
        
        # Nhãn trục X: Hiện số từ
        step = max(1, max_words // 10)  # Tối đa ~10 nhãn
        for i in range(0, max_words + 1, step):
            px = mx + (i / max_words * gw)
            self.graph_canvas.create_text(px, h - 5, text=str(i), fill="#666666", font=("Inter", 8))
        
        # Nhãn trục X
        self.graph_canvas.create_text(w / 2, h - 2, text="Số từ", fill="#555555", font=("Inter", 8))
