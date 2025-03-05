from django.shortcuts import render
import yt_dlp
import os

# Define cookies file paths
COOKIES_DIR = os.path.join(os.path.dirname(__file__), "..", "cookies")

def get_cookies_file(url):
    """Returns the appropriate cookies file for the platform."""
    if "youtube.com" in url:
        path = os.path.join(COOKIES_DIR, "www.youtube.com_cookies.txt")
    elif "instagram.com" in url:
        path = os.path.join(COOKIES_DIR, "www.instagram.com_cookies.txt")
    elif "facebook.com" in url:
        path = os.path.join(COOKIES_DIR, "www.facebook.com_cookies.txt")
    elif "x.com" in url or "twitter.com" in url:
        path = os.path.join(COOKIES_DIR, "www.x.com_cookies.txt")
    else:
        path = None  # No cookies file for unsupported platforms

    print(f"🔍 [DEBUG] Using cookies file: {path}")  # Log the detected file
    return path

def home(request):
    video_url = request.GET.get("url")
    
    if not video_url:
        return render(request, "download.html", {"error": "URL is required"})

    cookies_file = get_cookies_file(video_url)  # Get cookies file for the platform

    if cookies_file and os.path.exists(cookies_file):
        print(f"✅ [DEBUG] Cookies file found: {cookies_file}")
    else:
        print(f"❌ [DEBUG] Cookies file NOT FOUND at: {cookies_file}")

    return render(request, "download.html", {"message": "Check Render logs for cookies path"})
