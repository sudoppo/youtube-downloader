from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from PySide6.QtCore import QThread, Signal, QObject
import yt_dlp

class YoutubeInfoWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    
    def __init__(self, url):
        super().__init__()
        self.url = url

        
    def run(self):
        try:
            ydl_opts = {'quiet': True, 'skip_download': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)

            result = {
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail'),
                'uploader': info.get('uploader', 'Unknown Uploader'),
                'upload_date': info.get('upload_date', 'Unknown Date'),
                'duration': info.get('duration', 0),
                'url': info.get('webpage_url', self.url),
            }
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))