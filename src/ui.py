from tkinter import *
from tkinter import messagebox, filedialog
import src.scrap as scrap

class YoutubeDownloaderApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry(self.center_window(800, 600))

        # UI Components
        self.frame = Frame(self.root)
        self.entry = None
        self.download_button = None
        self.thumbnail_label = None
        self.video_title_label = None
        self.selected_thumbnail = None

        self.create_ui()

    def center_window(self, width, height):
        x_pos = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y_pos = (self.root.winfo_screenheight() // 2) - (height // 2)
        return f"{width}x{height}+{x_pos}+{y_pos}"
    
    def create_ui(self):
        self.frame.pack(expand=True, fill=BOTH)

        Label(self.frame, text="Youtube Downloader", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(40, 20), sticky="n")
        Label(self.frame, text="Enter a Youtube Link:", font=("Arial", 13)).grid(row=1, column=0, pady=(0, 10), sticky="e")
        
        self.entry = Entry(self.frame, width=40, font=("Arial", 12))
        self.entry.grid(row=1, column=1, pady=(0, 10), sticky="w")

        self.download_button = Button(self.frame, text="Submit", command=self.on_submit)
        self.download_button.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        for col in (0, 1):
            self.frame.grid_columnconfigure(col, weight=1)
        for row in range(4):
            self.frame.grid_rowconfigure(row, weight=0)

    def on_submit(self):
        url = self.entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL!")
            return

        try:
            scrap.set_url(url)
            video_data = scrap.get_video_info()
            self.display_thumbnail(video_data)
            self.download_button.config(text="Download", command=self.download_video)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve video: {e}")

    def display_thumbnail(self, video_data):
        if self.thumbnail_label:
            self.thumbnail_label.destroy()
        if self.video_title_label:
            self.video_title_label.destroy()

        try:
            thumbnail_url = video_data['thumbnail']
            self.selected_thumbnail = scrap.get_thumbnail(thumbnail_url)
            
            self.thumbnail_label = Label(self.frame, image=self.selected_thumbnail)
            self.thumbnail_label.image = self.selected_thumbnail  # avoid GC
            self.thumbnail_label.grid(row=2, column=0, columnspan=2, pady=(10, 10))

            self.video_title_label = Label(self.frame, text=video_data['title'], font=("Arial", 16, "bold"))
            self.video_title_label.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load thumbnail: {e}")

    def download_video(self):
        try:
            video_data = scrap.get_video_info()
            suggested_name = video_data['title'].replace('/', '_').replace('\\', '_')

            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4", 
                filetypes=[("MP4 files", "*.mp4")], 
                title="Save Video As",
                initialfile=suggested_name + '.mp4'
            )

            if file_path:
                scrap.download(file_path)
                self.cleanup_after_download()
                messagebox.showinfo("Success", "Download Completed!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cleanup_after_download(self):
        self.entry.delete(0, END)
        if self.thumbnail_label:
            self.thumbnail_label.destroy()
            self.thumbnail_label = None
        if self.video_title_label:
            self.video_title_label.destroy()
            self.video_title_label = None

        self.download_button.config(text="Submit", command=self.on_submit)