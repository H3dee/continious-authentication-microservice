import pandas as pd
import classifiers


def train_all(data):
    """Trains all users available in the train dataframe.

    Creates unique params files for all users in need of further predictions

    Parameters
    ----------
    data
        The train dataframe containing data for users in the system
    """

    df = pd.read_csv(data)
    users_ids = pd.unique(df['class'])
    for user_id in users_ids:
        rf = classifiers.RF(user_id)
        train_df = rf.prepare_dataset(df)
        x, y = rf.split_and_normalize_dataset(train_df)
        params = rf.tune_params(x, y)
        rf.train(x, y, params)


def validate_user(data, user_id):
    """Validates user mouse output data.

    Prediction limit is 70%. If prediction accuracy is lower than that limit method will return FALSE,
    otherwise TRUE

    Parameters
    ----------
    data
        The test dataframe containing data for current user
    user_id
        The user id
    """

    rf = classifiers.RF(user_id)
    df = pd.read_csv(data)
    test_df = rf.prepare_test_dataset(df)
    x, y = rf.split_and_normalize_test_dataset(test_df)
    is_valid = rf.predict(x, y)

    return is_valid
