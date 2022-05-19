import os
import csv

from flaskr.util import csv_helpers as helpers
from flaskr.util import settings as st
from flaskr.util import actions


def compute_features(filename, action_file):
    counter = 1
    prev_row = None
    n_from = 2
    n_to = 2

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = []

        for row in reader:
            counter = counter + 1

            if prev_row != None and prev_row == row:
                continue

            item = {
                "x": row['positionX'],
                "y": row['positionY'],
                "t": row['timestamp'],
                "button": row['button'],
                "state": row['event']
            }

            if row["button"] == 'Scroll':
                if prev_row != None:
                    item['x'] = prev_row['x']
                    item['y'] = prev_row['y']

            if (row['button'] == 'Left' or row['button'] == 'Right') and row['event'] == 'Released':
                data.append(item)

                if len(data) <= 2:
                    data = []
                    n_from = counter
                    continue

                if prev_row != None and prev_row['event'] == 'Drag':
                    n_to = counter
                    actions.process_drag_actions(data, action_file, n_from, n_to)

                if prev_row != None and prev_row['event'] == 'Pressed':
                    n_to = counter
                    actions.process_point_click_actions(data, action_file, n_from, n_to)

                data = []
                n_from = n_to + 1

            else:
                if int(item['x']) < st.X_LIMIT or int(item['y']) < st.Y_LIMIT:
                    data.append(item)
            prev_row = row

        n_to = counter
        actions.process_point_click_actions(data, action_file, n_from, n_to)
        return


def add_class_to_features(userid, target_features_file_path, features_by_action_file_path):
    action_file = open(features_by_action_file_path, "r")
    reader = csv.DictReader(action_file)

    for row in reader:
        target_features_file_path.write(row["type_of_action"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["traveled_distance_pixel"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["elapsed_time"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["direction_of_movement"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["straightness"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["num_points"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sum_of_angles"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_curv"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_curv"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_curv"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_curv"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_omega"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_omega"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_omega"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_omega"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["largest_deviation"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["dist_end_to_end_line"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["num_critical_points"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_vx"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_vx"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_vx"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_vx"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_vy"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_vy"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_vy"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_vy"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_v"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_v"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_v"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_v"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_a"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_a"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_a"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_a"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["mean_jerk"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["sd_jerk"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["max_jerk"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["min_jerk"])
        target_features_file_path.write(",")

        target_features_file_path.write(row["a_beg_time"])
        target_features_file_path.write(",")

        target_features_file_path.write(userid + ",")
        target_features_file_path.write(row["n_from"])
        target_features_file_path.write(",")
        target_features_file_path.write(row["n_to"])

        target_features_file_path.write("\n")

    action_file.close()
    return


def process_files(user_folder_path=None):
    if user_folder_path is None:
        feature_filename = st.TRAINING_FEATURE_FILENAME
        directory = os.fsencode(st.BASE_FOLDER + st.TRAINING_FOLDER)
    else:
        feature_filename = st.TEST_DATA_FOLDER + '/' + user_folder_path + '/features_with_classes.csv'
        directory = st.BASE_FOLDER + st.TEST_FOLDER + '/' + user_folder_path

    feature_file = open(feature_filename, "w")

    if st.SESSION_CUT == 2:
        helpers.print_csv_header_action(feature_file)

    if user_folder_path is not None:
        raw_data_file_path = directory + '/' + 'raw_events_data.csv'
        user_id = user_folder_path[5:len(user_folder_path)]

        features_without_class_file_path = directory + '/features.csv'
        features_without_class_file = open(features_without_class_file_path, "w")
        features_without_class_file.write(st.ACTION_CSV_HEADER)

        compute_features(raw_data_file_path, features_without_class_file)

        features_without_class_file.close()

        add_class_to_features(user_id, feature_file, features_without_class_file_path)
    else:
        for fdir in os.listdir(directory):
            dir_name = os.fsdecode(fdir)
            print('User: ' + dir_name)

            user_directory = st.BASE_FOLDER + st.TRAINING_FOLDER + '/' + dir_name
            user_id = dir_name[4:len(dir_name)]

            for file in os.listdir(user_directory):
                file_name = os.fsdecode(file)
                raw_data_file_path = user_directory + '/' + file_name

                print('File: ' + file_name)

                # compute features
                features_without_class_file = open(st.ACTION_FILENAME, "w")
                features_without_class_file.write(st.ACTION_CSV_HEADER)

                compute_features(raw_data_file_path, features_without_class_file)

                features_without_class_file.close()

                if st.SESSION_CUT == 2:
                    # add classes to rows
                    add_class_to_features(user_id, feature_file, st.ACTION_FILENAME)

    feature_file.close()
    print("SESSION_CUT: " + str(st.SESSION_CUT))

    return
