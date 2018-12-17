"""
    CommunistBadger v1.0.0
    This is the code for index computation of stock analysis.
    We perform analysis on news, tweets and stock and compute market index.
    Market Index: lambda1*PT/TT+lambda2*NT/TT+lambda2*CV(stock(n,t))
"""
import predict_sentiment_news, predict_sentiment_tweets

class MarketIndex():
    def __init__(self, article_name):
        self.article_name = article_name

    def compute_tweet_index(self):
        predict_sentiment_tweets._get_tweet_coefficient()

    def compute_news_index(self):
        sentiment = predict_sentiment_news.SentimentNews(self.article_name)
        sentiment.graph_sentiment()
        pos_percentage, neg_percentage = sentiment.compute_score()
        print("Positive Percentage: ", pos_percentage)
        print("Negative Percentaage: ", neg_percentage)

if __name__ == '__main__':
    index = MarketIndex("Google")
    index.compute_news_index()
