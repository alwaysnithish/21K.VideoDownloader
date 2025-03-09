from django.shortcuts import render
import yt_dlp
import os

def home(request):
    context = {}

    if request.method == "POST":
        if "fetch_info" in request.POST:
            video_url = request.POST.get("url")
            if not video_url:
                context["error"] = "URL is required"
            else:
                try:
                    # Determine the platform based on the URL
                    if "youtube.com" in video_url or "youtu.be" in video_url:
                        cookies_file = os.path.join("cookies", "www.youtube.com_cookies.txt")
                    elif "twitter.com" in video_url or "x.com" in video_url:
                        cookies_file = os.path.join("cookies", "www.x.com_cookies.txt")
                    elif "instagram.com" in video_url:
                        cookies_file = os.path.join("cookies", "www.instagram.com_cookies.txt")
                    elif "facebook.com" in video_url:
                        cookies_file = os.path.join("cookies", "www.facebook.com_cookies.txt")
                    else:
                        cookies_file = None

                    ydl_opts = {
                        # Request best video and best audio separately
                        "format": "bestvideo+bestaudio/best",
                        # Merge video and audio into a single file
                        "merge_output_format": "mp4",
                        "postprocessors": [
                            {
                                "key": "FFmpegVideoConvertor",
                                "preferedformat": "mp4",  # Ensure output is MP4
                            },
                            {
                                "key": "FFmpegMerger",  # Merge video and audio
                            },
                        ],
                    }

                    # Add cookies file to options if it exists
                    if cookies_file and os.path.exists(cookies_file):
                        ydl_opts["cookiefile"] = cookies_file

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)

                    # Extract merged MP4 formats (both video & audio)
                    mp4_formats = [
                        {
                            "url": fmt["url"],
                            "resolution": fmt.get("height", 0),  # Default to 0 if missing
                        }
                        for fmt in info.get("formats", [])
                        if "url" in fmt and fmt.get("vcodec") != "none" and fmt.get("acodec") != "none"  # Ensure both video & audio
                    ]

                    # Sort resolutions (highest first) and get top 3 only
                    mp4_formats = sorted(mp4_formats, key=lambda x: x["resolution"], reverse=True)[:3]

                    context["title"] = info.get("title")
                    context["thumbnail"] = info.get("thumbnail")
                    context["video_formats"] = mp4_formats  # Now always returns top 3

                except Exception as e:
                    context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)

def privacypolicy(request):
    return render(request, "privacypolicy.html")
def aboutus(request):
    return render(request, "aboutus.html")

def termsandconditions(request):
    return render(request, "termsandconditions.html")
