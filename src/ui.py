from PySide6.QtWidgets import (QApplication, QMessageBox, QFileDialog, 
                              QLabel, QPushButton, QLineEdit, QVBoxLayout, QFrame, QProgressBar)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QPixmap, QIcon
from PIL import ImageQt
import os
import io
import sys
import src.scrap as scrap

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class YoutubeDownloaderApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        ui_file_path = resource_path("src/test.ui")
        loading_dialog_path = resource_path("src/loading-dialog.ui")
        loader = QUiLoader()

        # ---- Load Main Window ----
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        self.window.setWindowIcon(QIcon(resource_path("assets/icons/youtube-icon.ico")))
        ui_file.close()

        # ---- Load Loading Dialog ----
        loading_dialog_file = QFile(loading_dialog_path)
        loading_dialog_file.open(QFile.ReadOnly)
        self.loading_dialog = loader.load(loading_dialog_file, self.window)  # parent = main window
        loading_dialog_file.close()

        # Disable close button
        self.loading_dialog.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint
        )

        # Widgets from main window
        self.entry = self.window.findChild(QLineEdit, "entry")
        self.submit_button = self.window.findChild(QPushButton, "submitButton")

        self.redo_button = self.window.findChild(QPushButton, "redoButton")
        self.redo_button.setIcon(QIcon(resource_path("assets/icons/redo.svg")))

        self.entry_label = self.window.findChild(QLabel, "entryLabel")
        self.title_label = self.window.findChild(QLabel, "title")
        self.thumb_frame = self.window.findChild(QFrame, "thumbFrame")
        self.thumb_label = self.window.findChild(QLabel, "thumbLabel")
        self.video_title_label = self.window.findChild(QLabel, "videoTitleLabel")

        # Widgets from loading dialog
        self.progress_bar = self.loading_dialog.findChild(QProgressBar, "progressBar")
        self.loading_console = self.loading_dialog.findChild(QLabel, "loadingConsole")

        # Get the parent widget that contains the preview elements
        self.video_preview_container = self.thumb_frame.parent()
        
        # Create a new layout for the container if it doesn't have one
        if not self.video_preview_container.layout():
            self.video_preview_container.setLayout(QVBoxLayout())
        
        # Initially hide the entire container and the redo button
        self.video_preview_container.hide()
        self.redo_button.hide()
        
        # Store original size policy
        self.original_size_policy = self.video_preview_container.sizePolicy()
        
        # Set size policy to ignore space when hidden
        new_size_policy = self.video_preview_container.sizePolicy()
        new_size_policy.setRetainSizeWhenHidden(False)
        self.video_preview_container.setSizePolicy(new_size_policy)

        # Connect button
        self.submit_button.clicked.connect(self.on_submit)
        self.redo_button.clicked.connect(self.cleanup)

        # Workers
        self.worker = None

    def on_submit(self):
        url = self.entry.text()
        if not url:
            QMessageBox.critical(self.window, "Error", "Please enter a URL!")
            return

        try:
            scrap.set_url(url)
            video_data = scrap.get_video_info()
            self.display_thumbnail(video_data)
            self.submit_button.setText("Download")
            self.submit_button.clicked.disconnect()
            self.submit_button.clicked.connect(self.download_video)
            self.video_preview_container.show()
            self.redo_button.show()

        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to retrieve video: {e}")

    def display_thumbnail(self, video_data):
        try:
            thumbnail_url = video_data['thumbnail']
            img = scrap.get_thumbnail(thumbnail_url)
            qt_img = ImageQt.ImageQt(img)
            pixmap = QPixmap.fromImage(qt_img)
            self.thumb_label.setPixmap(pixmap)
            self.video_title_label.setText(video_data['title'])
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Failed to load thumbnail: {e}")
            print(f"Error loading thumbnail: {e}")

    def download_video(self):
        try:
            video_data = scrap.get_video_info()
            suggested_name = video_data['title'].replace('/', '_').replace('\\', '_') + ".mp4"

            file_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Save Video As",
                suggested_name,
                "MP4 files (*.mp4)"
            )

            if file_path:
                # Show loading dialog
                self.progress_bar.setRange(0, 0)
                self.loading_console.setText("Downloading...")
                self.loading_dialog.setWindowTitle("Please wait")
                self.loading_dialog.show()

                self.worker = scrap.download(self.window, video_data['url'], file_path)
                self.worker.finished.connect(lambda: (
                    self.loading_dialog.close(),
                    QMessageBox.information(self.window, "Done", "Download complete!")
                ))
                self.worker.error.connect(lambda e: QMessageBox.critical(self.window, "Error", e))
                self.worker.finished.connect(self.cleanup)
                self.worker.start()

        except Exception as e:
            print("DownloadVideoError: " + str(e))
            QMessageBox.critical(self.window, "Error", str(e))

    def cleanup(self):
        self.entry.setText("")
        self.thumb_label.clear()
        self.video_title_label.clear()
        self.submit_button.setText("Submit")
        self.submit_button.clicked.disconnect()
        self.submit_button.clicked.connect(self.on_submit)
        self.video_preview_container.hide()
        self.redo_button.hide()
        self.worker = None

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())