from django.shortcuts import render
import yt_dlp
import os
import re

# Define the downloads directory relative to the project root
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "Download")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Ensure it exists

def sanitize_filename(filename):
    """
    Remove characters that are invalid in filenames.
    This helps prevent errors when saving files.
    """
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def home(request):
    context = {}

    if request.method == "POST":
        video_url = request.POST.get("url")
        if not video_url:
            context["error"] = "URL is required"
        else:
            try:
                ydl_opts = {
                    "format": "bv*+ba/b",  # Best video + best audio, fallback to best
                    "merge_output_format": "mp4",  # Ensure MP4 output
                    # Use a sanitized title for the output filename
                    "outtmpl": os.path.join(DOWNLOAD_DIR, sanitize_filename("%(title)s") + ".%(ext)s"),
                    "postprocessors": [
                        {"key": "FFmpegMerger"},  # Merge video and audio streams
                    ],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)

                # Build the final filename using the sanitized title
                title = info.get("title", "output")
                sanitized_title = sanitize_filename(title)
                filename = f"{sanitized_title}.mp4"
                file_path = os.path.join(DOWNLOAD_DIR, filename)

                context["title"] = title
                context["thumbnail"] = info.get("thumbnail")
                context["download_link"] = f"/downloads/{filename}"  # This URL must be served via Django's static or media settings

            except Exception as e:
                context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
