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
    def __init__(self, stockfile, mode, iftrain):
        self.mode = mode
        self.iftrain = iftrain
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
                saver.save(sess, "Models/model-stock-epoch{}-{}.ckpt".format(epoch, self.stockfile.split('/')[-1].replace('.csv','')))
                print("Model saved for epoch # {}".format(epoch))
                print("")
        y_train_pred = sess.run(outputs, feed_dict={self.X: x_train})
        y_test_pred = sess.run(outputs, feed_dict={self.X: x_test})
        return y_test_pred, y_train_pred

    def plot_predictions(self):
        DataRenderer = Stock_Data_Renderer.StockDataRenderer(self.stockfile)
        _, y_train, _, _, x_test, _ = DataRenderer.render_data()
        outputs = self.model_()
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            tf.train.get_checkpoint_state("Models")
            saver.restore(sess, "Models/model-stock-epoch40-{}.ckpt".format(self.stockfile.split('/')[-1].replace('.csv','')))
            prediction = sess.run(outputs, feed_dict={self.X:x_test})

        unnorm_pred = DataRenderer.unnormalize(prediction) # un-normalizing the values since we normalized them.
        ft = 0  # 0 = open, 1 = close, 2 = highest, 3 = lowest
        plt.plot(np.arange(y_train.shape[0], y_train.shape[0] + prediction.shape[0]), unnorm_pred[:, ft], color='black')
        plt.title('Predicted Stock Prices For {}'.format(self.stockfile.split('/')[-1].replace('.csv','')))
        plt.xlabel('Time [Days]')
        plt.ylabel('Price')
        plt.savefig("stock_prediction_{}.png".format(self.stockfile.split('/')[-1].replace('.csv','')))
        plt.close()

        candleStickList = []
        for vals in list(unnorm_pred):
            open, close, high, low = list(vals)
            vals_to_append = open, close, high, low
            candleStickList.append(vals_to_append)
        return candleStickList

    def run(self):
        if self.iftrain:
            self.train_network()
        else:
            pred = self.plot_predictions()
