import requests
from flask import Flask, request, render_template, jsonify, session, redirect
from spotify import get_music

app = Flask(__name__)
app.secret_key = 'ilovesecrets'
SPOTIFY_CLIENT_ID = '7c9a81122ea446d9a75dd69a38a1fc33'
SPOTIFY_CLIENT_SECRET = '4909ccc6903645de89c1dfa4b09d7669'
                         

@app.route('/')
def index():
    signin_url = 'https://accounts.spotify.com/authorize?' 
    parameters = [
        'client_id={}'.format(SPOTIFY_CLIENT_ID),
        'redirect_uri={}'.format('http://localhost:8080/oauth2callback'),
        'response_type=code',
        'scope=playlist-read-collaborative']
 
    signin_url += '&'.join(parameters)
 
    return redirect(signin_url)   
    #return render_template('index.html')

@app.route('/oauth2callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')
    if error:
        return("Error! {}".format(error))
 
    # Exchange the code for an access token
    print ('i got a code =' + code )
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8080/oauth2callback',
        'code': code,
        'grant_type': 'authorization_code'
    }
 
    r = requests.post(token_url, data=data)
 
    # In an ideal world we would store this token and use it to make all our
    # future API requests.
    #print 'This is json' 
    #print r.json()
    token = r.json().get('access_token')

    #print 'found a response?'
    try:
        r.raise_for_status()
        session['access_token'] = token
    except requests.exceptions.HTTPError as e:
        print "And you get an HTTPError:", e.message
      
    # Now we're going to call a SPOTIFY API, in this case the userinfo API
    #return render_template('index.html')
    return  render_template('index.html')

@app.route('/music', methods=['POST'])
def music():

    mood = request.form.get('mood')
    music = get_music(mood)

    # Store the mood in the session so we don't need to send it up all the time
    session['mood'] = mood

    return render_template('music.html', music=music)


@app.route('/api/music', methods=['POST'])
def music_api():

    offset = request.form.get('offset')
    mood = session.get('mood')

    # We can skip arguments with defaults - we don't need to supply 'limit'
    # but we do need to specify that the thing we're sending is 'offset'

    music = get_music(mood, offset=offset)

    return jsonify({'playlists': music}) # you can't just jsonify a list

def get_playlist_tracks(username, playlist_id):
    token = session.get('access_token')
    headers = { 'Authorization': 'Bearer {}'.format(token) }
    url = 'https://api.spotify.com/v1/users/'
    url += username
    url += '/playlists/'
    url += playlist_id
    url += '/tracks'
    return  requests.get(url, headers=headers).json()
   
def get_track_info(tracks): 
    tracks=tracks
    track_keys =  tracks.keys()
    track_items = tracks['items']
    track_by_albums = []
    track_by_songs = []
    for index, item  in enumerate(track_items):
        track_items_album = item['track']['album']['name']
        name_of_song = item['track']['name']
        track_artist = item['track']['artists'][0]['name']
        track_info = str(index+1) +". " + name_of_song + " from "  + track_items_album + " by " + track_artist
        track_by_songs.append(track_info)
        
    return track_by_songs

    def print_tests():
        #track_items_track_name =  item['track']['name']
        #print ("names of track: " + str(index) +" " +track_items_track_name)
        #track_items_track_number =  item['track']['track_number']
        #print ("A number  of  the track: " + str(index) +" " + str(track_items_track_number))
    
        # how do I create a list of albumn names from json to python?
   
        #for index, item  in enumerate(track_items):
        #    album_name = item['track']['album']['name'] 
        #    track_by_albums.extend(album_name)
        #    print "names of album: " 
        #    print track_by_albums 
        #   track_names =  item['track']['name']
        #    print "names of track: " 
        #    print track_names
        #for index in range(len(track_items)):
        #    track_items_album = track_items[index]['track']['album']['name']
        #    print ("names of album: " + str(index) +" " +track_items_album)  
        #    track_items_track_name =  track_items[index]['track']['name']
        #    print ("names of track: " + str(index) +" " +track_items_track_name)  
        #for index, item in track_items:
        #track_items_album = track_items[index]['track']['album']['name']
        #track_items_album = item['track']['album']['name']
        #   print (" did I get the album name ? " +  track_items_album)
        for key, value in track_items[0]['track'].items():
            #  i = i + 1
            #print ("key = " + key) 
            #print ("value = ")
            #print value
            if key == 'album':
            #   print ('the album is = ' ) 
            #   print value['name'] 
                print
            if key == 'name':
            #   print ('the name is = ' + value)
                album_name = value
            if key == 'track_number':
                album_track = value     


@app.route('/playlist/<username>/<playlist_id>', methods=['GET'])
def playlist_api(username, playlist_id):
    username = username
    playlist_id=playlist_id
    tracks = get_playlist_tracks(username, playlist_id)
    track_by_songs = get_track_info(tracks)

    return render_template('playlist2.html', tracks=track_by_songs)
    #return render_template('playlist.html', tracks=tracks)

    
if __name__ == "__main__":
    app.run(port=8080, debug=True)