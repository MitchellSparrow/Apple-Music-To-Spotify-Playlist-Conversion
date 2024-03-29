import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secrets import cid, secret, apple_key_ID, apple_team_ID, apple_private_key
import pandas as pd
import sys
import spotipy.util as util
import applemusicpy
import requests
from datetime import datetime
import jwt
import json


class Spotify():

    def getSpotifyTracks(self):
        artist_name = []
        track_name = []
        popularity = []
        track_id = []

        client_credentials_manager = SpotifyClientCredentials(
            client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)

        for i in range(0, 100, 50):
            track_results = sp.search(
                q='year:2018', type='track', limit=50, offset=i)
            for i, t in enumerate(track_results['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])
                popularity.append(t['popularity'])

        track_dataframe = pd.DataFrame(
            {'artist_name': artist_name,
             'track_name': track_name,
             'track_id': track_id,
             'popularity': popularity})

        print(track_dataframe)
        track_dataframe.head()

    def addSpotifySongs(self, apple_dataframe):
        artist_name = []
        track_name = []
        popularity = []
        track_id = []

        client_credentials_manager = SpotifyClientCredentials(
            client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)

        print("\n\n")
        dataframe_length = apple_dataframe["artist_name"].size

        for i in range(0, dataframe_length, 1):
            query = 'artist:' + \
                apple_dataframe["artist_name"][i] + \
                ' track:' + apple_dataframe["track_name"][i]

            track_results = sp.search(
                q=query, type='track', limit=1, offset=0)

            if int(track_results['tracks']['total']) > 0:
                print("Found:" + apple_dataframe["track_name"][i])
                var = track_results['tracks']['items'][0]
                artist_name.append(var['artists'][0]['name'])
                track_name.append(var['name'])
                track_id.append(var['id'])
                popularity.append(var['popularity'])
            else:
                print("Skipped:" + apple_dataframe["track_name"][i])

        track_dataframe = pd.DataFrame(
            {'artist_name': artist_name,
             'track_name': track_name,
             'track_id': track_id,
             'popularity': popularity})

        print("\n\n Equivalent Spotify songs:\n\n")

        print(track_dataframe)
        track_dataframe.head()

        return track_dataframe

    def signInUser(self):
        artist_name = []
        track_name = []
        popularity = []
        track_id = []

        scope = 'user-library-read'

        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print("Usage: %s username" % (sys.argv[0],))
            sys.exit()

        token = util.prompt_for_user_token(
            username, scope, cid, secret, "http://localhost:8888/callback")

        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks()
            for item in results['items']:
                track = item['track']
                artist_name.append(track['artists'][0]['name'])
                track_name.append(track['name'])
                track_id.append(track['id'])
                popularity.append(track['popularity'])
        else:
            print("Can't get token for", username)

        track_dataframe = pd.DataFrame(
            {'artist_name': artist_name,
             'track_name': track_name,
             'track_id': track_id,
             'popularity': popularity})

        return track_dataframe

    def createSpotifyPlaylist(self):
        scope = 'user-modify-private playlist-modify-private user-read-currently-playing user-library-read user-read-recently-played user-modify-playback-state playlist-read-collaborative playlist-modify-public playlist-read-private'

        input_user = input("\nContinue? (1 = yes, 0 = no): ")

        if int(input_user) == 0:
            sys.exit()

        playlist_name = input(
            "\nEnter a name of a playlis you would like to create: ")

        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print("Usage: %s username" % (sys.argv[0],))
            sys.exit()

        token = util.prompt_for_user_token(
            username, scope, cid, secret, "http://localhost:8888/callback")

        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.user_playlist_create(
                username, playlist_name, public=False)
            print("\n\nPlaylist", playlist_name, "created successfully.\n")
        else:
            print("Can't get token for", username)

        return results['id']

    def addSpotifySongsToPlaylist(self, playlist_ID, spotify_dataframe):
        username = "mitch.sparrow"
        scope = 'user-modify-private playlist-modify-private user-read-currently-playing user-library-read user-read-recently-played user-modify-playback-state playlist-read-collaborative playlist-modify-public playlist-read-private'

        token = util.prompt_for_user_token(
            username, scope, cid, secret, "http://localhost:8888/callback")

        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.user_playlist_add_tracks(
                username, playlist_id=playlist_ID, tracks=spotify_dataframe['track_id'])
            print("\nSongs added to playlist")
        else:
            print("Can't get token for", username)

    def getAppleMusic(self, song_dataframe):

        artist_name = []
        track_name = []
        date_added = []
        track_id = []

        print("\n\nSpotify Liked Songs:\n\n")
        print(song_dataframe)
        print("\n\nApple Music Search Results:\n\n")

        secret = open('AuthKey_W9K597H774.p8', 'rb').read()

        am = applemusicpy.AppleMusic(
            secret, apple_key_ID, apple_team_ID)

        for i in range(0, 10, 1):
            track_result = am.search(
                song_dataframe["track_name"][i], types=['songs'], limit=1)
            var = track_result['results']['songs']['data'][0]['attributes']
            artist_name.append(var['artistName'])
            track_name.append(var['name'])
            date_added.append(var['releaseDate'])
            track_id.append(var['playParams']['id'])

        track_dataframe22 = pd.DataFrame(
            {'artist_name': artist_name,
             'track_name': track_name,
             'release_date': date_added,
             'id': track_id})

        print(track_dataframe22)

    def getAppleMusicPlaylist(self):

        playlist_name = []
        last_date = []
        curator_name = []
        playlist_id = []

        artist_name = []
        track_name = []
        date_added = []
        track_id = []

        playlist = input(
            "\nEnter a name of a Apple Music playlist you would like to clone to Spotify: ")
        print("\n\nSearch results for", playlist, ":\n")

        secret = open('AuthKey_W9K597H774.p8', 'rb').read()
        am = applemusicpy.AppleMusic(secret, apple_key_ID, apple_team_ID)

        track_result = am.search(playlist, types=['playlists'], limit=5)

        ii = len(track_result['results']['playlists']['data'])

        if ii > 4:
            ii = 4

        for i in range(0, ii, 1):
            var = track_result['results']['playlists']['data'][i]
            playlist_name.append(var['attributes']['name'])
            playlist_id.append(var['id'])
            curator_name.append(var['attributes']['curatorName'])
            last_date.append(var['attributes']['lastModifiedDate'])

        track_dataframe = pd.DataFrame(
            {'playlist_name': playlist_name,
             'curator_name': curator_name,
             'ID': playlist_id,
             'last_modified':  last_date})

        print(track_dataframe)

        selection = input(
            "\nSelect a playlist you would like to clone (number 0 - {}):".format(ii-1))
        if(0 <= int(selection) <= ii):
            print("\n\nYou selected: ", track_result['results']['playlists']
                  ['data'][int(selection)]['attributes']['name'], "\n\nSongs in playlist:\n")
        else:
            print("You are stupid - a number between 1 and 5")
            sys.exit()

        result = am.playlist(track_result['results']['playlists']
                             ['data'][int(selection)]['id'])

        ii = len(result['data'][0]['relationships']['tracks']['data'])

        for i in range(0, ii, 1):
            var = result['data'][0]['relationships']['tracks']['data'][i]['attributes']
            artist_name.append(var['artistName'])
            track_name.append(var['name'])
            date_added.append(var['releaseDate'])
            track_id.append(var['playParams']['id'])

        playlist_dataframe = pd.DataFrame(
            {'artist_name': artist_name,
             'track_name': track_name,
             'release_date': date_added,
             'id': track_id})

        print(playlist_dataframe)

        return playlist_dataframe


if __name__ == '__main__':
    s = Spotify()
    # dataframe = s.signInUser()
    # s.getAppleMusic(dataframe)
    playlist_dataframe = s.getAppleMusicPlaylist()
    spotify_songs_dataframe = s.addSpotifySongs(playlist_dataframe)
    new_playlist_id = s.createSpotifyPlaylist()
    s.addSpotifySongsToPlaylist(new_playlist_id, spotify_songs_dataframe)
