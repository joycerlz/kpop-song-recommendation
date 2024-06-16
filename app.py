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

def display_recommendations(url):
    user_df = spotify_api.process_url(url)
    user_df = normalize_user_data(user_df, scaler, features_to_normalize)
    return get_recommendations(df, user_df)

def is_valid_spotify_url(url):
    pattern = r'^(https?://)?(www\.)?(open\.spotify\.com/(track|playlist)/[a-zA-Z0-9]+)(\?si=[a-zA-Z0-9]+)?$'
    return re.match(pattern, url) is not None

# streamlit app
st.set_page_config(page_title="K-pop Song Recommendation System", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 400px;
        margin-left: -400px;
    }

    """,
    unsafe_allow_html=True,
)

url_instruction = '''
        To get URL:
        - Go to the song or playlist you would like to share
        - Click on \'⋅⋅⋅\'
        - Hover over \'share\'
        - Hit copy link to track/playlist
        '''

st.write("# K-pop Song Recommendation System!")
st.write('Enter a Spotify track or playlist URL to get recommendations.')
st.markdown(url_instruction)

url = st.text_input("Spotify URL", placeholder='https://open.spotify.com/track/44zfpg3ndtGESsgpTbWeyE?si=f83c8eae88154287')

if url:
    if is_valid_spotify_url(url):
        rec = display_recommendations(url)
        st.write('Top Recommendations:')
        st.table(rec[['track_name', 'artist', 'album']])
    else:
        st.error('Please enter a valid Spotify track or playlist URL.')
