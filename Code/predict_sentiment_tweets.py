"""
    CommunistBadger v1.0.0
    This is the code for the predicting the sentiment from tweets scrapped from twitter.
"""

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
import tweepy as tp
from keras.preprocessing import sequence
import numpy as np
import re

consumer_key = 'pKnvO75ckS2QAj7mSq8nnlMBv'
consumer_secret = 'xiZ4835Rp85NZTxMZEMux2PE69pKX9nYHiFogq32yCyoiW3GNE'
access_token = '709712385246961664-yI4TWDMYDJP0J8ERUgO4KzmKgCzSYnA'
access_token_secret = 'AX1aHYqzv4xR6KPzfqfCHnaqvrA5A7IsPFi82fMxCjwxM'

tweets = []
pos_tweets_lst = []
neg_tweets_lst = []
neg_count = 0
pos_count = 0
t_sum = 0
coeff = 0.01
word = "hate"

def twitter_conn(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tp.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tp.API(auth, wait_on_rate_limit=True)
    return api


def search_tweets(api, keyword):
    for tweet_info in tp.Cursor(api.search, q=keyword,lang='en', tweet_mode='extended').items(200):
        if 'retweeted_status' in dir(tweet_info):
            tweets.append(tweet_info.retweeted_status.full_text)
        else:
            tweets.append(tweet_info.full_text)
    return tweets

def cleansing(tweet):
    tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub('@[^\s]+',' ', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub(r'\W*\b\w{1,3}\b', '', tweet)
    return tweet


model = load_model('Models/conv-1D-1.6-weights.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
max_features = 400000  # vocabulary size
api = twitter_conn(consumer_key, consumer_secret, access_token, access_token_secret)
twts = search_tweets(api, word)

def _get_results():
    cleaned_twts = [cleansing(x) for x in twts]
    tokenizer = Tokenizer(num_words=40000)
    tokenizer.fit_on_texts(cleaned_twts)
    tokenizer_padded = tokenizer.texts_to_sequences(cleaned_twts)
    x = np.array(sequence.pad_sequences(tokenizer_padded, maxlen=20, padding='post'))
    out = model.predict_classes(x, batch_size=1)
    flat_out = [y for x in out for y in x]
    neg_count = 0
    pos_count = 0
    t_sum = 0
    for ix in range(len(flat_out)):
        if flat_out[ix] == 1:
            pos_count += 1
            t_sum += 1
            pos_tweets_lst.append(cleaned_twts[ix])
        else:
            neg_count += 1
            t_sum += 1
            neg_tweets_lst.append(cleaned_twts[ix])

    return t_sum, neg_count, pos_count

def _get_tweet_coefficient():
    total_tweets, negative_tweets, positive_tweets = _get_results()
    print("Total Tweets: ", total_tweets)
    print("Total Negative Tweets: ", negative_tweets)
    print("Total Positive Tweets: ", positive_tweets)
    pos_percentage = (positive_tweets/total_tweets)
    neg_percentage = (negative_tweets/total_tweets)
    diff_percentage = (pos_percentage - neg_percentage)
    print("Difference Percentage: ", diff_percentage)
    print("Positive Percentage: ", pos_percentage)
    print("Negative Percentage: ", neg_percentage)
    if diff_percentage > 0.10:  # if the diff is less than a certain percentage, then negative is dominant.
        neg_percentage *= coeff
    else:
        pos_percentage *= coeff
    print("Up Positive Percentage: ", pos_percentage)
    print("Up Negative Percentage: ", neg_percentage)

if __name__ == '__main__':
    _get_tweet_coefficient()