from io import BytesIO
from PIL import ImageTk, Image
from yt_dlp import YoutubeDL
import yt_dlp
import requests

url = None

def download(output_path=None):
    global url
    if not url:
        raise ValueError("URL not set")
    
    if output_path is None:
        output_path = '%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'ffmpeg_location': './bin/ffmpeg.exe',
        'postprocessor_args': [
        
            # Copy video stream (no re-encode)
            '-c:v', 'copy',

            # Force audio to be AAC
            '-c:a', 'aac',
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def set_url(textInput):
    global url
    if (textInput):
        url = textInput

def get_video_info():
    global url
    if not url:
        raise ValueError("URL is not set. Please set the URL before fetching video info.")
    
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown Title'),
            'thumbnail': info.get('thumbnail'),
            'uploader': info.get('uploader', 'Unknown Uploader'),
            'upload_date': info.get('upload_date', 'Unknown Date'),
            'duration': info.get('duration', 0),
        }
    
def get_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    img_data = Image.open(BytesIO(response.content)).resize((320, 180))
    img = ImageTk.PhotoImage(img_data)
    return img