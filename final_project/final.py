import requests
import json
import matplotlib.pyplot as plt
import time
from matplotlib import style
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spotipy
import spotipy
from datetime import datetime
import calendar

token = util.prompt_for_user_token('slev12397','user-library-read',client_id='8022908ec4584139b085f818f10f11a8',client_secret='78334e2feb08493f948290e78dcba0f3',redirect_uri='http://localhost/')
spotify = spotipy.Spotify(auth=token)
results = spotify.current_user_saved_tracks(limit=50, offset=0)
results2 = spotify.next(results)

songs_duration = {}
for track in results['items']:
    time = track['track']["duration_ms"]
    songs_duration[track['track']['name']] = time
for track in results2['items']:
    time = track['track']["duration_ms"]
    songs_duration[track['track']['name']] = time

print(songs_duration)
