"""
    CommunistBadger v1.0.0
    This is the code for plotting candlestick graphs of stock data.
"""
import pandas as pd
from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import glob

class PlotGraph():
    def plot_graph(self, stockName):
        df = pd.read_csv(stockName)
        fig, ax = plt.subplots()
        try:
            candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.9)
            plt.xlabel('Date')
            plt.ylabel('Price')
            print("Plotting -> {}".format(stockName))
            stock_plot = stockName.split('.csv')[0].split('/')[1]
            plt.title("Stock Graph For {}".format(stock_plot))
            plt.savefig('Visualizations/candlestick_{}.png'.format(stock_plot))
        except:
            print("Error -> {}".format(stockName))

    def run(self):
       for stock in glob.glob("Data/Stocks/"+"*.csv"):
           self.plot_graph(stock)

if __name__ == '__main__':
    graph = PlotGraph()
    graph.run()
