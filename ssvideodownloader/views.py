from django.shortcuts import render
import yt_dlp
import os

# Define the download directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads")

# Ensure the directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def home(request):
    context = {}

    if request.method == "POST":
        if "fetch_info" in request.POST:
            video_url = request.POST.get("url")
            if not video_url:
                context["error"] = "URL is required"
            else:
                try:
                    ydl_opts = {
                        "format": "bv*+ba/b",  # Best video + best audio
                        "merge_output_format": "mp4",  # Ensure MP4 output
                        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),  # Save in the downloads directory
                        "postprocessors": [
                            {"key": "FFmpegMerger"},  # Merges video & audio
                        ],
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)  # Download the video

                    # Get the downloaded file path
                    downloaded_file = os.path.join(DOWNLOAD_DIR, f"{info['title']}.mp4")

                    context["title"] = info.get("title")
                    context["thumbnail"] = info.get("thumbnail")
                    context["download_path"] = downloaded_file  # Store the download path

                except Exception as e:
                    context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
