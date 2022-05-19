import pandas as pd
import classifiers
import processing


def train_all(data):
    """Trains all users available in the train dataframe.

    Creates unique params files for all users in need of further predictions

    Parameters
    ----------
    data
        The train dataframe containing data for users in the system
    """
    try:
        df = pd.read_csv(data)
        users_ids = pd.unique(df['class'])
        for user_id in users_ids:
            rf = classifiers.RF(user_id)
            train_df = processing.prepare_dataset(df, user_id)
            x, y = processing.split_and_normalize_dataset(train_df, user_id)
            params = rf.tune_params(x, y)
            rf.train(x, y, params)
    except (ValueError, FileNotFoundError):
        print('User isn''t exist in the system')

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


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
    try:
        rf = classifiers.RF(user_id)
        df = pd.read_csv(data)
        test_df = processing.prepare_test_dataset(df, user_id)
        x, y = processing.split_and_normalize_test_dataset(test_df, user_id)
        is_valid = rf.predict(x, y)
        return is_valid
    except (ValueError, FileNotFoundError):
        print('User isn''t exist in the system')

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
