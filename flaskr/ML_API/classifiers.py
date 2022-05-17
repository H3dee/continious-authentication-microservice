import logging
import pickle

import numpy as np
import pandas as pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle


class RF:
    def train(self, x, y, params):
        clf = RandomForestClassifier(**params)
        clf = clf.fit(x, y)
        with open(f'ml_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def predict(self, x, y):
        with open(f'ml_state_userId_{self.user_id}.pkl', 'rb') as f:
            clf = pickle.load(f)
        predicted = clf.predict(x)
        accuracy = round(f1_score(y, predicted, average='macro'), 3) * 100
        self.logger.info(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def prepare_dataset(self, dataset):
        users_count = len(pandas.unique(dataset['class']))
        self.logger.info(f'Users count: {users_count}')

        user_features_count = len(dataset[lambda x: x['class'] == self.user_id])
        self.logger.info(f'Features count for user id {self.user_id}: {user_features_count}')

        users_ids = pandas.unique(dataset['class'])
        users_ids = users_ids[users_ids != self.user_id]

        feature_count_per_user = round(user_features_count / (users_count - 1))
        self.logger.info(f'Feature number for the rest of the users: {feature_count_per_user}')
        for user_id in users_ids:
            count = len(dataset[lambda x: x['class'] == user_id])
            if count < feature_count_per_user:
                user_features_count = count
                self.logger.info(f'Total feature amount per user decreased to {count}')

        data = dataset[lambda x: x['class'] == self.user_id].head(user_features_count)

        for user_id in users_ids:
            data = pandas.concat([data, dataset[lambda x: x['class'] == user_id].head(feature_count_per_user)])
        self.logger.info('Split train data')
        data.loc[lambda x: x['class'] == self.user_id, 'class'] = 1
        data.loc[lambda x: x['class'] != 1, 'class'] = 0
        self.logger.info('Marked train data')

        return data

    def prepare_test_dataset(self, data):
        data.loc[lambda x: x['class'] == self.user_id, 'class'] = 1
        return data

    def split_and_normalize_dataset(self, dataset):
        dataset = shuffle(dataset)
        y = dataset['class']
        dataset = dataset.drop(['class', 'type_of_action'], axis=1)
        values = dataset.values

        scaler = preprocessing.StandardScaler()
        scaled_values = scaler.fit_transform(values)
        with open(f'ml_normalization_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        self.logger.info(f'Saved normalization state for user {self.user_id}')
        df_normalized = pandas.DataFrame(scaled_values)
        x = df_normalized

        self.logger.info('Split and normalized dataset')

        return x, y

    def split_and_normalize_test_dataset(self, dataset):
        y = dataset['class']
        dataset = dataset.drop(['class', 'type_of_action'], axis=1)
        values = dataset.values
        with open(f'ml_normalization_state_userId_{self.user_id}.pkl', 'rb') as f:
            scaler = pickle.load(f)
        scaled_values = scaler.transform(values)
        df_normalized = pandas.DataFrame(scaled_values)
        x = df_normalized

        return x, y

    def tune_params(self, x, y):
        n_estimators = [int(x) for x in np.linspace(start=10, stop=80, num=10)]
        max_features = ['auto', 'sqrt']
        max_depth = [2, 4]
        min_samples_split = [2, 5]
        min_samples_leaf = [1, 2]
        bootstrap = [True, False]
        param_grid = {'n_estimators': n_estimators,
                      'max_features': max_features,
                      'max_depth': max_depth,
                      'min_samples_split': min_samples_split,
                      'min_samples_leaf': min_samples_leaf,
                      'bootstrap': bootstrap}

        rf_grid = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=4, verbose=2, n_jobs=4)
        rf_grid.fit(x, y)

        self.logger.info(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

        self.logger = logging.getLogger("dev")
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    user_id = int
    logger = None
