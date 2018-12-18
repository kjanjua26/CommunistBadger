"""
    CommunistBadger v1.0.0
    This is the code for plotting candlestick graphs of stock data.
"""
import pandas as pd
from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt

class PlotGraph():
    def __init__(self, stockName):
        self.stockName = stockName


    def plot_graph(self):
        df = pd.read_csv("Data/{}.csv".format(self.stockName))
        fig, ax = plt.subplots()
        candlestick2_ohlc(ax, df['Open'], df['High'], df['Low'], df['Close'], width=0.9)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title("Stock Graph For {}".format(self.stockName))
        plt.savefig('candlestick_{}'.format(self.stockName))
        plt.show()

if __name__ == '__main__':
    graph = PlotGraph("aapl")
    graph.plot_graph()
