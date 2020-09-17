import os
import re

import numpy as np
import pandas as pd
from tqdm import tqdm

from textblob import TextBlob

original_data = pd.read_csv("./data/fantasy_football_auction_values.csv")
player_names = list(original_data.Player_Names)


def update_dataframe_with_sentiment_scores(dataframe, name_of_players_column):
    player_names = list(original_data[name_of_players_column])

    dataframe['sentiment_scores'] = np.zeros(dataframe.shape[0])

    for idx, name in enumerate(player_names):
        path_to_tweets = f"./sentiment-analysis/twitter/output/16-09-2020_{name}_tweets.csv"

        if os.path.exists(path_to_tweets):
            player_sentiment_score, num_tweets = _get_sentiment_analysis_on_dataframe(path_to_tweets)
            print(f'{name}: {player_sentiment_score} ({num_tweets})')
            dataframe['sentiment_scores'].iloc[idx] = player_sentiment_score
    dataframe = dataframe.fillna(0)
    return dataframe

def _get_sentiment_analysis_on_dataframe(path_to_tweets):
    player_tweets_df = pd.read_csv(path_to_tweets, index_col=0)
    player_tweets_df = player_tweets_df.reset_index()
    sentiment = []
    for idx, row in player_tweets_df.iterrows():
        sentiment.append(_get_tweet_sentiment(row['tweet']))
    num_tweets = player_tweets_df.shape[0]
    return np.mean(sentiment), num_tweets
        
def _get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    # create TextBlob object of passed tweet text 
    analysis = TextBlob(cleaned_tweet) 
    
    # polarity > 0 is positive
    # polarity == 0 is neutral
    # polarity < 0 is negative
    
    # return sentiment
    return analysis.sentiment.polarity

if __name__ == "__main__":
    sentiment_dataframe = update_dataframe_with_sentiment_scores(original_data, "Player_Names")
    sentiment_dataframe.to_csv("./data/fantasy_football_auction_values_with_sentiment.csv", index=False)

