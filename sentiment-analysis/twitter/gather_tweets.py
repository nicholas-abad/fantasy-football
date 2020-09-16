import argparse
from datetime import datetime
import os
import sys
import time

from tqdm import tqdm
from _tweets_json import *
from twython import Twython, TwythonError, TwythonRateLimitError

parser = argparse.ArgumentParser(description="Define the arguments in the gather_tweets.py file.")
parser.add_argument(
    "--search_term",
    action="store",
    dest="search_term",
    required=False,
    help="The search term that you want to search on Twitter. Default: DerekCarr",
    default="DerekCarr",
)
parser.add_argument(
    "--num_tweets",
    action="store",
    dest="num_tweets",
    required=False,
    help="The number of tweets that you want to scrape. Default: 100",
    default=1000,
)
parser.add_argument(
    "--output_dir",
    action="store",
    dest="output_dir",
    required=False,
    help="The output directory where you want to save your tweets file. Default: './output/'",
    default="./output/",
)

args = parser.parse_args()
search_term = args.search_term.replace(" ", "").replace("#", "")
num_tweets = int(args.num_tweets)
output_dir = args.output_dir


def search_twitter(search_term, limit):
    # Authorize use of Twitter API with supplied credentials (from twitter_auth).
    print('Authenticating....')
    twitter = Twython(
        app_key=os.getenv("TWITTER_CONSUMER_KEY"),
        app_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
        oauth_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        oauth_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
    )
    print(".... Successfully Authenticated!")

    tmpTweets = []
    tweets = []
    tweets_num_retweets = []
    tweets_num_favorite = []
    try:
        # x
        search_results = twitter.search(
            q=search_term,
            lang="en",
            tweet_mode="extended", 
            count=limit, 
            result_type="recent", # Can be one of recent, mixed or popular
        )
        tmpTweets.extend(search_results["statuses"])
        # Check if tweets are inbetween two dates.
        # NOTE: Twitter API does not have this functionality...
        startDate = datetime(2019, 12, 1, 0, 0, 0)
        endDate =   datetime(2020, 12, 1, 0, 0, 0)

        # Check if tweets are "reputable".
        min_retweets = 0
        min_favorites = 0

        for tweet in tqdm(tmpTweets):
            # Turn the tweet['created_at'] field into a datetime object.
            created_at_dt = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            if created_at_dt < endDate and created_at_dt > startDate:
                # Only get the "reputable" tweets
                if tweet['retweet_count'] >= min_retweets or tweet['favorite_count'] >= min_favorites:
                    tweets.append(tweet)
                    tweets_num_retweets.append(tweet['retweet_count'])
                    tweets_num_favorite.append(tweet['favorite_count'])
        print('Len TmpTweets: ', len(tmpTweets))
        print('Len Tweets: ', len(tweets))
        # save the id of the oldest tweet less one, this is the starting point for collecting further tweets.
        # oldest = tweets[-1]["id"] - 1
        # keep grabbing tweets until there are no tweets left to grab.
        # while len(search_results["statuses"]) > 0 and len(tweets) < limit:
        #     try:
        #         # all subsequent requests use the max_id param to prevent duplicates
        #         search_results = twitter.search(
        #             q=search_term, tweet_mode="extended", count=100, max_id=oldest
        #         )
        #         tweets.extend(search_results["statuses"])
        #         oldest = tweets[-1]["id"] - 1
        #         print(f"...{len(tweets)} tweets downloaded so far for #{search_term}")
        #     except TwythonRateLimitError as e:
        #         # We have hit the rate limit, so we need to take a break.
        #         remainder = (
        #             float(twitter.get_lastfunction_header(header="x-rate-limit-reset"))
        #             - time.time()
        #         )
        #         # Drop twitter API connection
        #         # del twitter
        #         print("sleeping for %d seconds" % remainder)
        #         # Pause until we can go again.
        #         time.sleep(remainder)
        #         # Renew twitter API connection
        #         twitter = Twython(
        #             consumer_key, consumer_secret, access_token, access_secret
        #         )
        #         continue

    except TwythonError as e:
        print(e)

    return tweets


if __name__ == "__main__":
    # Gather the tweets.
    tweets = search_twitter(search_term, num_tweets)

    to_full_json(tweets)
    # Transform tweets into a dataframe.
    tweets_df = to_pd_dataframe(tweets)

    # Create output directory if this does not exist yet
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Save the csv file into output directory with the specific name.
    current_date = datetime.now().strftime("%d-%m-%Y")
    whole_output_filename = (
        f"{output_dir}{current_date}_{search_term}_tweets.csv"
    )
    tweets_df.to_csv(whole_output_filename)
