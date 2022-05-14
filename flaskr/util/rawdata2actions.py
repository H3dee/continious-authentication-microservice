import os
import csv

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


def print_csv_header_action(feature_file):
    print("printCsvHeaderAction")
    feature_file.write("type_of_action,traveled_distance_pixel,elapsed_time,direction_of_movement,")
    feature_file.write("straightness,num_points,sum_of_angles,mean_curv,sd_curv,max_curv,min_curv,mean_omega,"
                       "sd_omega,max_omega,min_omega,")
    feature_file.write("largest_deviation,dist_end_to_end_line,num_critical_points,")
    feature_file.write("mean_vx,sd_vx,max_vx,min_vx,mean_vy,sd_vy,max_vy,min_vy,mean_v,sd_v,max_v,min_v,mean_a,sd_a,"
                       "max_a,min_a,mean_jerk,sd_jerk,max_jerk,min_jerk,a_beg_time,class,n_from,n_to")

    feature_file.write("\n")
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

    # HEADER
    if st.SESSION_CUT == 2:
        print_csv_header_action(feature_file)

    counter = 0

    for fdir in os.listdir(directory):
        dirname = os.fsdecode(fdir)
        print('User: ' + dirname)

        userdirectory = st.BASE_FOLDER + st.TRAINING_FOLDER + '/' + dirname
        userid = dirname[4:len(dirname)]

        for file in os.listdir(userdirectory):
            fname = os.fsdecode(file)
            filename = userdirectory + '/' + os.fsdecode(file)
            counter += 1

            print('File: ' + fname)

            # split session into actions
            action_file = open(st.ACTION_FILENAME, "w")
            action_file.write(st.ACTION_CSV_HEADER)

            process_session1(filename, action_file)

            action_file.close()
            # end split

            if st.SESSION_CUT == 2:
                print_session2(userid, feature_file)

    feature_file.close()
    print("Num session files: " + str(counter))

    print("SESSION_CUT: " + str(st.SESSION_CUT))
    if st.SESSION_CUT == 1:
        print("NUM_ACTIONS: "+str(st.NUM_ACTIONS))
    return
