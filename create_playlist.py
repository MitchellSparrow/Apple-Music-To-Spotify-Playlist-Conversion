
import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from exceptions import ResponseException
from secrets import spotify_token, spotify_user_id


class CreatePlaylist:

    def __init__(self):
        #self.youtube_client = self.get_youtube_client()
        #self.all_song_info = {}
        client = "mitch"

    def create_playlist(self):
        request_body = json.dumps({
            "name": "Apple Music",
            "description": "All liked Youtube videos",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):

        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]
        print(uri)

        return uri

    def add_song_to_playlist2(self):
        # Add all liked songs into a new Spotify playlist
        # populate dictionary with our liked songs

        # collect all of uri
        song_name = "Gipsy"
        artist = "Moksi"
        spotify_URI = self.get_spotify_uri(song_name, artist)

        # create a new playlist
        playlist_id = self.create_playlist()
        print(playlist_id)

        # add all songs into new playlis
        request_data = json.dumps(spotify_URI)
        print(request_data)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        print(response)

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = CreatePlaylist()
    #cp.get_spotify_uri("Gipsy", "Moksi")
    cp.add_song_to_playlist2()
