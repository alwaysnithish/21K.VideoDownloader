from django.shortcuts import render
import yt_dlp
import os

# Define cookies file path (single directory reference)
COOKIES_DIR = os.path.join(os.path.dirname(__file__), "..", "cookies")

def get_cookies_file(url):
    """Returns the appropriate cookies file for the platform."""
    cookies_map = {
        "youtube.com": "www.youtube.com_cookies.txt",
        "instagram.com": "www.instagram.com_cookies.txt",
        "facebook.com": "www.facebook.com_cookies.txt",
        "x.com": "www.x.com_cookies.txt",
        "twitter.com": "www.x.com_cookies.txt",  # Twitter is now X
    }

    for domain, file in cookies_map.items():
        if domain in url:
            return os.path.join(COOKIES_DIR, file)

    return None  # No cookies file for unsupported platforms

def home(request):
    context = {}

    if request.method == "POST":
        if "fetch_info" in request.POST:
            video_url = request.POST.get("url")
            if not video_url:
                context["error"] = "URL is required"
            else:
                try:
                    # Get appropriate cookies file
                    cookies_file = get_cookies_file(video_url)
                    
                    ydl_opts = {
                        "format": "bv*+ba/b",  # Best video + best audio, fallback to best
                        "merge_output_format": "mp4",  # Ensure MP4 output
                        "postprocessors": [
                            {"key": "FFmpegMerger"},  # Merges video & audio
                        ],
                    }

                    # Add cookies option if available
                    if cookies_file and os.path.exists(cookies_file):
                        ydl_opts["cookiefile"] = cookies_file

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)

                    # Extract video formats with both video & audio (MP4)
                    mp4_formats = [
                        {
                            "url": fmt["url"],
                            "resolution": fmt.get("height", 0),  # Default 0 if missing
                        }
                        for fmt in info.get("formats", [])
                        if "url" in fmt and fmt.get("vcodec") != "none" and fmt.get("acodec") != "none"
                    ]

                    # Sort resolutions (highest first) and get **top 3 only**
                    mp4_formats = sorted(mp4_formats, key=lambda x: x["resolution"], reverse=True)[:3]

                    context["title"] = info.get("title")
                    context["thumbnail"] = info.get("thumbnail")
                    context["video_formats"] = mp4_formats  # **Always returns top 3**

                except Exception as e:
                    context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
