import json
import sys

import numpy as np
import pandas as pd

def load_json_tweets(filepath):
    tweets = json.load(open(filepath))
    return tweets

def to_full_json(tweets, filepath="tweets.json"):
    with open(filepath, 'w') as f:
        #Dump json file. indent=4 prints the output prettier, but will increase disk space.
        json.dump(tweets, f, indent=4)

def to_minimal_json(tweets, filepath="tweets.json"):
    #This reduces each tweet to the set of keys (attributes) listed.
    #Other attributes can be used here, see https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    atts=['id_str', 'full_text']
    minimal_tweets = [{k:tweet[k] for k in atts} for tweet in tweets]
    with open(filepath, 'w') as f:
        #Dump json file. indent=4 prints the output prettier, but will increase disk space.
        json.dump(minimal_tweets, f, indent=4)

def to_just_text(tweets, filepath="tweets.txt"):
    #This just outputs the text of each tweet.
    with open(filepath, 'w') as f:
        for tweet in tweets:
            #Linebreaks are replaced so we have one tweet per line.
            f.write("%s\n" % tweet['full_text'].replace("\n", " ").replace("\r", " "))

def to_pd_dataframe(tweets):
    df = pd.DataFrame(np.empty(len(tweets)).astype(str), columns=['tweet'])
    for idx, tweet in enumerate(tweets):
        df.iloc[idx]['tweet'] = tweet['full_text'].replace("\n", " ").replace("\r", " ")
    return df

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: %s filepath outfile" % sys.argv[0])
        sys.exit (1)

    filepath = sys.argv[1]
    outfile = sys.argv[2]
    tweets = load_json_tweets(filepath)
    to_just_text(tweets, filepath="%s" % outfile)
