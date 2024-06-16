import spotipy
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:
    def __init__(self, CID, CSECRET):
        auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=CSECRET)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self.headers = ['track_id', 'track_name', 'album', 'artist', 'release_date',
                        'length', 'popularity', 'danceability', 'acousticness', 'energy',
                        'instrumentalness', 'liveness', 'loudness', 'speechiness',
                        'tempo', 'time_signature']

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

    def process_url(self, url):
        track_features = []
        if "track" in url:
            track_id = url.split('/')[-1].split('?')[0]
            features = self.get_track_features(track_id)
            track_features.append(features)

        elif "playlist" in url:
            playlist_id = url.split('/')[-1].split('?')[0]
            tracks = self.sp.playlist_tracks(playlist_id)["items"]
            np.random.shuffle(tracks)
            for item in tracks[:100]:
                track_id = item["track"]["id"]
                features = self.get_track_features(track_id)
                track_features.append(features)

        features_df = pd.DataFrame(track_features, columns=self.headers)
        return features_df

