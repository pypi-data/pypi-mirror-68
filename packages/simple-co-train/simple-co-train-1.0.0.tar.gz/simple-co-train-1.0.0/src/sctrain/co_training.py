import pandas as pd
from keras.callbacks import EarlyStopping
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from .models import build_cnn_model, build_dnn_model
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from enum import Enum
from .data import _load_from_csv, _load_from_path

callbacks_list = [
    EarlyStopping(monitor='val_accuracy', patience=2, restore_best_weights=True)
]

# set hyperparameters:
MAX_FEATURES = 5000
MAX_LEN = 100
BATCH_SIZE = 32
EPOCHS = 20

# co-training hyperparameters
MAX_ROUNDS = 20

UNCERTAINTY_FLOOR = 0.4
UNCERTAINTY_CEIL = 0.6

CERTAINTY_LOWER = 0.1
CERTAINTY_UPPER = 0.9


class SelectionStrategy(Enum):
    UNSURE_ONLY = 1
    CONFIDENT_ONLY = 2
    BOTH = 3


class CoTrainer:
    """
        This class orchestrates co-training
    """

    _tokenizer: Tokenizer = Tokenizer(num_words=MAX_FEATURES)

    def __init__(self,
                 data_path='data.csv',
                 x_name='text',
                 y_name='label',
                 unlabelled_size=0.9,
                 train_size=0.8,
                 mapping=None,
                 selection: SelectionStrategy = SelectionStrategy.UNSURE_ONLY):

        if data_path.endswith('.csv') or data_path.endswith('.tsv'):
            self._labelled, self._validation, self._unlabelled = _load_from_csv(data_path,
                                                                                unlabelled_size=unlabelled_size,
                                                                                train_size=train_size,
                                                                                y_name=y_name,
                                                                                mapping=mapping)
        else:
            self._labelled, self._validation, self._unlabelled = _load_from_path(data_path,
                                                                                 unlabelled_size=unlabelled_size,
                                                                                 train_size=train_size,
                                                                                 y_name=y_name,
                                                                                 mapping=mapping)

        self._x_name = x_name
        self._y_name = y_name
        self._selection = selection
        self.unsure_labelled = []
        self.recalls = []
        self.precisions = []
        self.f1_scores = []
        self.accuracies = []

    def _pre_process_texts(self, texts):
        sequences = self._tokenizer.texts_to_sequences(texts)
        return pad_sequences(sequences, padding='post', truncating='post', maxlen=MAX_LEN)

    def _pre_process_texts_2(self, texts):
        sequences = self._tokenizer.texts_to_sequences(texts)
        return self._tokenizer.sequences_to_matrix(sequences, mode='count')

    def _confident_only(self):
        most_confident_positive = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence > CERTAINTY_UPPER) &
            (self._pseudo_labelled.Confidence_2 > CERTAINTY_UPPER)
        ]
        most_confident_negative = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence < CERTAINTY_LOWER) &
            (self._pseudo_labelled.Confidence_2 < CERTAINTY_LOWER)
        ]

        most_confident_positive = most_confident_positive[[self._x_name, self._y_name]]
        most_confident_negative = most_confident_negative[[self._x_name, self._y_name]]

        # add to the labelled data
        self._labelled = pd.concat(
            [
                self._labelled,
                most_confident_positive,
                most_confident_negative
            ],
            axis=0,
            ignore_index=True)

        return most_confident_positive.index.tolist() + most_confident_negative.index.tolist()

    def _unsure_only(self):
        most_unsure_positive = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence > UNCERTAINTY_FLOOR) &
            (self._pseudo_labelled.Confidence < UNCERTAINTY_CEIL) &
            (self._pseudo_labelled.Confidence_2 > CERTAINTY_UPPER)
        ]
        most_unsure_positive_2 = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence_2 > UNCERTAINTY_FLOOR) &
            (self._pseudo_labelled.Confidence_2 < UNCERTAINTY_CEIL) &
            (self._pseudo_labelled.Confidence > CERTAINTY_UPPER)
        ]

        most_unsure_negative = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence > UNCERTAINTY_FLOOR) &
            (self._pseudo_labelled.Confidence < UNCERTAINTY_CEIL) &
            (self._pseudo_labelled.Confidence_2 < CERTAINTY_LOWER)
        ]
        most_unsure_negative_2 = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence_2 > UNCERTAINTY_FLOOR) &
            (self._pseudo_labelled.Confidence_2 < UNCERTAINTY_CEIL) &
            (self._pseudo_labelled.Confidence < CERTAINTY_LOWER)
        ]

        most_unsure_positive = most_unsure_positive[[self._x_name, self._y_name + '_2']]
        most_unsure_positive.rename(columns={self._x_name: self._x_name, self._y_name + '_2': self._y_name}, inplace=True)
        most_unsure_positive_2 = most_unsure_positive_2[[self._x_name, self._y_name]]

        most_unsure_negative = most_unsure_negative[[self._x_name, self._y_name + '_2']]
        most_unsure_negative.rename(columns={self._x_name: self._x_name, self._y_name + '_2': self._y_name}, inplace=True)
        most_unsure_negative_2 = most_unsure_negative_2[[self._x_name, self._y_name]]

        # add to the labelled data
        self._labelled = pd.concat(
            [
                self._labelled,
                most_unsure_negative,
                most_unsure_negative_2,
                most_unsure_positive,
                most_unsure_positive_2
            ],
            axis=0,
            ignore_index=True)

        return most_unsure_negative.index.tolist() + most_unsure_negative_2.index.tolist() + most_unsure_positive.index.tolist() + most_unsure_positive_2.index.tolist()

    def _co_train(self):
        count = 0

        if self._selection is SelectionStrategy.CONFIDENT_ONLY or self._selection is SelectionStrategy.BOTH:
            indexes = self._confident_only()
            count = count + len(indexes)
            self._pseudo_labelled.drop(indexes, inplace=True)

        if self._selection is SelectionStrategy.UNSURE_ONLY or self._selection is SelectionStrategy.BOTH:
            indexes = self._unsure_only()
            count = count + len(indexes)
            self._pseudo_labelled.drop(indexes, inplace=True)

        self.unsure_labelled.append(count)

    def _pseudo_label(self, u):
        unlabelled_preprocessed = self._pre_process_texts(u)
        unlabelled_preprocessed_2 = self._pre_process_texts_2(u)

        predictions = self._model.predict(unlabelled_preprocessed).flatten()
        predictions_2 = self._model_2.predict(unlabelled_preprocessed_2).flatten()

        self._pseudo_labelled = pd.DataFrame({
            self._x_name: u,
            self._y_name: [1 if p > 0.5 else 0 for p in predictions],
            'Confidence': predictions,
            self._y_name + '_2': [1 if p2 > 0.5 else 0 for p2 in predictions_2],
            'Confidence_2': predictions_2
        })

    def _train_model(self):
        reviews_train = self._labelled[self._x_name].to_numpy()
        y_train = self._labelled[self._y_name].to_numpy()

        self._tokenizer.fit_on_texts(reviews_train)

        x_train = self._pre_process_texts(reviews_train)
        x_validate = self._pre_process_texts(self._validation[self._x_name].to_numpy())

        x_train_2 = self._pre_process_texts_2(reviews_train)
        x_validate_2 = self._pre_process_texts_2(self._validation[self._x_name].to_numpy())

        y_validate = self._validation[self._y_name].to_numpy()

        self._model = build_cnn_model(MAX_FEATURES, MAX_LEN)
        self._model_2 = build_dnn_model(MAX_FEATURES)

        self._model.fit(x=x_train,
                        y=y_train,
                        epochs=EPOCHS,
                        validation_data=(x_validate, y_validate),
                        batch_size=BATCH_SIZE,
                        callbacks=callbacks_list)

        self._model_2.fit(x=x_train_2,
                          y=y_train,
                          epochs=EPOCHS,
                          validation_data=(x_validate_2, y_validate),
                          batch_size=BATCH_SIZE,
                          callbacks=callbacks_list)

        predictions = self._model.predict(x_validate).flatten()
        predictions_2 = self._model_2.predict(x_validate_2).flatten()
        predictions_ensemble = (predictions + predictions_2) / 2.0

        predictions = [1 if p > 0.5 else 0 for p in predictions]
        predictions_2 = [1 if p > 0.5 else 0 for p in predictions_2]
        predictions_ensemble = [1 if p > 0.5 else 0 for p in predictions_ensemble]

        self.precisions.append([
            precision_score(y_validate, predictions, average='macro'),
            precision_score(y_validate, predictions_2, average='macro'),
            precision_score(y_validate, predictions_ensemble, average='macro')])
        self.recalls.append([
            recall_score(y_validate, predictions, average='macro'),
            recall_score(y_validate, predictions_2, average='macro'),
            recall_score(y_validate, predictions_ensemble, average='macro')])
        self.f1_scores.append([
            f1_score(y_validate, predictions, average='macro'),
            f1_score(y_validate, predictions_2, average='macro'),
            f1_score(y_validate, predictions_ensemble, average='macro')])
        self.accuracies.append([
            accuracy_score(y_validate, predictions),
            accuracy_score(y_validate, predictions_2),
            accuracy_score(y_validate, predictions_ensemble)
        ])

    def run(self):
        self._train_model()
        self._pseudo_label(self._unlabelled[self._x_name].to_numpy())

        for i in range(MAX_ROUNDS):
            print(f'CO-TRAINING ROUND {i + 1}/{MAX_ROUNDS}')
            self._co_train()
            self._train_model()

            if len(self._pseudo_labelled) < 1000:
                break

            self._pseudo_label(self._pseudo_labelled[self._x_name].to_numpy())
