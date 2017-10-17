# coding=utf-8
import numpy as np

from keras.models import Sequential
from keras.layers import Activation
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from keras.utils.vis_utils import plot_model
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization
import matplotlib.pyplot as plt
import pandas as pd
import os

# Set Data Value
timesteps = seq_length = 30 #30분 마다의 값
data_dim = 5 #input data
output_dim = 1 # output data

# Data Load
data = pd.DataFrame.from_csv('data/etc.csv') # btc , bch, etc, eth, qtum, xrp
data = data[['first', 'high', 'low', 'volume', 'last']].values
scaler = MinMaxScaler(feature_range=(0, 1))  # 데이터 크기가 들쑥날쑥할때 0 ~ 1 사이의 값으로 분포시켜준다
data = scaler.fit_transform(data)

x = data
y = data[:, [-1]] #label data

dataX = []
dataY = []

# Sequence Set
for i in range(0, len(y) - seq_length):
    _x = x[i:i + seq_length]
    _y = y[i + seq_length]
    print (_x, "->", _y)
    dataX.append(_x)
    dataY.append(_y)

# Split to Train and Testing
train_size = int(len(dataY) * 0.7)
test_size = len(dataY) - train_size

trainX, testX = np.array(dataX[0:train_size]), \
                np.array(dataX[train_size:len(dataX)])
trainY, testY = np.array(dataY[0:train_size]),\
                np.array(dataY[train_size:len(dataY)])


model = Sequential()

# RNNs 의 변형 LSTM
model.add(LSTM(units=1, input_shape=(seq_length, data_dim),
                return_sequences=False))

model.add(Dense(1)) #뉴런
model.add(Activation('tanh')) #활성 함수
model.load_weights('model.h5') # model(가중치 값) 불러오기

# loss function, 최적화 함수
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

model.summary()

#Layer 구성 방식을 .png로 export
plot_model(model, to_file=os.path.basename(__file__) + '.png', show_shapes=True)

print (trainX.shape, trainY.shape)

# model.fit(trainX, trainY, epochs=200)  #<<--- model load시 사용하지 않아도 됨
# model.save_weights("model.h5") # model 저장

testPredict = model.predict(testX)
#차이값을 줄이기 위하여 MinMaxScaler 재적용
testY = scaler.fit_transform(testY)
testPredict = scaler.fit_transform(testPredict)

#그래프로 표현
plt.plot(testY)
plt.plot(testPredict)
plt.show()
