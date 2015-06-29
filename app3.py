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


if __name__ == "__main__":
    app.run(port=8080, debug=True)