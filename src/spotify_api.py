import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:
    def __init__(self, CID, CSECRET) -> None:
        auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=CSECRET)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    # get features of each track from track id
    def get_track_features(self, track_id):
        meta = self.sp.track(track_id)
        features = self.sp.audio_features(track_id)

        track = {
        'track_id': track_id,
        'track_name': meta['name'],
        'album': meta['album']['name'],
        'artist': meta['album']['artists'][0]['name'],
        'release_date': meta['album']['release_date'],
        'length': meta['duration_ms'],
        'popularity': meta['popularity'],
        'danceability': features[0]['danceability'],
        'acousticness': features[0]['acousticness'],
        'energy': features[0]['energy'],
        'instrumentalness': features[0]['instrumentalness'],
        'liveness': features[0]['liveness'],
        'loudness': features[0]['loudness'],
        'speechiness': features[0]['speechiness'],
        'tempo': features[0]['tempo'],
        'time_signature': features[0]['time_signature']
        }
        return track

    def get_playlist_tracks(self, playlist_id):
        playlist_tracks = self.sp.playlist_tracks(playlist_id)['items']
        tracks = []
        for item in playlist_tracks[:50]:
            track = self.get_track_features(item['track']['id'])
            tracks.append(track)
        return tracks


CID = '7c56991d824840bd82d5d7833f48bd00'
CSECRET = 'c035b79d95f842a38a48bc267d018fa7'
REDIRECT_URI = 'https://example.com/callback/'
