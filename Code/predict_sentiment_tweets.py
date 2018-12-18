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
import matplotlib.pyplot as plt

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

tweets = []
pos_tweets_lst = []
neg_tweets_lst = []
neg_count = 0
pos_count = 0
t_sum = 0
coeff = 0.01

class SentimentTweets():
    def __init__(self, word, tweet_count):
        self.word = word
        self.tweet_count = tweet_count
        self.model = load_model('Models/conv-1D-1.6-weights.h5')
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.max_features = 400000  # vocabulary size
        self.api = self.twitter_conn(consumer_key, consumer_secret, access_token, access_token_secret)
        self.twts = self.search_tweets(self.api, self.word)

    def twitter_conn(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tp.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tp.API(auth, wait_on_rate_limit=True)
        return api


    def search_tweets(self, api, keyword):
        for tweet_info in tp.Cursor(api.search, q=keyword,lang='en', tweet_mode='extended').items(self.tweet_count):
            if 'retweeted_status' in dir(tweet_info):
                tweets.append(tweet_info.retweeted_status.full_text)
            else:
                tweets.append(tweet_info.full_text)
        return tweets

    def cleansing(self, tweet):
        tweet.lower()
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        tweet = re.sub('@[^\s]+',' ', tweet)
        tweet = re.sub('[\s]+', ' ', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = re.sub(r'\W*\b\w{1,3}\b', '', tweet)
        return tweet

    def _get_results(self):
        cleaned_twts = [self.cleansing(x) for x in self.twts]
        tokenizer = Tokenizer(num_words=40000)
        tokenizer.fit_on_texts(cleaned_twts)
        tokenizer_padded = tokenizer.texts_to_sequences(cleaned_twts)
        x = np.array(sequence.pad_sequences(tokenizer_padded, maxlen=20, padding='post'))
        out = self.model.predict_classes(x, batch_size=1)
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

        return t_sum, neg_count, pos_count, flat_out


    def graph_sentiment(self):
        _, _, _, sentiments = self._get_results()
        objects = tuple(x for x in range(20))
        y_pos = np.arange(20)
        plt.bar(y_pos, sentiments[:20], align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Sentiment')
        plt.xlabel('Tweet Count')
        plt.title('Tweets Sentiment Graph for {}'.format(self.word))
        plt.savefig('sentiment_results_tweets_{}.png'.format(self.word))

    def _get_tweet_coefficient(self):
        total_tweets, negative_tweets, positive_tweets,_ = self._get_results()
        pos_percentage = (positive_tweets/total_tweets)
        neg_percentage = (negative_tweets/total_tweets)
        if pos_percentage > neg_percentage:
            neg_percentage *= coeff
        else:
            pos_percentage *= coeff
        self.graph_sentiment()
        return pos_percentage, neg_percentage
