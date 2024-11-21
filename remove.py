import json, os
from tinytag import TinyTag
import pandas as pd
from apis import spotify

# Config vars
with open('config.json') as config_file:
    config = json.load(config_file)

LIBRARY_PATH = config.get('library').get('LIBRARY_PATH')
    
# Checks for songs with junk tag and remove them
def get_comments(filepath):
    try:
        tag = TinyTag.get(filepath)
        return tag.comment  
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")
        return None

def scan_files_for_junk(library_path):
    junk_files = []
    for root, _, files in os.walk(library_path):
        for file in files:
            if file.endswith(('.mp3', '.wav', '.flac')): 
                filepath = os.path.join(root, file)
                comment = get_comments(filepath)
                if comment and 'junk' in comment.lower():
                    filename = os.path.basename(filepath)
                    junk_files.append(filename)
    return junk_files



# Remove track

LIBRARY_PATH = config.get('library').get('LIBRARY_PATH')
local_df = pd.read_excel(f'{LIBRARY_PATH}/library.xlsx',)

junk_files = scan_files_for_junk(LIBRARY_PATH)

to_delete_df = local_df[local_df['filename'].isin(junk_files)]
spotify_df = to_delete_df[to_delete_df['source'] == 'spotify']
youtube_df = to_delete_df[to_delete_df['source'] == 'youtube']


# Delete from streaming 

spotify_config = config.get('spotify')
sp = spotify.load_spotify_api(spotify_config.get('SPOTIFY_CLIENT_ID'), spotify_config.get('SPOTIFY_CLIENT_SECRET'))

for _, track in spotify_df.iterrows():
    track_id = track['streaming_id']
    spotify.remove_from_spotify_playlist(sp, spotify_config.get('SPOTIFY_PLAYLIST_ID'), track_id)

for _, track in youtube_df.iterrows():
    while True: 
        response = input(f"Delete {track['title']} - {track['artists']} from YouTube, and type YES to confirm: ")
        if response.strip().upper() == "YES": 
            print(f"Confirmed: {track['title']} - {track['artists']} will be deleted from YouTube.")
            break
        else:
            print("Invalid response. Please type YES to proceed.")

# Delete file
for track in junk_files:
    file_path = LIBRARY_PATH + '/' + track
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Fichier local supprimé : {file_path}")
    else:
        print(f"Fichier introuvable : {file_path}")


# Delete from CSV
updated_local_df = local_df[~local_df['filename'].isin(junk_files)]
updated_local_df.to_excel(f'{LIBRARY_PATH}/library.xlsx', index=False)

print("Le fichier Excel a été mis à jour. Tracks supprimés.")



