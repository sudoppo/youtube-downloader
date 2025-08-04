from tkinter import *
from tkinter import messagebox
from tkinter import filedialog 
import scrap

# Constants
WINDOW_TITLE = "Youtube Downloader"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FONT_TITLE = ("Arial", 18, "bold")
FONT_LABEL = ("Arial", 13)

# Global Variables
frame = None
thumbnail_label = None
video_title_label = None
selected_thumbnail = None
download_button = None
entry = None

def setup_root() -> Tk:
    root = Tk()
    root.title(WINDOW_TITLE)
    x_pos = (root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
    y_pos = (root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_pos}+{y_pos}")
    return root

def create_ui() -> Tk:
    global root, frame, entry, download_button
    root = setup_root()
    frame = Frame(root)
    frame.pack(expand=True, fill=BOTH)  # Center the frame

    Label(frame, text="Youtube Downloader", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(40, 20), sticky="n")
    Label(frame, text="Enter a Youtube Link:", font=("Arial", 13)).grid(row=1, column=0, pady=(0, 10), sticky="e")
    entry = Entry(frame, width=40, font=("Arial", 12))
    entry.grid(row=1, column=1, pady=(0, 10), sticky="w")

    download_button = Button(frame, text="Submit", command=lambda: send_url(entry.get()))
    download_button.grid(row=4, column=0, columnspan=2, pady=(20, 0))

    # Center widgets in the frame
    for col in (0, 1):
        frame.grid_columnconfigure(col, weight=1)
    for row in range(4):  # rows 0–3
        frame.grid_rowconfigure(row, weight=0)
    return root

def display_thumbnail(video_data) -> None:
    global selected_thumbnail, frame, thumbnail_label, video_title_label

    thumbnail_url = video_data['thumbnail']
    try:
        selected_thumbnail = scrap.get_thumbnail(thumbnail_url)
        thumbnail_label = Label(frame, image=selected_thumbnail)
        thumbnail_label.image = selected_thumbnail  # Keep a reference to avoid garbage collection
        thumbnail_label.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        video_title_label = Label(frame, text=f"{video_data['title']}", font=("Arial", 16, "bold"))
        video_title_label.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="n")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load thumbnail: {str(e)}")
    
def send_url(url: str) -> None:
    global root
    if not url:
        messagebox.showerror("Error", "Please enter a URL!")
        return
    scrap.set_url(url)
    video_data = scrap.get_video_info()
    display_thumbnail(video_data)
    download_button.config(text="Download", command=download_video)


def download_video() -> None:
    global entry, thumbnail_label, video_title_label
    try:
        video_data = scrap.get_video_info()
        suggested_name = video_data['title'].replace('/', '_').replace('\\', '_')

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4", 
            filetypes=[("MP4 files", "*.mp4")], 
            title="Save Video As",
            initialfile= suggested_name + '.mp4'
        )
        
        if file_path:
            scrap.download(file_path)
            entry.delete(0, END)

            if thumbnail_label:
                thumbnail_label.destroy()
                thumbnail_label = None
            
            if video_title_label:
                video_title_label.destroy()
                video_title_label = None

            # Reset the button to allow new input
            download_button.config(text="Submit", command=lambda: send_url(entry.get()))
            messagebox.showinfo("Success", "Download Completed!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    create_ui().mainloop()