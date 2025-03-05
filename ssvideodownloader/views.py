import os
import yt_dlp
from django.shortcuts import render
from django.http import FileResponse, HttpResponse

# Define the directory to store downloaded videos
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def home(request):
    video_info = None
    error_message = None

    if request.method == "POST":
        video_url = request.POST.get("video_url")

        if not video_url:
            error_message = "Please enter a video URL."
        else:
            try:
                ydl_opts = {
                    "quiet": True,
                    "skip_download": True,
                    "force_generic_extractor": False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    
                    # Extract title, thumbnail, and available formats
                    video_info = {
                        "title": info.get("title"),
                        "thumbnail": info.get("thumbnail"),
                        "formats": [
                            {
                                "format_id": fmt["format_id"],
                                "extension": fmt["ext"],
                                "resolution": fmt.get("resolution", fmt.get("height", "Audio Only")),
                                "filesize": fmt.get("filesize", "N/A"),
                            }
                            for fmt in info["formats"]
                        ],
                        "video_id": info.get("id"),
                        "url": video_url,  # Store the original URL
                    }

            except Exception as e:
                error_message = f"Error fetching video details: {str(e)}"

    return render(request, "home.html", {"video_info": video_info, "error_message": error_message})

def download_video(request, video_id, format_id):
    video_url = request.GET.get("url")  # Get original video URL

    if not video_url:
        return HttpResponse("Missing video URL.", status=400)

    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}_{format_id}.mp4")

    ydl_opts = {
        "format": format_id,
        "outtmpl": file_path,
        "quiet": True,
        "merge_output_format": "mp4",  # Ensure merged output format
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=f"{video_id}_{format_id}.mp4")

    except Exception as e:
        return HttpResponse(f"Error downloading video: {str(e)}", status=500)
