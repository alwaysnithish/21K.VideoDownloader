import os
import yt_dlp
from django.shortcuts import render

# Define & Ensure the downloads directory exists
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def home(request):
    context = {}

    if request.method == "POST":
        video_url = request.POST.get("url")
        if not video_url:
            context["error"] = "URL is required"
        else:
            try:
                ydl_opts = {
                    "format": "bv*+ba/b",  # Best video + best audio
                    "merge_output_format": "mp4",
                    "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
                    "postprocessors": [{"key": "FFmpegMerger"}],  # Merge video & audio
                }

                # Ensure downloads directory exists every time
                os.makedirs(DOWNLOAD_DIR, exist_ok=True)

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)

                context["title"] = info.get("title")
                context["thumbnail"] = info.get("thumbnail")
                context["download_link"] = f"/downloads/{info['title']}.mp4"

            except Exception as e:
                context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
