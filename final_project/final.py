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
import sqlite3

CACHE_FNAME = "finalproject_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION ={}
def get_saved_songs(username):
    if username in CACHE_DICTION:
        print("the user was in the cache")
        return CACHE_DICTION[username]
    else:
        print("Making a request from Spotify for " + username +"'s timeline")
        token = util.prompt_for_user_token(username,'user-library-read',client_id='8022908ec4584139b085f818f10f11a8',client_secret='78334e2feb08493f948290e78dcba0f3',redirect_uri='http://localhost/')
        spotify = spotipy.Spotify(auth=token)
        results1 = spotify.current_user_saved_tracks(limit=50, offset=0)
        results2 = spotify.next(results1)
        results3 = spotify.next(results2)
        for track in results2['items']:
            results1['items'].append(track)
        for track in results3['items']:
            results1['items'].append(track)
        data = results1
    try:
        CACHE_DICTION[username] =  data
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[username]
    except:
        print("Wasn't in cache and wasn't valid search either")
        return None
def youtube_watch_history(username):
    api_key = 'AIzaSyCvjekk8uxhz2MUbNbo6KVl3ZUXVrEDEeE'

results = get_saved_songs('slev12397')
songs_dict = {}
for track in results['items']:
    time = track['track']["duration_ms"]
    song_id = track['track']['id']
    songs_dict[track['track']['name']] = [time, song_id]

conn = sqlite3.connect('final_project.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Songs')
cur.execute('CREATE TABLE Songs(song_id NUMBER, song_name TEXT, duration NUMBER)')
for song in songs_dict:
    tup = songs_dict[song][1],song, songs_dict[song][0]
    cur.execute('INSERT INTO Songs (song_id, song_name, duration) VALUES (?,?,?)',tup)

conn.commit()
cur.close()
song_duration ={}
for track in songs_dict:
    song_duration[track] = songs_dict[track][0]

plt.bar(range(len(song_duration)), song_duration.values(), align='center')
plt.xticks(range(len(song_duration)), list(song_duration.keys()))

# plt.show()
