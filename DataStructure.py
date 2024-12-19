class ArtistGraph:
    """
    A class to analyze artist connections in a network based on playlist co-occurrences.

    Parameters
    ----------
    playlists : list
        A list of playlists containing tracks and artist information.

    Attributes
    ----------
    playlists : list
        A list of playlists containing tracks and artist information.

    adjList : dict
        Adjacency list where:
        - Keys: Tuples representing artists (ID, name, URL)
        - Values: Dictionaries with connected artists and co-occurrence weights.
          Example:
          {
              ("1", "Drake", "spotify_url"): {
                  ("2", "The Weeknd", "spotify_url"): 10,
                  ("3", "Post Malone", "spotify_url"): 5
              },
              ...
          }

    Methods
    -------
    generateAdjList(playlists)
        Constructs the adjacency list from the provided playlists.

    mostConnectedArtists(topN)
        Finds the top N most connected artists based on co-occurrence weights.

    highestCoOccurrencePair()
        Identifies the pair of artists with the highest co-occurrence weight.

    getMostRelatedArtists(artistName, topN)
        Retrieves the most related artists to a given artist based on co-occurrence weights.

    findCommonPlaylists(artist1Id, artist2Id, maxPlaylists)
        Finds playlists where two specified artists co-occur.

    getTopTracksForArtist(artistId, topN)
        Gets the top tracks and associated albums for a given artist.

    findArtistByName(artistName)
        Finds an artist tuple by their name.
    """

    def __init__(self, playlists):
        """
        Constructs all the necessary attributes for the ArtistGraph object.

        Parameters
        ----------
        playlists : list
            A list of playlists containing tracks and artist information.
        """
        self.playlists = playlists
        self.adjList = {}  # Initialize the adjacency list as a dictionary
        self.generateAdjList(playlists)  # Populate the adjacency list from playlists

    def generateAdjList(self, playlists):
        """
        Constructs the adjacency list from the provided playlists.

        Artists are represented as nodes, and co-occurrences in playlists 
        are represented as weighted edges.

        Parameters
        ----------
        playlists : list
            A list of playlists containing tracks and artist information.

        Returns
        -------
        None
        """
        for playlist in playlists:
            trackList = playlist.get('tracks', [])
            artistSet = set()  # Create a set to store unique artists in this playlist

            # Collect all artists in the current playlist
            for track in trackList:
                for artist in track['artists']:
                    artistId = artist['id']
                    artistName = artist['name']
                    artistUrl = artist['url']
                    if artistId and artistName:
                        artistSet.add((artistId, artistName, artistUrl))

            # Create adjacency list edges for co-occurring artists
            artistList = list(artistSet)  # Convert set to a list for pairing
            for i in range(len(artistList)):
                for j in range(i + 1, len(artistList)):
                    artist1 = artistList[i]
                    artist2 = artistList[j]

                    # Ensure both artists exist in the adjacency list
                    if artist1 not in self.adjList:
                        self.adjList[artist1] = {}
                    if artist2 not in self.adjList[artist1]:
                        self.adjList[artist1][artist2] = 0

                    # Increment the co-occurrence weight for the edge
                    self.adjList[artist1][artist2] += 1

                    # Repeat for the reverse direction
                    if artist2 not in self.adjList:
                        self.adjList[artist2] = {}
                    if artist1 not in self.adjList[artist2]:
                        self.adjList[artist2][artist1] = 0

                    # Increment the reverse co-occurrence weight
                    self.adjList[artist2][artist1] += 1

    def mostConnectedArtists(self, topN=20):
        """
        Finds the top N most connected artists based on co-occurrence weights.

        Parameters
        ----------
        topN : int
            Number of top connected artists to return.

        Returns
        -------
        list
            A list of tuples containing artist information and their total connection weight.
        """
        connections = [] # example of connections: [(('1', 'Drake', 'spotify_url'), 10), (('2', 'The Weeknd', 'spotify_url'), 5)]
        for artist, neighbors in self.adjList.items():
            totalConnections = sum(neighbors.values())  # Sum all connection weights for the artist
            connections.append((artist, totalConnections))

        # Sort by total connections in descending order
        connections.sort(key=lambda x: x[1], reverse=True)
        return connections[:topN]

    def highestCoOccurrencePair(self):
        """
        Identifies the pair of artists with the highest co-occurrence weight.

        Returns
        -------
        tuple
            A tuple containing the two artists and the co-occurrence weight.
        """
        maxWeight = 0
        bestPair = None
        for artist, neighbors in self.adjList.items():
            for neighbor, weight in neighbors.items():
                if weight > maxWeight:  # Check if this pair has a higher weight
                    maxWeight = weight
                    bestPair = (artist, neighbor)  # Update the best pair
        return bestPair, maxWeight

    def getMostRelatedArtists(self, artistName, topN=3):
        """
        Retrieves the most related artists to a given artist based on co-occurrence weights.

        Parameters
        ----------
        artistName : str
            The name of the artist to find related artists for.
        topN : int
            Number of related artists to return.

        Returns
        -------
        list
            A list of related artists and their co-occurrence weights.
        """
        selectedArtist = self.findArtistByName(artistName)  # Find the artist in the adjacency list
        if not selectedArtist:  # If the artist is not found
            print(f"Artist '{artistName}' not found.")
            return []

        # Sort neighbors by co-occurrence weight
        relatedArtists = list(self.adjList[selectedArtist].items())
        relatedArtists.sort(key=lambda x: x[1], reverse=True)
        return relatedArtists[:topN]  # Return the top N related artists

    def findCommonPlaylists(self, artist1Id, artist2Id, maxPlaylists=3):
        """
        Finds playlists where two specified artists co-occur.

        Parameters
        ----------
        artist1Id : str
            ID of the first artist.
        artist2Id : str
            ID of the second artist.
        maxPlaylists : int
            Maximum number of playlists to return.

        Returns
        -------
        list
            A list of playlists where both artists co-occur.
        """
        commonPlaylists = []
        for playlist in self.playlists:  # Loop through playlists
            artistIds = set()  # Create a set of artist IDs in the playlist
            for track in playlist.get('tracks', []):
                for artist in track['artists']:
                    if artist.get('id'):
                        artistIds.add(artist['id'])  # Add artist IDs to the set

            # Check if both artists are in the same playlist
            if artist1Id in artistIds and artist2Id in artistIds:
                commonPlaylists.append(playlist)  # Add the playlist to the result

            if len(commonPlaylists) >= maxPlaylists:  # Stop if we've reached the limit
                break
        return commonPlaylists # example of commonPlaylists: [{'playlist_id': '1', 'name': 'Playlist 1', 'url': 'spotify_url', 'tracks': [...]}, ...]

    def getTopTracksForArtist(self, artistId, topN=3):
        """
        Gets the top tracks and associated albums for a given artist.

        Parameters
        ----------
        artistId : str
            The Spotify ID of the artist.
        topN : int
            Number of top tracks to return.

        Returns
        -------
        list
            A list of dictionaries containing track names, album information, and URLs.
        """
        topTracks = []
        for playlist in self.playlists:
            for track in playlist.get('tracks', []):
                if 'artists' in track:
                    for artist in track['artists']:
                        if artist.get('id') == artistId:
                            topTracks.append({
                                "track_name": track['name'],
                                "album_name": track['album'],
                                "url": track.get('url')
                            })
        return topTracks[:topN] # return the top N tracks

    def findArtistByName(self, artistName):
        """
        Finds an artist tuple by their name.

        Parameters
        ----------
        artistName : str
            Name of the artist to find.

        Returns
        -------
        tuple or None
            The artist tuple if found, else None.
        """
        for artist in self.adjList.keys():
            if artist[1].lower() == artistName.lower():  # Check if the name matches
                return artist
        return None  # Return None if not found
