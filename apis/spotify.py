import spotipy, json
from spotipy.oauth2 import SpotifyOAuth


def load_spotify_api(id, secret):

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=id,
        client_secret=secret,
        redirect_uri="http://localhost:8888/callback",
        scope="playlist-read-private playlist-modify-public playlist-modify-private"
    ))

    return sp

def load_playlist_tracks(sp, id):
    results = sp.playlist_items(id)['items']
    songs = []

    for result in results:
        song = {}
        song['title'] = result['track']['name']
        

        artists = []
        for artist in result['track']['artists']:
            name = artist['name']
            artists.append(name)
        song['artists'] = ', '.join(artists)
        song['streaming_id'] = result['track']['id']
        song['source'] = 'spotify'

        songs.append(song)

    return songs

def remove_from_spotify_playlist(spotify_api, playlist_id, track_id):
    try:
        spotify_api.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
        print(f"Morceau {track_id} supprimé de la playlist Spotify.")
    except Exception as e:
        print(f"Erreur lors de la suppression du morceau {track_id} : {e}")