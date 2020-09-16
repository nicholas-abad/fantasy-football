import sys
import time

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

from gather_tweets import search_twitter
from tweets_json import to_pd_dataframe


nltk.download("vader_lexicon")


def sentiment_analysis(search_term, limit, save_df=True):
    sid = SentimentIntensityAnalyzer()

    # Gather the tweets
    tweets = search_twitter(search_term, limit)

    # Put the tweets into a Pandas dataframe
    tweets_df = to_pd_dataframe(tweets)
    print(tweets_df.shape)
    if save_df:
        tweets_df.to_csv(path_or_buf="dataframe.csv")


if __name__ == "__main__":
    search_term = sys.argv[1]
    limit = int(sys.argv[2])
    sentiment_analysis(search_term, limit)
