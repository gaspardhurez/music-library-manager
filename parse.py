import json
import pandas as pd
from apis import spotify, youtube

# Config vars
with open('config.json') as config_file:
    config = json.load(config_file)


# Parse streaming playlists
spotify_config = config.get('spotify')
youtube_config = config.get('youtube')
sp = spotify.load_spotify_api(spotify_config.get('SPOTIFY_CLIENT_ID'), spotify_config.get('SPOTIFY_CLIENT_SECRET'))
spotify_songs = spotify.load_playlist_tracks(sp, spotify_config.get('SPOTIFY_PLAYLIST_ID'))
youtube_songs = youtube.load_youtube_tracks(youtube_config.get('YOUTUBE_PLAYLIST_URL'))

streaming_songs = spotify_songs + youtube_songs
streaming_df = pd.DataFrame(streaming_songs)
streaming_df['purchase_url'] = ''
streaming_df['filename'] = ''

# Parse current local library songs
LIBRARY_PATH = config.get('library').get('LIBRARY_PATH')
local_df = pd.read_excel(f'{LIBRARY_PATH}/library.xlsx',)
print(local_df.columns)

# Check new streaming tracks
new_tracks = streaming_df[~streaming_df['streaming_id'].isin(local_df['streaming_id'])]
if not new_tracks.empty:
    local_df = pd.concat([local_df, new_tracks], ignore_index=True)

print(new_tracks)
local_df.to_excel(f'{LIBRARY_PATH}/library.xlsx', index=False)
print(local_df)





