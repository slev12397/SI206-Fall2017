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
from datetime import date
import calendar, datetime
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
        print("the Spotify user was in the cache")
        return CACHE_DICTION[username]
    else:
        print("Making a request from Spotify for " + username +"'s songs")
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
def darksky(year, month, day):
    date = str(year +'/'+ month +'/' + day)
    try:
        cache_file = open(CACHE_FNAME,'r')
        cache_contents = cache_file.read()
        cache_file.close()
        CACHE_DICTION = json.loads(cache_contents)
    except:
        CACHE_DICTION ={}
    if date in CACHE_DICTION:
        print("the day was in the cache")
        return CACHE_DICTION[date]
    else:
        print("Making a request from Darksky for " + year +'/'+ month +'/' + day)
        api_key = 'ad64317cbf3184964b51d495402c11e5'
        time = '{}-{}-{}T00:00:00'.format(year,month,day)
        lat = '42.2808'
        lng = '83.7430'
        url = 'https://api.darksky.net/forecast/{}/{},{},{}'.format(api_key,lat,lng,time)
        res = requests.request(method="get", url=url)
        results = json.loads(res.text)
        data = results
    try:
        CACHE_DICTION[date] =  data
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[date]
    except:
        print("Wasn't in cache and wasn't valid search either")
        return None

results = get_saved_songs('slev12397')
songs_dict = {}
for track in results['items']:
    time = track['track']["duration_ms"]
    song_id = track['track']['id']
    time_added = track['added_at']
    year = time_added[0:4]
    month = time_added[5:7]
    day = time_added[8:10]
    temp = darksky(year, month, day)['currently']['temperature']
    day_added = date(int(time_added[0:4]),int(time_added[5:7]),int(time_added[8:10])).weekday()
    day = calendar.day_name[day_added]
    songs_dict[track['track']['name']] = [time, song_id, day, temp]

conn = sqlite3.connect('final_project.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Songs')
cur.execute('CREATE TABLE Songs (song_id NUMBER, song_name TEXT, duration NUMBER, day_added TEXT, temperature TEXT)')
for song in songs_dict:
    tup = songs_dict[song][1], song, songs_dict[song][0], songs_dict[song][2], songs_dict[song][3]
    cur.execute('INSERT INTO Songs (song_id, song_name, duration,day_added, temperature) VALUES (?,?,?,?,?)',tup)

conn.commit()
cur.close()
song_duration ={}
for track in songs_dict:
    song_duration[track] = songs_dict[track][0]

# plt.bar(range(len(song_duration)), song_duration.values(), align='center')
# plt.xticks(range(len(song_duration)), list(song_duration.keys()))

weekday_feq = {}
for track in songs_dict:
    if songs_dict[track][2] in weekday_feq:
        weekday_feq[songs_dict[track][2]] +=1
    else:
        weekday_feq[songs_dict[track][2]]=1
for day in weekday_feq:
    print("On " + day + 's I added ' + str(weekday_feq[day]) + ' songs to my Spotify library')
    print('============================================================')
plt.bar(range(len(weekday_feq)), weekday_feq.values(), align='center')
plt.xticks(range(len(weekday_feq)), list(weekday_feq.keys()))
# plt.show()
