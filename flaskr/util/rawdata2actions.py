import os
import csv

from flaskr.util import csv_helpers as helpers
from flaskr.util import settings as st
from flaskr.util import actions


def process_session1(filename, action_file):
    counter = 1
    prevrow = None
    n_from = 2
    n_to = 2

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = []

        for row in reader:
            counter = counter + 1

            if prevrow != None and prevrow == row:
                continue

            item = {
                "x": row['positionX'],
                "y": row['positionY'],
                "t": row['timestamp'],
                "button": row['button'],
                "state": row['event']
            }

            if row["button"] == 'Scroll':
                if prevrow != None:
                    item['x'] = prevrow['x']
                    item['y'] = prevrow['y']

            if row['button'] == 'Left' and row['event'] == 'Released':
                data.append(item)

                if len(data) <= 2:
                    data = []
                    n_from = counter
                    continue

                if prevrow != None and prevrow['event'] == 'Drag':
                    n_to = counter
                    actions.process_drag_actions(data, action_file, n_from, n_to)

                if prevrow != None and prevrow['event'] == 'Pressed':
                    n_to = counter
                    actions.process_point_click_actions(data, action_file, n_from, n_to)

                data = []
                n_from = n_to + 1

            else:
                if int(item['x']) < st.X_LIMIT or int(item['y']) < st.Y_LIMIT:
                    data.append(item)
            prevrow = row

        n_to = counter
        actions.process_point_click_actions(data, action_file, n_from, n_to)
        return


def print_session2(userid, feature_file):
    action_file = open(st.ACTION_FILENAME, "r")
    reader = csv.DictReader(action_file)

    for row in reader:
        feature_file.write(row["type_of_action"])
        feature_file.write(",")
        feature_file.write(row["traveled_distance_pixel"])
        feature_file.write(",")
        feature_file.write(row["elapsed_time"])
        feature_file.write(",")
        feature_file.write(row["direction_of_movement"])
        feature_file.write(",")
        feature_file.write(row["straightness"])
        feature_file.write(",")
        feature_file.write(row["num_points"])
        feature_file.write(",")
        feature_file.write(row["sum_of_angles"])
        feature_file.write(",")

        feature_file.write(row["mean_curv"])
        feature_file.write(",")
        feature_file.write(row["sd_curv"])
        feature_file.write(",")
        feature_file.write(row["max_curv"])
        feature_file.write(",")
        feature_file.write(row["min_curv"])
        feature_file.write(",")

        feature_file.write(row["mean_omega"])
        feature_file.write(",")
        feature_file.write(row["sd_omega"])
        feature_file.write(",")
        feature_file.write(row["max_omega"])
        feature_file.write(",")
        feature_file.write(row["min_omega"])
        feature_file.write(",")

        feature_file.write(row["largest_deviation"])
        feature_file.write(",")
        feature_file.write(row["dist_end_to_end_line"])
        feature_file.write(",")
        feature_file.write(row["num_critical_points"])
        feature_file.write(",")

        feature_file.write(row["mean_vx"])
        feature_file.write(",")
        feature_file.write(row["sd_vx"])
        feature_file.write(",")
        feature_file.write(row["max_vx"])
        feature_file.write(",")
        feature_file.write(row["min_vx"])
        feature_file.write(",")

        feature_file.write(row["mean_vy"])
        feature_file.write(",")
        feature_file.write(row["sd_vy"])
        feature_file.write(",")
        feature_file.write(row["max_vy"])
        feature_file.write(",")
        feature_file.write(row["min_vy"])
        feature_file.write(",")

        feature_file.write(row["mean_v"])
        feature_file.write(",")
        feature_file.write(row["sd_v"])
        feature_file.write(",")
        feature_file.write(row["max_v"])
        feature_file.write(",")
        feature_file.write(row["min_v"])
        feature_file.write(",")

        feature_file.write(row["mean_a"])
        feature_file.write(",")
        feature_file.write(row["sd_a"])
        feature_file.write(",")
        feature_file.write(row["max_a"])
        feature_file.write(",")
        feature_file.write(row["min_a"])
        feature_file.write(",")

        feature_file.write(row["mean_jerk"])
        feature_file.write(",")
        feature_file.write(row["sd_jerk"])
        feature_file.write(",")
        feature_file.write(row["max_jerk"])
        feature_file.write(",")
        feature_file.write(row["min_jerk"])
        feature_file.write(",")

        feature_file.write(row["a_beg_time"])
        feature_file.write(",")

        feature_file.write(userid + ",")
        feature_file.write(row["n_from"])
        feature_file.write(",")
        feature_file.write(row["n_to"])

        feature_file.write("\n")

    action_file.close()
    return


def process_files():
    feature_filename = st.TRAINING_FEATURE_FILENAME

    feature_file = open(feature_filename, "w")

    directory = os.fsencode(st.BASE_FOLDER + st.TRAINING_FOLDER)

    if st.SESSION_CUT == 2:
        helpers.print_csv_header_action(feature_file)

    for fdir in os.listdir(directory):
        dir_name = os.fsdecode(fdir)
        print('User: ' + dir_name)

        user_directory = st.BASE_FOLDER + st.TRAINING_FOLDER + '/' + dir_name
        userid = dir_name[4:len(dir_name)]

        for file in os.listdir(user_directory):
            file_name = os.fsdecode(file)
            file_path = user_directory + '/' + os.fsdecode(file)

            print('File: ' + file_name)

            # compute features
            action_file = open(st.ACTION_FILENAME, "w")
            action_file.write(st.ACTION_CSV_HEADER)

            process_session1(file_path, action_file)

            action_file.close()

            if st.SESSION_CUT == 2:
                # add classes to rows
                print_session2(userid, feature_file)

    feature_file.close()
    print("SESSION_CUT: " + str(st.SESSION_CUT))

    return
