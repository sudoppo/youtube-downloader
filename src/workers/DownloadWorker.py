from PySide6.QtCore import QThread, Signal, QObject
import yt_dlp

class DownloadWorker(QThread):
    finished = Signal()
    error = Signal(str)

    def __init__(self, url, output_path=None):
        super().__init__()
        self.url = url
        self.output_path = output_path or "%(title)s.%(ext)s"

    def run(self):
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': self.output_path,
                'ffmpeg_location': './bin/ffmpeg.exe',
                'postprocessor_args': [
        
                    # Copy video stream (no re-encode)
                    '-c:v', 'copy',

                    # Force audio to be AAC
                    '-c:a', 'aac',
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished.emit()
        except Exception as ex:
            error_str = str(ex)
            print("Download Worker Error: " + error_str)
            self.error.emit(error_str)