from django.shortcuts import render
import yt_dlp

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
                        "format": "bv+ba/b",  # Best video + best audio, fallback to best
                        "merge_output_format": "mp4",  # Ensure MP4 output
                        "postprocessors": [
                            {"key": "FFmpegMerger"},  # Merges video & audio
                        ],
                    }

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

                    # Sort resolutions (highest first) and get **top 3 only**
                    mp4_formats = sorted(mp4_formats, key=lambda x: x["resolution"], reverse=True)[:3]

                    context["title"] = info.get("title")
                    context["thumbnail"] = info.get("thumbnail")
                    context["video_formats"] = mp4_formats  # **Now always returns top 3**

                except Exception as e:
                    context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
