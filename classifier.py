"""
  Classifier.py:
  Utilizes a K-Nearest Neighbor Classifier to classify dispatches.
  Strengths:
    -- Low-dimensionality data, which means very reasonable results
    -- No need to store model & load it every time
  Weaknesses:
    -- Takes a while to predict
    -- Utilizes more storage than another predictive model
  Based on validation, we have an approximate 60% prediction rate,
  which is quite good for three parameters (latitude, longitude, time).
"""

import pandas as pd
import numpy as np
import math

from sklearn.utils import shuffle
from datetime import datetime
from collections import defaultdict, Counter

class Query():
  def __init__(self, latitude, longitude, timestamp):
    self.latitude = latitude
    self.longitude = longitude
    self.received_time_seconds = timestamp

class KNNClassifier():
  def __init__(self, datafile='./data/cleaned_data.csv', k=7, validation=False):
    """
    Initializes our classifier.
    """
    self.k = k
    self.df = pd.read_csv(datafile)
    if validation: self._validate()
    self.X, self.Y = self._extract_features(self.df)

  def _validate(self):
    """
    Trains and validates the classifier.
    """
    # Shuffle the dataset
    df_train, df_test = self.df[:9900], self.df[9900:]

    print 'Extracting features...'
    X_train, Y_train = self._extract_features(df_train)
    X_test, Y_test = self._extract_features(df_test)
    print 'Extracted features'
    print

    # Validate the dataset
    print 'Validating dataset...'
    correct = 0.
    for i, x in X_test.iterrows():
      y = self._predict(x, X=X_train, Y=Y_train)
      print y[1], Y_test[i]
      if y[1] == Y_test[i]:
        correct += 1.
    print 'Validation score: ' + str(correct/len(Y_test))
    print

    print 'Done training.'

  def _predict(self, x, X, Y):
    """
    For validation use only.
    """
    neighbors = self._find_closest_neighbors(x, X, Y)
    return self._ensemble_output(neighbors)

  def predict(self, x):
    print 'predicting...'
    return self._predict(x, self.X, self.Y)

  def _ensemble_output(self, predictions):
    """
    Takes closest neighbors, and returns the most frequent
    class. If ties, returns the closest class of the neighbors.
    """
    f = Counter()
    mode = None
    modes = []
    pos = defaultdict(float)
    for i, p in enumerate(predictions):
      f[p] += 1
      pos[p] += i
      if f[p] > f[mode]:
        modes = [p]
        mode_f = f[p]
      elif f[p] == f[mode]:
        modes.append(p)
    if len(modes) == 1:
      return modes[0]
    else:
      for m in modes:
        pos[m] = pos[m]/f[m]
      return min(modes, key=pos[m])

  def _find_closest_neighbors(self, x, X, Y):
    """
    Finds the k-th nearest neighbors of x in index.
    """
    neighbors = []
    for i, (_, x2) in enumerate(X.iterrows()):
      d = self._find_dist(x, x2)
      neighbors.append((d, Y[i]))
    neighbors.sort()
    return neighbors[:self.k]

  def _find_dist(self, x1, x2):
    """
    Evaluates the distance between two data points.
    Utilizes the circular nature of the 24-hour clock.
    Assumes that the times are already in minute form.
    """
    t1, t2 = int(x1.received_time_seconds), int(x2.received_time_seconds)
    time_diff = min(86400+t1-t2, t2-t1)
    lat_diff = float(x1.latitude) - float(x2.latitude)
    long_diff = float(x1.longitude) - float(x2.longitude)
    return math.sqrt(time_diff**2 + (lat_diff)**2 + (long_diff)**2)

  def _extract_features(self, X):
    """
    Extracts features and composes the design matrix.

    Feature 1: Time - Hours, Minutes, Seconds
    Feature 2: Latitude
    Feature 3: Longitude
    """
    return X[['received_time_seconds', 'latitude', 'longitude']], X['unit_type']