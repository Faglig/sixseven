# file: network_worker.py

import requests
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadWorker(QThread):
    data_loaded = pyqtSignal(object)  # object - может быть str, dict, list
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            
            if 'json' in content_type:
                data = response.json()
            else:
                # Для .md файлов - просто текст
                data = response.text
            
            self.data_loaded.emit(data)
        except Exception as e:
            self.error.emit(str(e))