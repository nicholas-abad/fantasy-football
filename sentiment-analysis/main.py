from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


nltk.download('vader_lexicon')

def sentiment_analysis():
    sid = SentimentIntensityAnalyzer()
