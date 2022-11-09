from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import settings


app = Flask(__name__)

app.secret_key = settings.flask_secret_key
app.config['SESSION_COOKIE_NAME'] = 'User Session'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth(spotify_client_id=settings.spotify_client_id, spotify_client_secret=settings.spotify_client_secret)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth(spotify_client_id=settings.spotify_client_id, spotify_client_secret=settings.spotify_client_secret)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getPlaylists', _external=True))

@app.route('/getPlaylists')
def getPlaylists():
    return "Some Playlists"


def create_spotify_oauth(spotify_client_id, spotify_client_secret):
    return SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read')


if __name__ == "__main__":
    app.run()