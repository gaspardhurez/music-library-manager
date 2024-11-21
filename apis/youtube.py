from googleapiclient.discovery import build
import json
from pytube import Playlist
import yt_dlp




def load_youtube_tracks(playlist_url):

    # Options pour l'extraction des métadonnées
    ydl_opts = {
        'quiet': True,           # Désactiver les logs détaillés
        'extract_flat': True,    # N'extrait que les métadonnées, pas les vidéos
    }

    # Extraire les métadonnées des vidéos de la playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)

    # Récupérer les informations des vidéos
    songs = [
        {
            'title': video['title'] + ' / ' + video.get('uploader'),
            'artists': '',
            'streaming_id': video['id'],
            'source': 'youtube'
        }
        for video in playlist_info['entries']
    ]

    return songs

def remove_tracks_from_youtube(tracklist):
    pass