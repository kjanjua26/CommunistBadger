"""
    CommunistBadger v1.0.0
    This is the code for the model which will be trained to predict the sentiment analysis for tweets.
"""

from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import re

def cleansing(tweet):
    tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub('@[^\s]+','AT_USER', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub(r'\W*\b\w{1,3}\b', '', tweet)
    return tweet

def model():
    model = Sequential()
    model.add(Embedding(max_features, 32, input_length=20)) # Embedding for input tweets
    model.add(Conv1D(filters=128, kernel_size=5, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    model.add(Conv1D(filters=64, kernel_size=6, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    model.add(Conv1D(filters=32, kernel_size=7, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    model.add(Conv1D(filters=32, kernel_size=8, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    return model

data = pd.read_csv("Data/train_data_1.6m.csv", encoding="ISO-8859-1", header=None).iloc[:, [0, 4, 5]].sample(frac=1).reset_index(drop=True)
tweets = np.array(data.iloc[:, 2].apply(cleansing).values)
y = np.array(data.iloc[:, 0].values)
y[y == 4] = 1
max_features = 400000
tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts(tweets)
tokenizer_padded = tokenizer.texts_to_sequences(tweets)
x = np.array(sequence.pad_sequences(tokenizer_padded, maxlen=20, padding='post'))

model = model()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
X_train, x_test, Y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
batch_size = 128
model.fit(X_train, Y_train, nb_epoch=10, batch_size=batch_size, verbose=1)

validation_size = 100000
x_valid = x_test[-validation_size:]
y_valid = y_test[-validation_size:]
x_test = x_test[:-validation_size]
y_test = y_test[:-validation_size]
score, acc = model.evaluate(x_test, y_test, verbose=0, batch_size=batch_size)
print("\n")
print("The accuracy is: %.5f" % (acc))
print("\nSaving Model.")

model.save('Models/conv-1D-1.6-weights.h5')