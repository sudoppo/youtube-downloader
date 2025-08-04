from tkinter import Tk
from src.ui import YoutubeDownloaderApp

def main():
    root = Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()