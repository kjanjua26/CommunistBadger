"""
    CommunistBadger v1.0.0
    This is the code for data rendering for the model_stock_prediction.py.
    We preprocess the data and prepare it for the network.
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

class StockDataRenderer():
    def __init__(self, file_name):
        self.file = file_name
        self.seq_len = 20
        self.valid_data_percent = 10
        self.test_data_percent = 10

    def normalize(self, df):
        min_max_scaler = MinMaxScaler()
        df['open'] = min_max_scaler.fit_transform(df.open.values.reshape(-1, 1))
        df['high'] = min_max_scaler.fit_transform(df.high.values.reshape(-1, 1))
        df['low'] = min_max_scaler.fit_transform(df.low.values.reshape(-1, 1))
        df['close'] = min_max_scaler.fit_transform(df['close'].values.reshape(-1, 1))
        return df

    def load_stock(self, stock):
        data_raw = stock.as_matrix()
        data = []
        for index in range(len(data_raw) - self.seq_len):
            data.append(data_raw[index: index + self.seq_len])
        data = np.array(data)
        valid_set_size = int(np.round(self.valid_data_percent / 100 * data.shape[0]));
        test_set_size = int(np.round(self.test_data_percent / 100 * data.shape[0]));
        train_set_size = data.shape[0] - (valid_set_size + test_set_size);
        x_train = data[:train_set_size, :-1, :]
        y_train = data[:train_set_size, -1, :]
        x_valid = data[train_set_size:train_set_size + valid_set_size, :-1, :]
        y_valid = data[train_set_size:train_set_size + valid_set_size, -1, :]
        x_test = data[train_set_size + valid_set_size:, :-1, :]
        y_test = data[train_set_size + valid_set_size:, -1, :]
        return [x_train, y_train, x_valid, y_valid, x_test, y_test]

    def render_data(self):
        df = pd.read_csv(self.file)
        df.drop(['day'],1,inplace=True)
        df.drop(['volume'],1,inplace=True)
        df_stock = df.copy()
        df_stock_norm = self.normalize(df_stock)
        x_train, y_train, x_valid, y_valid, x_test, y_test = self.load_stock(df_stock_norm)
        return x_train, y_train, x_valid, y_valid, x_test, y_test

    def next_batch(self, num, data, labels):
        idx = np.arange(0, len(data))
        np.random.shuffle(idx)
        idx = idx[:num]
        data_shuffle = [data[i] for i in idx]
        labels_shuffle = [labels[i] for i in idx]
        return np.asarray(data_shuffle), np.asarray(labels_shuffle)
