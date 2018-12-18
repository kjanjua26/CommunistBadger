"""
    CommunistBadger v1.0.0
    This is the code for index computation of stock analysis.
    We perform analysis on news, tweets and stock and compute market index.
    Market Index: lambda1*PT/TT+lambda2*NT/TT+lambda2*sum(CV(stock(n,t)))
"""
import predict_sentiment_news, predict_sentiment_tweets, model_stock_prediction
import numpy as np

class MarketIndex():
    def __init__(self, name, tweet_count):
        self.name = name
        self.tweet_count = tweet_count
        self.open_lst = []
        self.close_lst = []
        self.high_lst = []
        self.low_lst = []

    def compute_tweet_index(self):
        sentiment = predict_sentiment_tweets.SentimentTweets(self.name, self.tweet_count)
        pos_percentage, neg_percentage = sentiment._get_tweet_coefficient()
        print("Positive Percentage: ", pos_percentage)
        print("Negative Percentaage: ", neg_percentage)

    def compute_news_index(self):
        sentiment = predict_sentiment_news.SentimentNews(self.name)
        sentiment.graph_sentiment()
        pos_percentage, neg_percentage = sentiment.compute_score()
        print("Positive Percentage: ", pos_percentage)
        print("Negative Percentaage: ", neg_percentage)

    def stock_index(self):
        stockModel = model_stock_prediction.StockPredictor("Data/Stocks/{}.csv".format(self.name), "LSTM", False)
        predictions = stockModel.run()
        for pred in predictions:
            open, close, high, low = pred
            self.open_lst.append(open)
            self.close_lst.append(close)
            self.high_lst.append(high)
            self.low_lst.append(low)
        print("Computing Variance")
        open_arr = np.asarray(self.open_lst)
        close_arr = np.asarray(self.close_lst)
        high_arr = np.asarray(self.high_lst)
        low_arr = np.asarray(self.low_lst)
        open_var = np.var(open_arr)
        close_var = np.var(close_arr)
        high_var = np.var(high_arr)
        low_var = np.var(low_arr)
        total_variation = open_var + close_var + high_var + low_var
        print("{} Variation: ".format(self.name), total_variation)

if __name__ == '__main__':
    index = MarketIndex("FB", 100)
    index.stock_index()
