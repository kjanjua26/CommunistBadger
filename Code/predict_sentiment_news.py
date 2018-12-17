"""
    CommunistBadger v1.0.0
    This is the code for the predicting the sentiment from news scrapped from news sources.
"""

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
import numpy as np
import re
import pandas as pd
import glob



class SentimentNews():
    def __init__(self, article_name):
        self.articles = []
        self.pos_list = []
        self.neg_list = []
        self.coeff = 0.01
        self.article_name = article_name
        self.file_name = "Articles/"
        self.model = load_model('Models/conv-1D-1.6-weights.h5')
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.max_features = 400000  # vocabulary size

    def cleansing(self, article):
        article.lower()
        article = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', article)
        article = re.sub('@[^\s]+', ' ', article)
        article = re.sub('[\s]+', ' ', article)
        article = re.sub(r'#([^\s]+)', r'\1', article)
        article = re.sub(r'\W*\b\w{1,3}\b', '', article)
        return article

    def parse_news(self):
        for ix in glob.glob(self.file_name+"*.csv"):
            if self.article_name in ix:
                data_frame = pd.read_csv(ix)
        articles = data_frame['Article']
        for article in articles:
            self.articles.append(self.cleansing(article))

    def get_sentiment(self):
        self.parse_news()
        tokenizer = Tokenizer(num_words=40000)
        tokenizer.fit_on_texts(self.articles)
        tokenizer_padded = tokenizer.texts_to_sequences(self.articles)
        x = np.array(sequence.pad_sequences(tokenizer_padded, maxlen=20, padding='post'))
        out = self.model.predict_classes(x, batch_size=1)
        flat_out = [y for x in out for y in x]
        pos_count = 0; neg_count = 0
        for index in range(len(flat_out)):
            if flat_out[index] == 1:
                pos_count += 1
                self.pos_list.append(self.articles[index])
            else:
                neg_count += 1
                self.neg_list.append(self.articles[index])
        assert pos_count + neg_count == len(flat_out)
        return pos_count, neg_count, len(flat_out)

    def compute_score(self):
        pos_count, neg_count, total_count = self.get_sentiment()
        pos_percentage = (pos_count / total_count)
        neg_percentage = (neg_count / total_count)
        diff_percentage = (pos_percentage - neg_percentage)
        if diff_percentage > 0.10:  # if the diff is less than a certain percentage, then negative is dominant.
            neg_percentage *= self.coeff
        else:
            pos_percentage *= self.coeff
        return pos_percentage, neg_percentage



if __name__ == '__main__':
    sentiment = SentimentNews("Google")
    pos_percentage, neg_percentage = sentiment.compute_score()
    print("Positive Percentage: ", pos_percentage)
    print("Negative Percentaage: ", neg_percentage)
