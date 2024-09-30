# -*- coding: utf-8 -*-
"""RNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15WEXd6TzXXbrHrgtnqZ2IsAuT6WDHqh2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
dataset = pd.read_csv('/home/zayan/Downloads/DL/codeanddataset-221103-211006/code and dataset/Google_Stock_Price_Train.csv')

dataset.head()

training_set = dataset.iloc[:,1:2].values

training_set

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

training_set_scaled

training_set_scaled.shape

X_train = []
Y_train = []

for i in range(60,1258):
  X_train.append(training_set_scaled[i-60:i,0])
  Y_train.append(training_set_scaled[i,0])

X_train, Y_train = np.array(X_train), np.array(Y_train)

X_train

X_train.shape

Y_train.shape

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_train.shape

X_train

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()

regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units=1))

regressor.compile(optimizer='adam', loss='mean_squared_error')

regressor.fit(X_train, Y_train, epochs=100, batch_size=32)

dataset_test = pd.read_csv("/home/zayan/Downloads/DL/codeanddataset-221103-211006/code and dataset/Google_Stock_Price_Test.csv")
real_stock = dataset_test.iloc[:,1:2]
real_stock

dataset_total = pd.concat((dataset['Open'], dataset_test['Open']), axis=0)
dataset_total

inputs = dataset_total[len(dataset_total)-len(dataset_test)-60:].values
inputs

inputs.shape

inputs = inputs.reshape(-1,1)
inputs.shape

inputs = sc.transform(inputs)

inputs

X_test = []
for i in range(60,80):
  X_test.append(inputs[i-60:i,0])

X_test = np.array(X_test)
X_test.shape

X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
X_test.shape

predicted_stock = regressor.predict(X_test)

predicted_stock = sc.inverse_transform(predicted_stock)
predicted_stock

plt.plot(real_stock, color='red', label='Real Google Stock Price')
plt.plot(predicted_stock, color='blue', label='Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()
