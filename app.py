import streamlit as st
import pandas as pd

from src.utils import load_data, fit_and_normalize, normalize_user_data, get_recommendations
from src.spotify_api import SpotifyAPI

CID = '7c56991d824840bd82d5d7833f48bd00'
CSECRET = 'c035b79d95f842a38a48bc267d018fa7'
spotify_api = SpotifyAPI(CID, CSECRET)

df = load_data('data/track_infoFull.csv')
features_to_normalize = ['loudness', 'tempo', 'popularity']
df, scaler = fit_and_normalize(df, features_to_normalize)


