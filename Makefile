.PHONY: build clean installer

build:
	pyinstaller --onefile --noconsole \
	--name "YouTube Downloader" \
	--icon "assets/youtube-icon.ico" \
	--add-binary "bin/ffmpeg.exe;bin" \
	--add-binary "bin/ffprobe.exe;bin" \
	--add-binary "bin/ffplay.exe;bin" \
	--add-data "src/test.ui;src" \
	--collect-all yt_dlp \
	--hidden-import "pkg_resources" \
	--hidden-import "yt_dlp.compat" \
	--hidden-import "yt_dlp.utils" \
	--upx-dir "bin/upx" \
	--runtime-tmpdir "." \
	main.py
	"C:\Program Files (x86)\Inno Setup 6\iscc.exe" youtube-downloader.iss

clean:
	rm -rf build dist __pycache__ *.spec