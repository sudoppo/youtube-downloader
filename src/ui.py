from PySide6.QtWidgets import (QApplication, QMessageBox, QFileDialog, 
                              QLabel, QPushButton, QLineEdit, QVBoxLayout, QFrame)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap
from PIL import ImageQt
import sys
import src.scrap as scrap

class YoutubeDownloaderApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        loader = QUiLoader()
        ui_file = QFile("src/test.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

        # Widgets
        self.entry = self.window.findChild(QLineEdit, "entry")
        self.submit_button = self.window.findChild(QPushButton, "submitButton")
        self.entry_label = self.window.findChild(QLabel, "entryLabel")
        self.title_label = self.window.findChild(QLabel, "title")
        self.thumb_frame = self.window.findChild(QFrame, "thumbFrame")
        self.thumb_label = self.window.findChild(QLabel, "thumbLabel")
        self.video_title_label = self.window.findChild(QLabel, "videoTitleLabel")

        # Get the parent widget that contains the preview elements
        self.video_preview_container = self.thumb_frame.parent()
        
        # Create a new layout for the container if it doesn't have one
        if not self.video_preview_container.layout():
            self.video_preview_container.setLayout(QVBoxLayout())
        
        # Initially hide the entire container
        self.video_preview_container.hide()
        
        # Store original size policy
        self.original_size_policy = self.video_preview_container.sizePolicy()
        
        # Set size policy to ignore space when hidden
        new_size_policy = self.video_preview_container.sizePolicy()
        new_size_policy.setRetainSizeWhenHidden(False)
        self.video_preview_container.setSizePolicy(new_size_policy)

        # Connect button
        self.submit_button.clicked.connect(self.on_submit)

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
                scrap.download(file_path)
                QMessageBox.information(self.window, "Success", "Download completed!")

                self.entry.setText("")
                self.thumb_label.clear()
                self.video_title_label.clear()
                self.submit_button.setText("Submit")
                self.submit_button.clicked.disconnect()
                self.submit_button.clicked.connect(self.on_submit)
                self.video_preview_container.hide()

        except Exception as e:
            QMessageBox.critical(self.window, "Error", str(e))

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())