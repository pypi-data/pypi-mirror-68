from .data import _load_tsv_data
from .models import build_cnn_model, build_dnn_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from sklearn.model_selection import KFold
import pandas as pd
from keras.callbacks import EarlyStopping
from sklearn.metrics import f1_score, precision_score, recall_score

# set hyperparameters:
MAX_FEATURES = 5000
MAX_LEN = 100
BATCH_SIZE = 32
EPOCHS = 20


def _pre_process_texts(texts):
    sequences = tokenizer.texts_to_sequences(texts)
    result = pad_sequences(sequences, padding='post', truncating='post', maxlen=MAX_LEN)
    return result


def _pre_process_texts_2(texts):
    sequences = tokenizer.texts_to_sequences(texts)
    result = tokenizer.sequences_to_matrix(sequences, mode='count')
    return result


def _load_imdb_data():
    _data = pd.read_csv('imdb.csv')
    _data['sentiment'] = _data['sentiment'].map({'negative': 0, 'positive': 1})
    _data.rename(columns={"review": "Review", "sentiment": "Label"}, inplace=True)
    return _data


tokenizer = Tokenizer(num_words=MAX_FEATURES)

callbacks_list = [
    EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)
]

data = _load_imdb_data()
data = data.sample(5000)

all_scores = []
k_fold = KFold(n_splits=5, shuffle=True)
splits = k_fold.split(data)

for train_index, test_index in splits:
    X_train = data.iloc[train_index, [0]].to_numpy().flatten()
    y_train = data.iloc[train_index, [1]].to_numpy().flatten()

    X_test = data.iloc[test_index, [0]].to_numpy().flatten()
    y_test = data.iloc[test_index, [1]].to_numpy().flatten()

    tokenizer.fit_on_texts(X_train)

    X_train = _pre_process_texts_2(X_train)
    X_test = _pre_process_texts_2(X_test)

    # model = build_cnn_model(MAX_FEATURES, MAX_LEN)
    model = build_dnn_model(MAX_FEATURES)

    history = model.fit(x=X_train,
                        y=y_train,
                        epochs=EPOCHS,
                        batch_size=BATCH_SIZE,
                        validation_split=0.1,
                        callbacks=callbacks_list)

    metrics = model.evaluate(X_test, y_test)

    predictions = model.predict(X_test).flatten()
    predictions = np.where(predictions > 0.5, 1, 0)
    f1 = f1_score(y_test, predictions, average='macro')
    precision = precision_score(y_test, predictions, average='macro')
    recall = recall_score(y_test, predictions, average='macro')
    metrics.append(f1)
    metrics.append(precision)
    metrics.append(recall)
    all_scores.append(metrics)

print(all_scores)
average = np.mean(all_scores, axis=0)
print(average)

# from keras.models import load_model
import json
with open('word_dict.json', 'w') as file:
    json.dump(tokenizer.word_index, file)
model.save('imdb_model.h5')
# model = load_model('imdb_model.h5')
