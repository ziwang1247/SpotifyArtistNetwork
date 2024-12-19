from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json

# Set up Spotify API credentials
client_id = 'cb4eaf75acd64c9d845876d809f9e562'
client_secret = 'c07b7e8cb67443cc91fb0f2682fd98f3'

# Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Fetch playlists from Spotify
def fetch_playlists(query, limit=200):
    playlists = []
    offset = 0
    while len(playlists) < limit:
        results = sp.search(q=query, type="playlist", limit=min(50, limit - len(playlists)), offset=offset)
        if not results or 'playlists' not in results or 'items' not in results['playlists']:
            print("Unexpected API response:", results)
            break
        playlists.extend(results['playlists']['items'])
        offset += 50
        if len(results['playlists']['items']) == 0:  # No more results
            break
    return playlists

# Fetch tracks and associated artists from a Spotify playlist
def fetch_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id, limit=100)
    while results:
        for item in results['items']:
            if not item or 'track' not in item or not item['track']:
                print("Invalid track data:", item)
                continue
            track = item['track']
            if 'id' not in track or 'name' not in track or 'artists' not in track or 'album' not in track:
                print("Incomplete track data:", track)
                continue
            tracks.append({
                "track_id": track['id'],
                "name": track['name'],
                "artists": [
                    {
                        "id": artist['id'],
                        "name": artist['name'],
                        "url": artist['external_urls']['spotify'] if 'external_urls' in artist and 'spotify' in artist['external_urls'] else None
                    }
                    for artist in track['artists'] if 'id' in artist and 'name' in artist
                ],
                "album": track['album']['name'],
                "url": track['external_urls']['spotify'] if 'external_urls' in track and 'spotify' in track['external_urls'] else None
            })
        results = sp.next(results) if results and results['next'] else None
    return tracks


# Store data to a JSON file
def store_data_in_json(playlists):
    data = {"playlists": []}

    for playlist in playlists:
        if not playlist or 'id' not in playlist or 'name' not in playlist or 'external_urls' not in playlist:
            print("Invalid playlist data:", playlist)
            continue # skip invalid playlist

        playlist_info = {
            "playlist_id": playlist['id'],
            "name": playlist['name'],
            "url": playlist['external_urls']['spotify'],
            "tracks": fetch_playlist_tracks(playlist['id'])
        }
        data["playlists"].append(playlist_info)

    # Save data to JSON
    with open("spotify_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Data saved to spotify_data.json")

# Main
playlists = fetch_playlists("2024", limit=200)
store_data_in_json(playlists)
