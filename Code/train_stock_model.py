"""
    CommunistBadger v1.0.0
    This is the code for neural network used in the stock prediction.
    We use LSTM and GRUs for the task. We use tensorflow for the task.
"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import Stock_Data_Renderer

class StockPredictor():
    def __init__(self, stockfile):
        self.stockfile = stockfile
        self.batch_size = 32
        self.seq_length = 20
        self.neurons = 256
        self.epochs = 50
        self.data_split = 0.33
        self.no_units_lstm = 4
        self.activation = tf.nn.elu
        self.no_outputs = 4
        self.no_inputs = 4
        self.no_steps = 19
        self.learning_rate = 0.001
        self.X = tf.placeholder(tf.float32, [None, self.no_steps, self.no_inputs])
        self.Y = tf.placeholder(tf.float32, [None, self.no_outputs])


    def model_(self):
        lstm_cells = [tf.contrib.rnn.BasicRNNCell(num_units=self.neurons, activation=self.activation) for _ in range(self.no_units_lstm)]
        stacked_lstm = tf.contrib.rnn.MultiRNNCell(lstm_cells)
        rnn_outputs, states = tf.nn.dynamic_rnn(stacked_lstm, self.X, dtype=tf.float32)
        reshaped_outputs = tf.reshape(rnn_outputs, [-1, self.neurons])
        combined_outputs = tf.layers.dense(reshaped_outputs, self.no_outputs)
        outputs = tf.reshape(combined_outputs, [-1, self.no_steps, self.no_outputs])
        outputs = outputs[:, self.no_steps - 1, :]  # keep only last output of the sequence
        return outputs

    def training_ops(self):
        returned_outputs = self.model_()
        loss = tf.losses.mean_squared_error(self.Y, returned_outputs)  # MSE for real valued data.
        return loss, returned_outputs

    def train_network(self):
        DataRenderer = Stock_Data_Renderer.StockDataRenderer(self.stockfile)
        x_train, y_train, x_valid, y_valid, x_test, y_test = DataRenderer.render_data()
        x_batch, y_batch = DataRenderer.next_batch(self.batch_size, x_train, y_train)
        loss, outputs = self.training_ops()
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        ops = optimizer.minimize(loss)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        for epoch in range(self.epochs):
            train_loss, _ = sess.run([loss, ops], feed_dict={self.X: x_batch, self.Y: y_batch})
            print("Epoch: {} Loss: {}".format(epoch, train_loss))
            if epoch % 10 == 0:
                val_loss, _ = sess.run([loss, ops], feed_dict={self.X: x_valid, self.Y: y_valid})
                print("Validation Time!")
                print("Val Loss: {}".format(val_loss))
                save_path = saver.save(sess, "Models/model-stock-epoch{}.ckpt".format(epoch))
                print("Model saved for epoch # {}".format(epoch))
                print("")
        y_train_pred = sess.run(outputs, feed_dict={self.X: x_train})
        y_valid_pred = sess.run(outputs, feed_dict={self.X: x_valid})
        y_test_pred = sess.run(outputs, feed_dict={self.X: x_test})

if __name__ == '__main__':
    pred = StockPredictor("Data/Stocks/EBAY.csv")
    pred.train_network()
