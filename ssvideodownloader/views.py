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
    "format": "bestvideo+bestaudio/best",  # Prioritize best video + audio
    "merge_output_format": "mp4"  # Merge into a single MP4 file
                    }
                        # Bypass region restrictions# Public proxy (change if needed)# Fetch the best available format
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)

                    # Extract downloadable MP4 formats
                    mp4_formats = [
                        {
                            "url": fmt["url"],
                            "resolution": fmt.get("height", 0),  # Default to 0 if missing
                        }
                        for fmt in info.get("formats", [])
                        if "url" in fmt and fmt["ext"] == "mp4"
                    ]

                    # Sort resolutions (highest first), handling cases where "height" might be missing
                    mp4_formats = sorted(mp4_formats, key=lambda x: int(x["resolution"]) if isinstance(x["resolution"], int) else 0, reverse=True)[:3]

                    context["title"] = info.get("title")
                    context["thumbnail"] = info.get("thumbnail")
                    context["video_formats"] = mp4_formats  # Store MP4 download links

                except Exception as e:
                    context["error"] = f"Error: {str(e)}"

    return render(request, "download.html", context)
