# src/utils.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def fit_and_normalize(df, features_to_normalize):
    min_row = {'popularity': 0, 'loudness': -60, 'tempo': 0}
    max_row = {'popularity': 100, 'loudness': 0, 'tempo': 250}

    min_row_df = pd.DataFrame([min_row])
    max_row_df = pd.DataFrame([max_row])

    df_with_extremes = pd.concat([df, min_row_df, max_row_df], ignore_index=True)

    scaler = MinMaxScaler()
    df_with_extremes[features_to_normalize] = scaler.fit_transform(df_with_extremes[features_to_normalize])

    # Remove the min and max rows after scaling
    df = df_with_extremes.iloc[:-2]
    return df, scaler

def normalize_user_data(df, scaler, features_to_normalize):
   df[features_to_normalize] = scaler.transform(df[features_to_normalize])
   return df

def load_data(file_path):
    return pd.read_csv(file_path)

def get_recommendations(user_features_df, df, top_n=10):
    features_to_include = ['loudness', 'tempo', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'speechiness']
    normalized_features = df[features_to_include].values
    user_normalized = user_features_df[features_to_include].values

    similarity_scores = cosine_similarity(normalized_features, user_normalized)

    # ensuring that even for only one track, it returns 10 recommend songs
    if len(user_normalized) == 1:
      mean_similarity = similarity_scores.flatten()
    else:
      mean_similarity = similarity_scores.mean(axis=0)

    top_indices = mean_similarity.argsort()[-top_n:][::-1]
    return df.iloc[top_indices]

# Example usage: Get recommendations based on user input
# recommendations = get_recommendations(user_features_df, df, features_to_normalize)
# recommendations[['track_name', 'artist', 'album']]
