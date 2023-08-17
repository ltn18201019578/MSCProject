from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os
import numpy as np
from keras.utils import plot_model

# Define model architecture
from tensorflow.keras.layers import Dropout
from tensorflow.keras.regularizers import l2
def create_model():
    model = Sequential()
    model.add(LSTM(256, return_sequences=True, input_shape=(13, 164), kernel_regularizer=l2(0.01)))  # LSTM layer
    model.add(Dropout(0.5))
    model.add(LSTM(128, kernel_regularizer=l2(0.01)))  # LSTM layer
    model.add(Dropout(0.5))
    model.add(Dense(64, activation ='relu'))  # Dense layer
    model.add(Dense(4, activation ='softmax'))  # Output layer
    # Compile the model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# 创建模型
model = create_model()

# 绘制模型结构图，并保存为图片文件
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)