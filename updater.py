import os
import sys
import subprocess
import urllib.request
import json
import time
import threading
import tempfile
import ctypes

class UpdaterMixin:
    def check_for_updates_manual(self):
        import threading
        threading.Thread(target=self.check_for_updates, kwargs={"manual": True}, daemon=True).start()

    def check_for_updates(self, manual=False):
        try:
            from main import VERSION, UPDATE_URL
        except ImportError:
            VERSION = "1.7.0"
            UPDATE_URL = "https://raw.githubusercontent.com/auhsuai/Word-Pro/main/version.json"

        try:
            nocache_url = f"{UPDATE_URL}?t={int(time.time())}"
            req = urllib.request.Request(nocache_url, headers={'User-Agent': 'WordPro-Updater'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                remote_version = data.get("version", VERSION)
                download_url = data.get("download_url", "")
                changelog = data.get("changelog", "Bản cập nhật quan trọng.")
                if remote_version > VERSION:
                    if hasattr(self, 'show_update_popup'):
                        self.show_update_popup(remote_version, download_url, changelog)
                elif manual:
                    from tkinter import messagebox
                    messagebox.showinfo("Cập nhật", f"Bạn đang dùng bản mới nhất (v{VERSION}).")
        except Exception as e:
            if manual:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", f"Không thể kết nối máy chủ: {e}")

    def start_smart_update(self, url, dialog_window):
        thread = threading.Thread(target=self._download_thread, args=(url, dialog_window))
        thread.daemon = True
        thread.start()

    def _download_thread(self, url, dialog_window):
        try:
            temp_dir = tempfile.gettempdir()
            setup_path = os.path.join(temp_dir, "WordPro_Update_Setup.exe")
            req = urllib.request.Request(url, headers={'User-Agent': 'WordPro-Updater'})
            with urllib.request.urlopen(req) as response:
                total_size = int(response.info().get('Content-Length', 0))
                downloaded = 0
                with open(setup_path, 'wb') as f:
                    while True:
                        buffer = response.read(64 * 1024)
                        if not buffer: break
                        downloaded += len(buffer)
                        f.write(buffer)
                        if total_size > 0:
                            percent = int(downloaded * 100 / total_size)
                            self.after(10, lambda p=percent: dialog_window.update_progress(p))
            self.after(100, lambda: self._run_installer_and_exit(setup_path))
        except Exception as e:
            self.after(10, lambda: dialog_window.show_error(str(e)))

    def _run_installer_and_exit(self, path):
        """Chạy bộ cài và ÉP BUỘC cài đè vào thư mục hiện tại"""
        try:
            # Lấy chính xác thư mục mà file .exe đang chạy
            if getattr(sys, 'frozen', False):
                # Nếu chạy từ file .exe đã build
                install_dir = os.path.dirname(sys.executable)
            else:
                # Nếu chạy từ code python
                install_dir = os.getcwd()

            # Các tham số quan trọng:
            # /DIR="..." : Ép buộc cài vào đúng thư mục này
            # /SILENT : Hiện thanh tiến trình, tự chạy
            # /CLOSEAPPLICATIONS : Đóng app cũ
            # /RESTARTAPPLICATIONS : Khởi động lại app
            params = f'/SILENT /DIR="{install_dir}" /SUPPRESSMSGBOXES /RESTARTAPPLICATIONS /CLOSEAPPLICATIONS /FORCECLOSEAPPLICATIONS /SP-'
            
            # Chạy với quyền Admin để có thể ghi đè file trong mọi thư mục
            ctypes.windll.shell32.ShellExecuteW(None, "runas", path, params, None, 1)
            
            # Thoát ngay lập tức
            os._exit(0)
        except Exception as e:
            os.startfile(path)
            os._exit(0)
