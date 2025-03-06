import os
import yt_dlp
from django.shortcuts import render

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

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)

                # Extract top 3 video formats
                video_formats = sorted(
                    [
                        {"url": fmt["url"], "resolution": fmt.get("height", 0)}
                        for fmt in info["formats"]
                        if "url" in fmt and fmt.get("vcodec") != "none" and fmt.get("acodec") != "none"
                    ],
                    key=lambda x: x["resolution"], reverse=True
                )[:3]

                context["title"] = info.get("title")
                context["thumbnail"] = info.get("thumbnail")
                context["video_formats"] = video_formats  # Returns Top 3

            except Exception as e:
                context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
