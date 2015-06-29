from flask import Flask, request, render_template, jsonify, session, redirect
from spotify import get_music
import requests
app = Flask(__name__)
app.secret_key = 'ilovesecrets'

SPOTIFY_CLIENT_ID = '7c9a81122ea446d9a75dd69a38a1fc33'
SPOTIFY_CLIENT_SECRET = '4909ccc6903645de89c1dfa4b09d7669'



 

@app.route('/')
def signin():

    # We are going to immediately redirect to spotify.  We could ask the user
    # to sign in by clicking a button, if this were a more interesting app.

       
    return render_template('login.html')

    

@app.route('/index', methods=["post"] )
def index():

    # We are going to immediately redirect to Google. We could ask the user
    # to sign in by clicking a button, if this were a more interesting app.

    
    return render_template('index.html')
    #return redirect(signin_url)

@app.route('/oauth2callback')
def callback():
    print "CALLBACK REDIRECT"
    code = request.args.get('code')
    error = request.args.get('error')
    if error:
        return("Error! {}".format(error))

    # Exchange the code for an access token

    token_url = 'https://accounts.google.com/o/oauth2/token'
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
    token = r.json().get('access_token')

    # Now we're going to call a Google API, in this case the userinfo API

    r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={}'.format(token))

    info = r.json()
    print info
    user_name = info.get('name')
    return "Thank you for signing in, {}".format(user_name)



def get_playlist_tracks(user_id, playlist_id):
    token = SPOTIFY_TOKEN
    #token = 'BQD3LH8JXyl-KZ_sDSmZu0_zjyNy1mc7ZeMK-3XlqeHB9_Zo5xeMDZUZMz2JeQ_Ec2wiu4sEAy158oIrz9GBo8tZhMcJKiiCJ93F7fYpR8eBQS9XEyJRQW1opeQUu_bPuegh1cbTNItC-6rC'
    headers = { 'Authorization': 'Bearer {}'.format(token) }
    url = 'https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks'
    

    return requests.get(url, headers=headers).json()
    



@app.route('/music', methods=['POST'])
def music():

    mood = request.form.get('mood')
    music = get_music(mood)
    # Store the mood in the session so we don't need to send it up all the time
    session['mood'] = mood
    print '$$$$$$$$$$$$$$$$$$$$ music done $$$$$$$$$$$$$$$$$$$'

    return render_template('music.html', music=music)


#@app.route('/api/music', methods=['POST'])
#def music_api():
#    print ' #####################entering api ##################################'
#    offset = request.form.get('offset')
#    mood = session.get('mood')

    # We can skip arguments with defaults - we don't need to supply 'limit'
    # but we do need to specify that the thing we're sending is 'offset'

#    music = get_music(mood, offset=offset)
#    print '#####################  api done #######################'

#   return jsonify({'playlists': music}) # you can't just jsonify a list

@app.route('/playlist/<username>/<playlist_id>', methods=['POST'])
def playlist(username, playlist_id):
    print '############################# inside of playlist ###################'
    username = '1112389416'
    playlist_id = '2yCIJgYWeWZmShpthNazPB'
    tracks = get_playlist_tracks(username, playlist_id)
    return render_template('playlist.html', tracks=tracks)

if __name__ == "__main__":
    app.run(port=8080, debug=True)