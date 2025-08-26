from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from PySide6.QtWidgets import QMessageBox                              
from io import BytesIO
from src.workers.DownloadWorker import DownloadWorker
from PIL import ImageTk, Image
from yt_dlp import YoutubeDL
import src.workers.DownloadWorker as DownloadWorker
import yt_dlp
import requests

url = None

def download(window, url, output_path=None):
    return DownloadWorker(url, output_path)

def set_url(textInput):
    global url
    if (textInput):
        sanitized_url = sanitize_youtube_url(textInput)
        url = sanitized_url
    else:
        raise ValueError("URL is not set. Please set the URL before fetching video info.")

def get_video_info():
    global url
    
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
            'url': info.get('webpage_url', url),
        }
    
def get_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    img = Image.open(BytesIO(response.content)).resize((320, 180))
    return img

def sanitize_youtube_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if 'v' in query:
        new_query = {'v': query['v'][0]}
        parsed = parsed._replace(query=urlencode(new_query))
        return urlunparse(parsed)
    return url