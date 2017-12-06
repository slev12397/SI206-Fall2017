import requests
import json
import matplotlib.pyplot as plt
import time
from matplotlib import style
import instagram_info
import spotipy
import sys
import spotipy.util as util



def instagram_collector():
    access_token = instagram_info.access_token
    client_id = instagram_info.client_id
    url = 'https://api.instagram.com/v1/users/self/media/liked?access_token='+ access_token
    response = requests.get(url)
    return json.loads(response.text)
def spotify_collector():
    spotify = spotipy.Spotify()
    util.prompt_for_user_token('1447449240','user-read-recently-played',client_id='76422d4dd50d44469f327b071520f5a7',client_secret='f2b6931f6cc441a09894d84790759c75',redirect_uri='https://localhost:3000/callback')
    return spotify.current_user_recently_played(limit=50)

def youtube_collector():
    pass
sp = spotipy.Spotify()

results = sp.search(q='weezer', limit=20)
print(results)
