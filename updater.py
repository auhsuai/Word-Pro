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
    @staticmethod
    def _so_sanh_phien_ban(v1, v2):
        """So sánh 2 chuỗi version theo semantic (trả về True nếu v1 > v2)"""
        try:
            p1 = [int(x) for x in v1.split('.')]
            p2 = [int(x) for x in v2.split('.')]
            return p1 > p2
        except (ValueError, AttributeError):
            return v1 > v2

    def check_for_updates_manual(self):
        import threading
        threading.Thread(target=self.check_for_updates, kwargs={"manual": True}, daemon=True).start()

    def check_for_updates(self, manual=False):
        phien_ban = getattr(self, 'phien_ban', '1.8.3')
        duong_dan = getattr(self, 'duong_dan_cap_nhat',
                            'https://raw.githubusercontent.com/auhsuai/Word-Pro/main/version.json')

        try:
            nocache_url = f"{duong_dan}?t={int(time.time())}"
            req = urllib.request.Request(nocache_url, headers={'User-Agent': 'WordPro-Updater'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                remote_version = data.get("version", phien_ban)
                download_url = data.get("download_url", "")
                changelog = data.get("changelog", "Bản cập nhật quan trọng.")
                if self._so_sanh_phien_ban(remote_version, phien_ban):
                    if hasattr(self, 'show_update_popup'):
                        self.after(0, lambda rv=remote_version, du=download_url, cl=changelog:
                                   self.show_update_popup(rv, du, cl))
                elif manual:
                    self.after(0, lambda: self.show_message_dialog(
                        "Cập nhật", f"Bạn đang dùng bản mới nhất (v{phien_ban})."))
        except Exception as e:
            if manual:
                self.after(0, lambda err=str(e): self.show_message_dialog(
                    "Lỗi", f"Không thể kết nối máy chủ: {err}", is_error=True))

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
        # Lấy thư mục cài đặt trước để đảm bảo luôn có giá trị
        if getattr(sys, 'frozen', False):
            install_dir = os.path.dirname(sys.executable)
        else:
            install_dir = os.getcwd()

        # Các tham số quan trọng:
        # /DIR="..." : Ép buộc cài vào đúng thư mục này
        # /SILENT : Hiện thanh tiến trình, tự chạy
        # /CLOSEAPPLICATIONS : Đóng app cũ
        # /RESTARTAPPLICATIONS : Khởi động lại app
        params = f'/SILENT /DIR="{install_dir}" /SUPPRESSMSGBOXES /RESTARTAPPLICATIONS /CLOSEAPPLICATIONS /FORCECLOSEAPPLICATIONS /SP-'

        try:
            # Chạy với quyền Admin để có thể ghi đè file trong mọi thư mục
            ctypes.windll.shell32.ShellExecuteW(None, "runas", path, params, None, 1)
        except Exception:
            # Fallback: chạy không cần admin nhưng VẪN GIỮ params tránh cài sai thư mục
            try:
                subprocess.Popen(f'"{path}" {params}', shell=True)
            except Exception:
                os.startfile(path)

        # Thoát ngay lập tức
        os._exit(0)
