import json
from DataStructure import ArtistGraph

# Load the JSON data
with open("spotify_data.json", "r") as f:
    data = json.load(f)

playlists = data.get("playlists", [])
artistGraph = ArtistGraph(playlists)

print("Welcome to Spotify Artist Network!")

while True:
    # Step 1: Most Connected Artists
    while True:
        try:
            topN = int(input("\nEnter the number of top N most connected/popular artists in 2024 you want to know: "))
            if topN <= 0:
                raise ValueError
            break
        except ValueError:
            print(f"Invalid input. Please try again.")

    topArtists = artistGraph.mostConnectedArtists(topN)
    print(f"\nMost Connected/Popular Artists in 2024 (Top {topN}):")
    for artist, connections in topArtists:  # artist is a tuple (artistId, artistName, artistUrl)
        print(f"{artist[1]}: {connections} connections")

    # Step 2: Highest Co-occurrence Pair
    while True:
        choice = input("\nDo you want to know the two artists with the highest co-occurrence? (Yes/No): ").strip().lower()
        if choice in ["yes", "no"]:
            break
        print("Invalid input. Please enter 'Yes' or 'No'.")

    if choice == "yes":
        bestPair, maxWeight = artistGraph.highestCoOccurrencePair()  # bestPair is a tuple: (artist, neighbor)
        if bestPair:
            artist1Info = f"{bestPair[0][1]} (Spotify URL: {bestPair[0][2]})"
            artist2Info = f"{bestPair[1][1]} (Spotify URL: {bestPair[1][2]})"
            print(f"\nThe two artists with the highest co-occurrence are {artist1Info} and {artist2Info} with {maxWeight} occurrences.")

    # Step 3: Explore Songs and Albums
    while True:
        artistNameInput = input("\nEnter an artist's name to explore their popular songs and albums: ").strip()
        artist = artistGraph.findArtistByName(artistNameInput)
        if artist:
            print(f"\nTop 3 Songs and Associated Albums for {artistNameInput}:")
            tracks = artistGraph.getTopTracksForArtist(artist[0], topN=3)
            for idx, track in enumerate(tracks, start=1):
                print(f"{idx}. Track: {track['track_name']} - Album: {track['album_name']} - URL: {track['url']}")
            break
        else:
            print(f"Artist '{artistNameInput}' not found. Please try again.")

    # Step 4: Related Artists
    while True:
        choice = input(f"\nDo you want recommendations of 3 artists that co-occur with {artistNameInput}? (Yes/No): ").strip().lower()
        if choice in ["yes", "no"]:
            break
        print("Invalid input. Please enter 'Yes' or 'No'.")

    if choice == "yes":
        relatedArtists = artistGraph.getMostRelatedArtists(artistNameInput, topN=3)
        if relatedArtists:
            print("\nTop Related Artists:")
            for idx, (relatedArtist, weight) in enumerate(relatedArtists, start=1):
                print(f"{idx}. {relatedArtist[1]} (Spotify URL: {relatedArtist[2]}) - Co-occurrences: {weight}")
        else:
            print("\nNo related artists found.")

        # Step 5: Common Playlists
        while True:
            relatedArtistName = input("\nChoose a related artist to see common playlists: ").strip()
            relatedArtist = artistGraph.findArtistByName(relatedArtistName)
            if relatedArtist:
                playlists = artistGraph.findCommonPlaylists(artist[0], relatedArtist[0], maxPlaylists=3)
                if playlists:
                    print("\nPlaylists containing both artists:")
                    for idx, playlist in enumerate(playlists, start=1):
                        print(f"{idx}. {playlist['name']} - URL: {playlist['url']}")
                else:
                    print("\nNo common playlists found.")
                break
            else:
                print(f"Artist '{relatedArtistName}' not found. Please try again.")

    # Ask if the user wants to explore another artist / restart the program
    while True:
        exploreMore = input("\nThank you! Do you want to explore another artist? (Yes/No): ").strip().lower()
        if exploreMore in ["yes", "no"]:
            break
        print("Invalid input. Please enter 'Yes' or 'No'.")

    if exploreMore != "yes":
        print("\nGoodbye! Thank you for exploring the Spotify Artist Network.")
        break
