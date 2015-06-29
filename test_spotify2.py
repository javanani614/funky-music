import requests
import os
token = os.environ.get('SPOTIFY_TOKEN')
headers = { 'Authorization': 'Bearer {}'.format(token) }
url = 'https://api.spotify.com/v1/users/1112389416/playlists/2yCIJgYWeWZmShpthNazPB/tracks'
results = requests.get(url, headers=headers).json()
print results
