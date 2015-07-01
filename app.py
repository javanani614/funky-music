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
    print 'This is json' 
    print r.json()
    token = r.json().get('access_token')

    print 'found a response?'
    try:
        r.raise_for_status()
        session['access_token'] = token
    except requests.exceptions.HTTPError as e:
        print "And you get an HTTPError:", e.message
    
    
    print '## end of r type ####'
    print r 
    print '#################### end of r   ###################'
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
    print('TOKEN TOKEN TOKEN TOKEN TOKEN')

    token = session.get('access_token')
    print token
    #token = 'BQANEYvdYTrf0oqNNTEDIxLyLCZfvyNAlAsMLgn9ckh4RkzIVUbn0MOfkf3WNPY68gwylC_yHgMdpMzDFVHY5e1aiIn76pQty43VEEdZFLM8kcIzaW2HUygUff9BnQgodTk4Q_k-h82_tDh-_aCo7n2Dd6zmxzb2'
    headers = { 'Authorization': 'Bearer {}'.format(token) }
    url = 'https://api.spotify.com/v1/users/'
    url += username
    url += '/playlists/'
    url += playlist_id
    url += '/tracks'
    return  requests.get(url, headers=headers).json()
   
     

@app.route('/playlist/<username>/<playlist_id>', methods=['GET'])
def playlist_api(username, playlist_id):
    username = username
    playlist_id=playlist_id
    tracks = get_playlist_tracks(username, playlist_id)
    print (music)
    #print len(tracks)
    print tracks.keys()
    track_items = tracks['items']
    #print len(track_items[0])
    i = 0
    for key, value in track_items[0]['track'].items():
      #  i = i + 1
        print ("key = " + key) 
        #print ("value = ")
        #print value
        if key == 'album':
            print ('the album is = ' ) 
            print value['name'] 
            print
        if key == 'name':
            print ('the name is = ' + value)
            album_name = value
        if key == 'track_number':
            print  ('track number = ' + str(value))
            album_track = value
        if key in 'artists':
            artists_info = value
            for detail in artists_info:
                #print "ARTISTS"
                for element in detail.items():
                     print element


                
       
    #    if i == 2:
    #        break

    #for i in range(1):
    #    tracks.keys['items']['track']['album']
    return render_template('playlist.html', tracks=tracks)
    #return render_template('playlist.html', tracks=tracks)

    
if __name__ == "__main__":
    app.run(port=8080, debug=True)