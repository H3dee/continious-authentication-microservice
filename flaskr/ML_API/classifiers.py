import pickle
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


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
        print(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def tune_params(self, x, y):
        n_estimators = [int(x) for x in np.linspace(start=10, stop=80, num=10)]
        max_features = ['auto', 'sqrt']
        max_depth = [2, 4]
        min_samples_split = [2, 5]
        min_samples_leaf = [1, 2]
        bootstrap = [True, False]
        param_grid = dict(n_estimators=n_estimators, max_features=max_features, max_depth=max_depth,
                          min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, bootstrap=bootstrap)

        rf_grid = GridSearchCV(estimator=RandomForestClassifier(), scoring='f1', param_grid=param_grid, cv=5, verbose=2, n_jobs=6)
        rf_grid.fit(x, y)

        print(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

    user_id = int


class KNN:
    def train(self, x, y, params):
        clf = KNeighborsClassifier(**params)
        clf = clf.fit(x, y)
        with open(f'ml_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def predict(self, x, y):
        with open(f'ml_state_userId_{self.user_id}.pkl', 'rb') as f:
            clf = pickle.load(f)
        predicted = clf.predict(x)
        accuracy = round(f1_score(y, predicted, average='macro'), 3) * 100
        print(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def tune_params(self, x, y):
        k_range = range(1, 31, 2)
        param_grid = dict(n_neighbors=k_range)

        rf_grid = GridSearchCV(estimator=KNeighborsClassifier(), scoring='f1', param_grid=param_grid, cv=10, verbose=1,
                               n_jobs=4)
        rf_grid = rf_grid.fit(x, y)

        print(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

    user_id = int


class DT:
    def train(self, x, y, params):
        clf = tree.DecisionTreeClassifier(**params)
        clf = clf.fit(x, y)
        with open(f'ml_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def predict(self, x, y):
        with open(f'ml_state_userId_{self.user_id}.pkl', 'rb') as f:
            clf = pickle.load(f)
        predicted = clf.predict(x)
        accuracy = round(f1_score(y, predicted, average='macro'), 3) * 100
        print(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def tune_params(self, x, y):
        criterion = ['gini', 'entropy']
        max_depth = [4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 30, 40, 50, 70, 90, 120, 150]
        param_grid = dict(criterion=criterion, max_depth=max_depth)

        rf_grid = GridSearchCV(estimator=tree.DecisionTreeClassifier(), param_grid=param_grid, cv=10, verbose=1,
                               n_jobs=4)
        rf_grid = rf_grid.fit(x, y)

        print(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

    user_id = int


class SVM:
    def train(self, x, y, params):
        clf = SVC(**params)
        clf = clf.fit(x, y)
        with open(f'ml_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def predict(self, x, y):
        with open(f'ml_state_userId_{self.user_id}.pkl', 'rb') as f:
            clf = pickle.load(f)
        predicted = clf.predict(x)
        accuracy = round(f1_score(y, predicted, average='macro'), 3) * 100
        print(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def tune_params(self, x, y):
        C = [0.1, 1, 10, 100, 1000]
        gamma = [1, 0.1, 0.01, 0.001, 0.0001]
        kernel = ['rbf']
        param_grid = dict(C=C, gamma=gamma, kernel=kernel)

        rf_grid = GridSearchCV(estimator=SVC(), param_grid=param_grid, scoring='f1', cv=4, verbose=2, n_jobs=4)
        rf_grid = rf_grid.fit(x, y)

        print(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

    user_id = int


class LR:
    def train(self, x, y, params):
        clf = LogisticRegression(**params)
        clf = clf.fit(x, y)
        with open(f'ml_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def predict(self, x, y):
        with open(f'ml_state_userId_{self.user_id}.pkl', 'rb') as f:
            clf = pickle.load(f)
        predicted = clf.predict(x)
        accuracy = round(f1_score(y, predicted, average='macro'), 3) * 100
        print(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def tune_params(self, x, y):
        solver = ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
        penalty = ['l1', 'l2']
        C = [0.001, 0.01, 0.1, 1, 10, 100]
        param_grid = dict(solver=solver, penalty=penalty, C=C)

        rf_grid = GridSearchCV(estimator=LogisticRegression(max_iter=500), param_grid=param_grid, scoring='f1', cv=5, verbose=2, n_jobs=4)
        rf_grid = rf_grid.fit(x, y)

        print(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

    user_id = int


class NB:
    def train(self, x, y, params):
        clf = GaussianNB(**params)
        clf = clf.fit(x, y)
        with open(f'ml_state_userId_{self.user_id}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def predict(self, x, y):
        with open(f'ml_state_userId_{self.user_id}.pkl', 'rb') as f:
            clf = pickle.load(f)
        predicted = clf.predict(x)
        accuracy = round(f1_score(y, predicted, average='macro'), 3) * 100
        print(f'F1-Score: {accuracy}%')
        if accuracy >= 70:
            return True
        return False

    def tune_params(self, x, y):
        var_smoothing = np.logspace(0, -9, num=100)
        param_grid = dict(var_smoothing=var_smoothing)

        rf_grid = GridSearchCV(estimator=GaussianNB(), param_grid=param_grid, scoring='f1', cv=10, verbose=2, n_jobs=4)
        rf_grid = rf_grid.fit(x, y)

        print(f"Scored best params for user {self.user_id}: {rf_grid.best_params_}")
        params = rf_grid.best_params_

        return params

    def __init__(self, user_id):
        self.user_id = user_id

    user_id = int
