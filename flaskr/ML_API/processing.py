import pandas
import pickle
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler


def prepare_dataset(dataset, user_id):
    users_count = len(pandas.unique(dataset['class']))
    print(f'Users count: {users_count}')

    user_features_count = len(dataset[lambda x: x['class'] == user_id])
    print(f'Features count for user id {user_id}: {user_features_count}')

    users_ids = pandas.unique(dataset['class'])
    users_ids = users_ids[users_ids != user_id]

    feature_count_per_user = round(user_features_count / (users_count - 1))
    print(f'Feature number for the rest of the users: {feature_count_per_user}')

    for u_id in users_ids:
        count = len(dataset[lambda x: x['class'] == u_id])
        if count < feature_count_per_user:
            user_features_count = count
            print(f'Total feature amount per user decreased to {count}')

    data = dataset[lambda x: x['class'] == user_id].head(user_features_count)

    for u_id in users_ids:
        data = pandas.concat([data, dataset[lambda x: x['class'] == u_id].head(feature_count_per_user)])
    print('Split train data')
    data.loc[lambda x: x['class'] == user_id, 'class'] = 1
    data.loc[lambda x: x['class'] != 1, 'class'] = 0
    print('Marked train data')

    return data


def prepare_test_dataset(data, user_id):
    data.loc[lambda x: x['class'] == user_id, 'class'] = 1
    return data


def split_and_normalize_dataset(dataset, user_id):
    dataset = shuffle(dataset)
    y = dataset['class']
    dataset = dataset.drop(['class', 'type_of_action'], axis=1)
    values = dataset.values

    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(values)
    with open(f'ml_normalization_state_userId_{user_id}.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print(f'Saved normalization state for user {user_id}')
    df_normalized = pandas.DataFrame(scaled_values)
    x = df_normalized

    print('Split and normalized dataset')

    return x, y


def split_and_normalize_test_dataset(dataset, user_id):
    y = dataset['class']
    dataset = dataset.drop(['class', 'type_of_action'], axis=1)
    values = dataset.values
    with open(f'ml_normalization_state_userId_{user_id}.pkl', 'rb') as f:
        scaler = pickle.load(f)
    scaled_values = scaler.transform(values)
    df_normalized = pandas.DataFrame(scaled_values)
    x = df_normalized

    return x, y
