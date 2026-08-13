import requests
from PyQt5.QtCore import QThread, pyqtSignal

class VersionChecker(QThread):
    update_available = pyqtSignal(str)
    error = pyqtSignal(str)

    CURRENT_VERSION = "1.0.0"

    def run(self):
        try:
            response = requests.get("https://api.github.com/repos/Faglig/sixseven/releases/latest", timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").lstrip("v")
                if latest_version and latest_version != self.CURRENT_VERSION:
                    self.update_available.emit(latest_version)
        except Exception as e:
            self.error.emit(str(e))