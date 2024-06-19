import streamlit as st
import pandas as pd
import re

from src.utils import load_data, fit_and_normalize, normalize_user_data, get_recommendations
from src.spotify_api import SpotifyAPI

CID = '7c56991d824840bd82d5d7833f48bd00'
CSECRET = 'c035b79d95f842a38a48bc267d018fa7'
spotify_api = SpotifyAPI(CID, CSECRET)

df = load_data('data/track_infoFull.csv')
features_to_normalize = ['loudness', 'tempo', 'popularity']
df, scaler = fit_and_normalize(df, features_to_normalize)

def display_recommendations(url=None, u_df=None):
    if url:
        user_df = spotify_api.get_df_from_url(url)
    else:
        user_df = u_df
    user_df = normalize_user_data(user_df, scaler, features_to_normalize)
    rec = get_recommendations(df, user_df)
    recommendations = rec[['track_name', 'artist', 'album']]
    recommendations.columns = ['Track Title', 'Artist', 'Album']
    return recommendations.reset_index(drop=True)

def is_valid_spotify_url(url):
    pattern = r'^(https?://)?(www\.)?(open\.spotify\.com/(track|playlist)/[a-zA-Z0-9]+)(\?si=[a-zA-Z0-9]+)?$'
    return re.match(pattern, url) is not None

# streamlit app
st.set_page_config(page_title="K-pop Song Recommendation System", layout="wide")

url_instruction = '''
        :mag: To get URL:
        - Go to the song or playlist you would like to share
        - Click on \'⋅⋅⋅\'
        - Hover over \'share\'
        - Hit copy link to track/playlist
        '''

st.write("# K-pop Song Recommendation System :sunglasses:")
st.markdown(
    """
    ## Welcome to the K-Pop Song Recommender!

    Discover your next favorite K-Pop tracks! You can either:

    - **Enter a Spotify track or playlist URL**: Get recommendations based on your current listening preferences.
    - **Customize your music features**: Adjust sliders to select your desired audio features and find the most similar songs in our database.

    Explore new music tailored to your tastes!

    :mag: To get URL:
    - Go to the song or playlist you would like to share
    - Click on \'⋅⋅⋅\'
    - Hover over \'share\'
    - Hit copy link to track/playlist

    :rocket: Audio Feature Descriptions:

    - **Danceability**: Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
    - **Tempo**: The speed or pace of a track measured in beats per minute (BPM). Values typically range from 0 to 250 BPM.
    - **Loudness**: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness between tracks. Values range from -60 dB (quiet) to 0 dB (loud).
    - **Acousticness**: A confidence measure of whether the track is acoustic. A value of 1.0 represents high confidence the track is acoustic.
    - **Energy**: A measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. Values range from 0.0 to 1.0.
    """
)
st.sidebar.markdown(url_instruction)

url = st.sidebar.text_input("Enter a Spotify URL", placeholder='https://open.spotify.com/track')

if url:
    if is_valid_spotify_url(url):
        rec = display_recommendations(url=url)
        st.write('Top Recommendations:')
        st.table(rec)
    else:
        st.error('Please enter a valid Spotify track or playlist URL.')

danceability = st.sidebar.slider("Select the desired danceability:", min_value=0.0, max_value=1.0, value=0.6)
tempo = st.sidebar.slider("Select the desired tempo (BPM):", min_value=0, max_value=250, value=128)
loudness = st.sidebar.slider("Select the desired loudness level (dB):", min_value=-60, max_value=0, value=-20)
acousticness = st.sidebar.slider("Select the desired acousticness:", min_value=0.0, max_value=1.0, value=0.2)
energy = st.sidebar.slider("Select the desired energy level:", min_value=0.0, max_value=1.0, value=0.8)
instrumentalness = 0.2
liveness = 0.2
speechiness = 0.5
popularity = 50

clicked = st.sidebar.button("Submit")

user_features = pd.DataFrame([{
    'loudness': loudness,
    'tempo': tempo,
    'danceability': danceability,
    'acousticness': acousticness,
    'energy': energy,
    'instrumentalness': instrumentalness,
    'liveness': liveness,
    'speechiness': speechiness,
    'popularity': popularity
}])

if clicked:
    rec = display_recommendations(u_df=user_features)
    st.write('Top Recommendations:')
    st.table(rec)