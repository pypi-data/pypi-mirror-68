from abc import ABC, abstractmethod
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from .models import build_cnn_model, build_dnn_model
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

callbacks_list = [
    EarlyStopping(monitor='val_accuracy', patience=2, restore_best_weights=True)
]

# set hyperparameters:
MAX_FEATURES = 5000
MAX_LEN = 100
BATCH_SIZE = 32
EPOCHS = 20

# co-training hyperparameters
MAX_ROUNDS = 10

CERTAINTY_LOWER = 0.01
CERTAINTY_UPPER = 0.99


class SelfTrainer(ABC):
    """
        This class orchestrates self-training
    """

    _tokenizer: Tokenizer = Tokenizer(num_words=MAX_FEATURES)

    def __init__(self,
                 labelled: pd.DataFrame,
                 validation: pd.DataFrame,
                 unlabelled: pd.DataFrame):
        self._labelled = labelled
        self._validation = validation
        self._unlabelled = unlabelled
        self.unsure_labelled = []
        self.recalls = []
        self.precisions = []
        self.f1_scores = []
        self.accuracies = []

    @abstractmethod
    def _pre_process_texts(self, texts):
        pass

    @abstractmethod
    def _build_model(self):
        pass

    def _confident_only(self):
        most_confident = self._pseudo_labelled[
            (self._pseudo_labelled.Confidence > CERTAINTY_UPPER) |
            (self._pseudo_labelled.Confidence < CERTAINTY_LOWER)
        ]

        most_confident = most_confident[['Review', 'Label']]

        # add to the labelled data
        self._labelled = pd.concat([self._labelled, most_confident], axis=0, ignore_index=True)

        return most_confident.index.tolist()

    def _self_train(self):
        indexes = self._confident_only()
        self._pseudo_labelled.drop(indexes, inplace=True)
        self.unsure_labelled.append(len(indexes))

    def _pseudo_label(self, u):
        unlabelled_preprocessed = self._pre_process_texts(u)

        predictions = self._model.predict(unlabelled_preprocessed).flatten()

        self._pseudo_labelled = pd.DataFrame({
            'Review': u,
            'Label': [1 if p > 0.5 else 0 for p in predictions],
            'Confidence': predictions
        })

    def _train_model(self):
        reviews_train = self._labelled['Review'].to_numpy()
        y_train = self._labelled['Label'].to_numpy()

        self._tokenizer.fit_on_texts(reviews_train)

        x_train = self._pre_process_texts(reviews_train)
        x_validate = self._pre_process_texts(self._validation['Review'].to_numpy())

        y_validate = self._validation['Label'].to_numpy()

        self._model = self._build_model()

        self._model.fit(x=x_train,
                        y=y_train,
                        epochs=EPOCHS,
                        validation_data=(x_validate, y_validate),
                        batch_size=BATCH_SIZE,
                        callbacks=callbacks_list)

        predictions = self._model.predict(x_validate).flatten()

        predictions = [1 if p > 0.5 else 0 for p in predictions]

        self.precisions.append(precision_score(y_validate, predictions, average='macro'))
        self.recalls.append(recall_score(y_validate, predictions, average='macro'))
        self.f1_scores.append(f1_score(y_validate, predictions, average='macro'))
        self.accuracies.append(accuracy_score(y_validate, predictions))

    def run(self):
        self._train_model()
        self._pseudo_label(self._unlabelled['Review'].to_numpy())

        for i in range(MAX_ROUNDS):
            print(f'SELF-TRAINING ROUND {i + 1}/{MAX_ROUNDS}')
            self._self_train()
            self._train_model()

            if len(self._pseudo_labelled) < 1000:
                break

            self._pseudo_label(self._pseudo_labelled['Review'].to_numpy())


class DnnSelfTrainer(SelfTrainer):
    def _build_model(self):
        return build_dnn_model(MAX_FEATURES)

    def _pre_process_texts(self, texts):
        sequences = self._tokenizer.texts_to_sequences(texts)
        return self._tokenizer.sequences_to_matrix(sequences, mode='count')


class CnnSelfTrainer(SelfTrainer):
    def _build_model(self):
        return build_cnn_model(MAX_FEATURES, MAX_LEN)

    def _pre_process_texts(self, texts):
        sequences = self._tokenizer.texts_to_sequences(texts)
        return pad_sequences(sequences, padding='post', truncating='post', maxlen=MAX_LEN)
