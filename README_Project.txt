SI507 Final Project
Zi Wang

README for Spotify Artist Network Project

Overview & Graph Structure
--------------------------

The Spotify Artist Network project is an interactive Python program that allows users to explore artist connections, popular songs and playlist recommendations using a graph-based network constructed from Spotify playlist data.

My graph is designed to store relationships between artists, where each artist is represented as a node in the adjacency list. A node is a tuple containing the artist's ID, name, and Spotify URL. Edges between nodes represent their co-occurrence in playlists, with weights indicating the number of playlists where the two artists appear together. Artists that frequently co-occur in playlists have stronger connections (higher weights).

The program offers a text-based interface for user interactions.


Interactions
------------

Users can interact with the program through a series of prompts:

1.Find Most Connected Artists:
Prompt: Enter the number of top N most connected/popular artists in 2024 you want to know: [num]
Response: The program displays the top N artists with the highest co-occurrence connections in the graph.

2.Find Artists with the Highest Co-occurrence:
Prompt: Do you want to know the two artists with the highest co-occurrence? (Yes/No):
Response: The program identifies and displays the two artists that co-occur most often in playlists.

3.Explore Songs and Albums of an Artist:
Prompt: Enter an artist's name to explore their popular songs and albums: [name]
Response: The program displays the top three songs and associated albums for the entered artist.

4.Find Related Artists:
Prompt: Do you want recommendations of 3 artists that co-occur with [artist name]? (Yes/No):
Response: The program displays three artists that frequently co-occur with the entered artist. The url to each artist's Spotify profile is provided as well.

5.Find Common Playlists:
Prompt: Choose a related artist to see common playlists: [name]
Response: The program displays up to three playlists containing both the entered artist and the selected related artist.


Special Instructions
----------------------

The only required package is spotipy. However, this package is only used in dataset.py for fetching data from the Spotify API. Since all necessary data is already stored in spotify_data.json, no additional packages are required to run the main program.



