# Python - Clone Apple Music Playlist to Spotify

The following python script is used to clone public Apple Music playlists to Spotify. The reason I created this project was because I was using both music applications at the time and was often transferring songs and playlists between the music apps. This became very time consuming to do manually and so I decided to write a script that could do it for me. 

## How it works:

* The script allows the user to search and select a playlist on Apple Music that they would like to clone
* The script then recreates a playlist in Spotify with this same name in the users account 
* Additionaly, the user can choose if this playlist is public or private and if a song is not found on Spotify, it will be skipped in the playlist

## Installation:

```bash
pip install -r requirements.txt
```

## Usage:

```bash
python spotify.py "Spotify username"
```
