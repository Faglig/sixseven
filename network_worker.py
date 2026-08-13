import requests
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadWorker(QThread):
    data_loaded = pyqtSignal(object)   # <-- object вместо dict
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.data_loaded.emit(data)
        except Exception as e:
            self.error.emit(str(e))