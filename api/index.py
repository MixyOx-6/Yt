import yt_dlp

def handler(request):
    url = request.args.get("url")

    if not url:
        return {
            "statusCode": 400,
            "body": {"error": "URL missing"}
        }

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'noplaylist': True,
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                return {
                    "statusCode": 500,
                    "body": {"error": "Failed to extract info"}
                }

            formats = info.get("formats", [])

            best_mp4 = None
            best_audio = None

            for f in formats:
                if (
                    f.get("ext") == "mp4"
                    and f.get("vcodec") != "none"
                    and f.get("acodec") != "none"
                ):
                    best_mp4 = f

                if f.get("vcodec") == "none" and f.get("acodec") != "none":
                    best_audio = f

            return {
                "statusCode": 200,
                "body": {
                    "title": info.get("title"),
                    "video_url": best_mp4["url"] if best_mp4 else None,
                    "audio_url": best_audio["url"] if best_audio else None
                }
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
        }
