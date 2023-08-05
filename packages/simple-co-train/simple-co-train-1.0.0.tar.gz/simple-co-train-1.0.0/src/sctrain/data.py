import pandas as pd
import glob
import os
from sklearn.model_selection import train_test_split


def _load_tsv_data(base_path: str) -> pd.DataFrame:
    all_file_paths = glob.glob(os.path.join(base_path, "*.tsv"))
    df = pd.concat((pd.read_csv(f, sep="\t") for f in all_file_paths), axis=0, ignore_index=True)
    if 'Score' in df:
        df.pop('Score')
    return df


def _load_from_path(path='data', unlabelled_size=0.9, train_size=0.8, y_name='label', mapping=None):
    data = _load_tsv_data(path)

    if mapping is not None:
        data[y_name] = data[y_name].map(mapping)

    _unlabelled, data = train_test_split(data, train_size=unlabelled_size)
    _labelled, _validation = train_test_split(data, train_size=train_size)
    return _labelled, _validation, _unlabelled


def _load_from_csv(name='data.csv', unlabelled_size=0.9, train_size=0.8, y_name='label', mapping=None):
    # 50000
    data = pd.read_csv(name)

    if mapping is not None:
        data[y_name] = data[y_name].map(mapping)

    _unlabelled, data = train_test_split(data, train_size=unlabelled_size)
    _labelled, _validation = train_test_split(data, train_size=train_size)
    return _labelled, _validation, _unlabelled
