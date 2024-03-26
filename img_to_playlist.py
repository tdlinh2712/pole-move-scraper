import base64
import json
import pytesseract
from PIL import Image
from dataclasses import dataclass
from requests import session
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os

import keys
os.environ["SPOTIPY_CLIENT_ID"] = keys.CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"]=keys.CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"]=keys.REDIRECT_URL

@dataclass

class RoutineInfo:
    class_name: str = ""
    song_name: str = ""
    artist: str = ""
    def __init__(self, class_name: str, song_name: str, artist: str):
        self.class_name = class_name
        self.song_name = song_name
        self.artist = artist

    def toIterable(self):
        return iter(
            [
                self.class_name,
                self.song_name,
                self.artist
            ]
        )

    def toHeader(self):
        return [
            "Class",
            "Song",
            "Artist",
        ]

# Open the image file
image = Image.open('bobbi_term1.jpeg')

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)

lines = text.splitlines()

routine_infos = []

for line in lines:
    #try split each line by '-', if it doesnt split into 3 then ignore the line
    song_info = line.split("-")
    if len(song_info) != 3:
        continue
    routine_infos.append(RoutineInfo(class_name=song_info[0].strip(),song_name= song_info[1].strip(), artist=song_info[2].strip()))


print(routine_infos)
url = 'https://accounts.spotify.com/api/token'

username = keys.USERNAME
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)


sp = spotipy.Spotify(auth=token)

# TODO: oauth flow
user = sp.current_user()
print(f"User: {user['display_name']}")

song_uris = []
for routine_info in routine_infos:
    q="artist:" +  routine_info.artist + " track:" + routine_info.song_name

    print(q)
    search_results = sp.search(q=q, type='track')
    print(search_results['tracks']['href'])
    print(f"Found {search_results['tracks']['total']} results")
    if (search_results['tracks']['total'] == 0):
        continue
    print(f"Top 1: {search_results['tracks']['items'][0]['name']} url {search_results['tracks']['items'][0]['external_urls']['spotify']}")
    song_uris.append(search_results['tracks']['items'][0]['external_urls']['spotify'])

playlist = sp.user_playlist_create(user['id'], 'My Playlist', public=True)
print(f"Playlist Created: {playlist['name']}")
print(playlist)
res = sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
print(res)
print(f"Created playlist at {playlist['external_urls']['spotify']}")

#print(response)

