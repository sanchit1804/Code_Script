import os
import sys
import yt_dlp

def download_playlist(playlist_url, download_format):
    if download_format not in ['mp3', 'mp4']:
        print("Invalid format. Choose 'mp3' or 'mp4'.")
        return

    output_dir = os.path.join("downloads", download_format)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
    }

    if download_format == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif download_format == 'mp4':
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python download_playlist.py <playlist_url> <mp3|mp4>")
        sys.exit(1)

    playlist_url = sys.argv[1]
    download_format = sys.argv[2].lower()
    download_playlist(playlist_url, download_format)

