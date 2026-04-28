from fastapi import FastAPI
from ytmusicapi import YTMusic
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ytmusic = YTMusic()

def format_results(search_results):
    cleaned_results = []
    for item in search_results:
        if 'videoId' in item:
            cleaned_results.append({
                "videoId": item['videoId'],
                "title": item.get('title', 'Unknown Title'),
                "artist": item.get('artists', [{'name': 'Unknown Artist'}])[0]['name'] if 'artists' in item else 'Unknown Artist',
                "thumbnail": item['thumbnails'][-1]['url'] if 'thumbnails' in item else ''
            })
    return cleaned_results

@app.get("/api/search")
def search_music(query: str):
    try:
        # Mencari lagu berdasarkan query
        search_results = ytmusic.search(query, filter="songs", limit=15)
        # Mengembalikan data dalam objek 'data' agar konsisten
        return {"status": "success", "data": format_results(search_results)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/play")
def get_audio_url(videoId: str):
    try:
        # Logika sederhana: arahkan ke layanan eksternal atau stream
        # Untuk implementasi penuh, biasanya butuh yt-dlp di server
        playback_url = f"https://www.youtube.com/watch?v={videoId}"
        return {"status": "success", "audio": playback_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/home")
def get_home_data():
    try:
        data = {
            "recent": format_results(ytmusic.search('lagu hits indonesia', filter="songs", limit=6)),
            "trending": format_results(ytmusic.search('trending music', filter="songs", limit=10))
        }
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
