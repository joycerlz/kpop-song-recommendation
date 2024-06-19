# Kpop Song Recommendation System
This project aims to provide personalized K-Pop song recommendations based on user preferences and Spotify data.

## Features
- **Personalized Recommendations:** Get song suggestions based on your favorite Spotify track or playlist
- **Feature Based Search:** Customize your desired audio features like danceability, energy, and tempo to find songs that match your taste

## To Run the App
- Clone the repository: ```git clone https://github.com/joycerlz/kpop-song-recommendation.git```
- Install the required dependencies: ```pip install -r requirements.txt```
- Run the streamlit app: ```streamlit run app.py```

## Data Engineering
**Spotify API:** I'm using the [Spotify Web API](https://developer.spotify.com/documentation/web-api) to fetch song metadata and audio features.

I manually combined 30+ random K-pop playlists created by other users into one playlist, removed duplicate songs, then fetched track metadata into the ```data/track_infoFull.csv``` file. I am using this file as my recommender database.

This project uses cosine similarity to compare and recommend songs based on the provided features.

## Exploratory Data Analysis
<img src="https://github.com/joycerlz/kpop-song-recommendation/assets/81258562/edbf77b2-bcbf-426c-b4d1-e86b8b79e518" width="750" height="600">
