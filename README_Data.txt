SI507 Final Project
Zi Wang

README for Data Sources

Spotify Web API
----------------

Spotify Web API Url: https://developer.spotify.com/documentation/web-api
Spotipy url: https://spotipy.readthedocs.io/en/2.24.0/
(Url to Spotipy, a lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform.)

Format: JSON
The fetched data is stored locally in a JSON file named spotify_data.json.

Access Method:
1.Authentication is done using Spotify's OAuth credentials (client_id and client_secret).
2.The Spotipy library is used to interact with Spotify's Web API.
3.Data is fetched using the following methods: 
	A) sp.search: to search for playlists matching the keyword "2024". 
	B) sp.playlist_tracks: to retrieve track details from each playlist.


Summary of data:
The data I accessed contains information about 200 playlists retrieved by searching with the keyword "2024". Each playlist contains about 100 tracks. 
Data stored contains: 
Playlist-level variables: playlist_id, name, url, tracks
Track-level variables: track_id, name, album, url, artists
Artist-level variables: id, name, url



