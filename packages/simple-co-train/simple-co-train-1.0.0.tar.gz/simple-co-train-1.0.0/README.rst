========
Overview
========

A simple co-training library built with Keras.

* Free software: MIT license

Installation
============

Before installing simple-co-train, please install one of Keras' backend engines: TensorFlow, Theano, or CNTK.

::

    pip install simple-co-train

Documentation
=============


Basic usage:

.. code-block:: python

    from sctrain import CoTrainer, SelectionStrategy
    from sctrain.results import print_results

    trainer = CoTrainer(
        data_path='imdb.csv',  # this can be a directory, e.g. 'data'
        x_name='review',  # optional, defaults to 'text'
        y_name='sentiment',  # optional, defaults to 'label'
        unlabelled_size=0.9, # optional, what portion of total data should be used as unlabelled
        train_size=0.8, # optional, what portion of labelled data should be used as training data
        mapping={'negative': 0, 'positive': 1}  # optional mapping, y column must be 0 or 1
        selection = SelectionStrategy.UNSURE_ONLY # optional, can be CONFIDENT_ONLY or BOTH
    )
    # run the co-training, this may take a while...
    trainer.run()
    # print out accuracy, f1 score, precision, recall, and labelled samples at each co-training round
    print_results(trainer)

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
