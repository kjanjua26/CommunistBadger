"""
    CommunistBadger v1.0.0
    This is the code for machine learning based stock price fitter network used in the stock prediction.
    We use SVM with RBF as kernel for the task.
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVR



class MLPredictor():
    def __init__(self):
        self.dates = []
        self.prices = []

    # Read CSV file
    def readFile(self, filename):
        with open(filename, "r") as csvfile:
            fileReader = csv.reader(csvfile)
            next(fileReader)
            for row in fileReader:
                self.dates.append(int(row[0].split('-')[0]))
                self.prices.append(float(row[1]))
        return self.dates, self.prices


    # Predict the apple stock prices.
    def predict_prices(self, dates, prices):
        dates = np.reshape(dates, (len(dates), 1))
        rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        rbf.fit(dates, prices)
        plt.title("Fit on Apple Stocks")
        plt.scatter(dates, prices, color="black", label='Data')  # dates is x and prices are y
        plt.plot(dates, rbf.predict(dates), color="red", label="RBF")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        return rbf.predict(dates)[0]

if __name__ == '__main__':
    mlpred = MLPredictor()
    dates, prices = mlpred.readFile('Data/aapl.csv')
    predicted_price = mlpred.predict_prices(dates, prices)
    print("The price will move from", prices[0], "to", ":", predicted_price)
