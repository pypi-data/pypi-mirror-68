from keras.models import Sequential
from keras import layers
from enum import Enum


class PoolingStrategy(Enum):
    MAX = 1
    AVERAGE = 2
    NONE = 3


def build_cnn_model(input_dim, input_length, pooling=PoolingStrategy.MAX) -> Sequential:
    if pooling is PoolingStrategy.MAX:
        pooling_layer = layers.GlobalMaxPooling1D()
    elif pooling is PoolingStrategy.AVERAGE:
        pooling_layer = layers.GlobalAveragePooling1D()
    else:
        pooling_layer = layers.Flatten()

    model = Sequential([
        layers.Embedding(input_dim=input_dim, output_dim=64, input_length=input_length),
        layers.Conv1D(filters=64, kernel_size=5, activation='relu'),
        pooling_layer,
        layers.Dense(10, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def build_dnn_model(input_dim) -> Sequential:
    model = Sequential([
        layers.Dense(64, input_dim=input_dim, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def build_rnn_model(input_dim, input_length) -> Sequential:
    model = Sequential([
        layers.Embedding(input_dim=input_dim, output_dim=64, input_length=input_length),
        layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
        layers.Bidirectional(layers.LSTM(32)),
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(8, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model
