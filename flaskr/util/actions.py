import numpy as np
import math

from flaskr.util import general_statistics as gs
from flaskr.util import settings as st
from flaskr.util import time_sample_interpolation as ts


def compute_action_features(x, y, t, action_code, action_file, n_from, n_to):
    n = len(x)
    if st.GLOBAL_DEBUG:
        print("\t\t" + str(n_from) + '-' + str(n_to) + " len: " + str(n))

    if n < st.GLOBAL_MIN_ACTION_LENGTH:
        return None
    x = [int(e) for e in x]
    y = [int(e) for e in y]
    t = [float(e) for e in t]

    if gs.containsNull(x):
        return None

    for i in range(1, n):
        if x[i] > st.X_LIMIT or y[i] > st.Y_LIMIT:
            x[i] = x[i - 1]
            y[i] = y[i - 1]

    if st.INTERPOLATION_TYPE != 'NO':
        result = None
        if st.INTERPOLATION_TYPE == 'LINEAR':
            xyt_line_array = np.column_stack((np.array(x), np.array(y), np.array(t)))
            result = ts.time_sample_interpolation_linear(xyt_line_array, st.FREQUENCY)
        if st.INTERPOLATION_TYPE == 'POLINOMIAL':
            xyt_line_array = np.column_stack((np.array(x), np.array(y), np.array(t)))
            result = ts.time_sample_interpolation_polinomial(xyt_line_array, st.FREQUENCY)
        if st.INTERPOLATION_TYPE == 'SPLINE':
            xyt_line_array = np.column_stack((np.array(x), np.array(y), np.array(t)))
            result = ts.time_sample_interpolation_spline(xyt_line_array, st.FREQUENCY)
        if result != None:
            x = result[:, 0]
            y = result[:, 1]
            t = result[:, 2]
            n = len(x)
        else:
            print('Interpolation error. No interpolation.')
            print('\t' + str(n_from) + '-' + str(n_to) + " len: " + str(n))
    # trajectory from the beginning point of the action
    # angles
    trajectory = 0
    sum_of_angles = 0
    angles = [0]
    path = [0]
    # velocities
    vx = [0]
    vy = [0]
    v = [0]
    for i in range(1, n):
        dx = int(x[i]) - int(x[i - 1])
        dy = int(y[i]) - int(y[i - 1])
        dt = float(t[i]) - float(t[i - 1])
        if dt == 0:
            dt = 0.01
        vx_val = dx / dt
        vy_val = dy / dt
        vx.append(vx_val)
        vy.append(vy_val)
        v.append(math.sqrt(vx_val * vx_val + vy_val * vy_val))
        angle = math.atan2(dy, dx)
        angles.append(angle)
        sum_of_angles += angle
        distance = math.sqrt(dx * dx + dy * dy)
        trajectory = trajectory + distance
        path.append(trajectory)

    mean_vx = gs.mean(vx, 0, len(vx))
    sd_vx = gs.stdev(vx, 0, len(vx))
    max_vx = gs.max(vx, 0, len(vx))
    min_vx = gs.min_not_null(vx, 0, len(vx))

    mean_vy = gs.mean(vy, 0, len(vy))
    sd_vy = gs.stdev(vy, 0, len(vy))
    max_vy = gs.max(vy, 0, len(vy))
    min_vy = gs.min_not_null(vy, 0, len(vy))

    mean_v = gs.mean(v, 0, len(v))
    sd_v = gs.stdev(v, 0, len(v))
    max_v = gs.max(v, 0, len(v))
    min_v = gs.min_not_null(v, 0, len(v))

    # angular velocity
    omega = [0]
    no = len(angles)
    for i in range(1, no):
        dtheta = angles[i] - angles[i - 1]
        dt = float(t[i]) - float(t[i - 1])
        if dt == 0:
            dt = 0.01
        omega.append(dtheta / dt)

    mean_omega = gs.mean(omega, 0, len(omega))
    sd_omega = gs.stdev(omega, 0, len(omega))
    max_omega = gs.max(omega, 0, len(omega))
    min_omega = gs.min_not_null(omega, 0, len(omega))

    # acceleration
    a = [0]
    acc_time_at_beginning = 0
    cont = True
    for i in range(1, n - 1):
        dv = v[i] - v[i - 1]
        dt = float(t[i]) - float(t[i - 1])
        if dt == 0:
            dt = 0.01
        if cont and dv > 0:
            acc_time_at_beginning += dt
        else:
            cont = False
        a.append(dv / dt)
    mean_a = gs.mean(a, 0, len(a))
    sd_a = gs.stdev(a, 0, len(a))
    max_a = gs.max(a, 0, len(a))
    min_a = gs.min_not_null(a, 0, len(a))

    # jerk
    j = [0]
    na = len(a)
    for i in range(1, na):
        da = a[i] - a[i - 1]
        dt = float(t[i]) - float(t[i - 1])
        if dt == 0:
            dt = 0.01
        j.append(da / dt)
    mean_jerk = gs.mean(j, 0, len(j))
    sd_jerk = gs.stdev(j, 0, len(j))
    max_jerk = gs.max(j, 0, len(j))
    min_jerk = gs.min_not_null(j, 0, len(j))

    # curvature: defined by Gamboa&Fred, 2004
    # num_critical_points
    c = []
    num_critical_points = 0
    nn = len(path)
    for i in range(1, nn):
        dp = path[i] - path[i - 1]
        if dp == 0:
            continue
        dangle = angles[i] - angles[i - 1]
        curv = dangle / dp
        c.append(curv)
        if abs(curv) < st.CURV_THRESHOLD:
            num_critical_points = num_critical_points + 1
    mean_curv = gs.mean(c, 0, len(c))
    sd_curv = gs.stdev(c, 0, len(c))
    max_curv = gs.max(c, 0, len(c))
    min_curv = gs.min_not_null(c, 0, len(c))

    # time
    time = float(t[n - 1]) - float(t[0])

    # direction: -pi..pi
    theta = math.atan2(int(y[n - 1]) - int(y[0]), int(x[n - 1]) - int(x[0]))
    direction = compute_direction(theta)

    # distEndtToEndLine
    dist_end_to_end_line = math.sqrt(
        (int(x[0]) - int(x[n - 1])) * (int(x[0]) - int(x[n - 1])) + (int(y[0]) - int(y[n - 1])) * (
                int(y[0]) - int(y[n - 1])))

    # straightness
    if trajectory == 0:
        straightness = 0
    else:
        straightness = dist_end_to_end_line / trajectory
    if straightness > 1:
        straightness = 1

    # largest deviation
    largest_deviation = compute_largest_deviation(x, y)

    result = str(action_code) + ',' + str(trajectory) + ',' + str(time) + ',' + str(direction) + ',' + \
             str(straightness) + ',' + str(n) + ',' + str(sum_of_angles) + ',' + \
             str(mean_curv) + "," + str(sd_curv) + "," + str(max_curv) + "," + str(min_curv) + "," + \
             str(mean_omega) + "," + str(sd_omega) + "," + str(max_omega) + "," + str(min_omega) + "," + \
             str(largest_deviation) + "," + \
             str(dist_end_to_end_line) + "," + str(num_critical_points) + "," + \
             str(mean_vx) + "," + str(sd_vx) + "," + str(max_vx) + "," + str(min_vx) + "," + \
             str(mean_vy) + "," + str(sd_vy) + "," + str(max_vy) + "," + str(min_vy) + "," + \
             str(mean_v) + "," + str(sd_v) + "," + str(max_v) + "," + str(min_v) + "," + \
             str(mean_a) + "," + str(sd_a) + "," + str(max_a) + "," + str(min_a) + "," + \
             str(mean_jerk) + "," + str(sd_jerk) + "," + str(max_jerk) + "," + str(min_jerk) + "," + \
             str(acc_time_at_beginning) + "," + \
             str(n_from) + "," + str(n_to) + \
             "\n"

    return result


def print_action(x, y, t, action_code, action_file, n_from, n_to):
    result = compute_action_features(x, y, t, action_code, action_file, n_from, n_to)

    if result != None:
        action_file.write(result)
    return


def compute_largest_deviation(x, y):
    n = len(x)
    a = float(x[n - 1]) - float(x[0])
    b = float(y[0]) - float(y[n - 1])
    c = float(x[0]) * float(y[n - 1]) - float(x[n - 1]) * float(y[0])
    max = 0
    den = math.sqrt(a * a + b * b)
    for i in range(1, n - 1):
        #     distance x_i,y_i from line
        d = math.fabs(a * float(x[i]) + b * float(y[i]) + c)
        if d > max:
            max = d
    if den > 0:
        max /= den
    return max


def process_point_click(x, y, t, action_file, n_from, n_to):
    print_action(x, y, t, st.PC, action_file, n_from, n_to)
    return


def process_mouse_move(x, y, t, action_file, n_from, n_to):
    print_action(x, y, t, st.MM, action_file, n_from, n_to)
    return


def process_drag_action(x, y, t, action_file, n_from, n_to):
    print_action(x, y, t, st.DD, action_file, n_from, n_to)
    return


def process_point_click_actions(data, action_file, n_from, n_to):
    if st.GLOBAL_DEBUG:
        print("MM*PC:" + str(n_from) + "-" + str(n_to))
    x = []
    y = []
    t = []
    prev_time = 0
    start = n_from
    counter = 0
    for item in data:
        act_state = item['state']
        act_time = float(item['t'])
        counter += 1
        if act_state == 'Pressed':
            if len(t) > st.GLOBAL_MIN_ACTION_LENGTH:
                x.append(item['x'])
                y.append(item['y'])
                t.append(act_time)
                if st.GLOBAL_DEBUG:
                    print("\tPC:" + str(start) + "-" + str(n_to))
                process_point_click(x, y, t, action_file, start, n_to)
            return
        else:
            if act_time - prev_time > st.GLOBAL_DELTA_TIME:
                stop = n_from + counter - 2
                if len(t) > st.GLOBAL_MIN_ACTION_LENGTH:
                    if st.GLOBAL_DEBUG:
                        print("\tMM:" + str(start) + "-" + str(stop))
                    process_mouse_move(x, y, t, action_file, start, stop)
                x = []
                y = []
                t = []
                start = stop + 1
            else:
                x.append(item['x'])
                y.append(item['y'])
                t.append(act_time)
        prev_time = act_time
    return


def process_mouse_move_actions(data, action_file, n_from, n_to):
    if st.GLOBAL_DEBUG:
        print("MM*MM:" + str(n_from) + "-" + str(n_to))
    x = []
    y = []
    t = []
    start = n_from
    counter = 0
    prev_time = 0
    for item in data:
        x.append(item['x'])
        y.append(item['y'])
        counter += 1
        act_time = float(item['t'])
        t.append(act_time)
        if act_time - prev_time > st.GLOBAL_DELTA_TIME:
            stop = n_from + counter - 2
            if len(t) > st.GLOBAL_MIN_ACTION_LENGTH:

                if st.GLOBAL_DEBUG:
                    print("\tMM:" + str(start) + "-" + str(stop))
                process_mouse_move(x, y, t, action_file, start, stop)
                x = []
                y = []
                t = []
                start = stop + 1
        prev_time = act_time
    if len(t) > st.GLOBAL_MIN_ACTION_LENGTH:
        if st.GLOBAL_DEBUG:
            print("\tMM:" + str(start) + "-" + str(n_to))
        process_mouse_move(x, y, t, action_file, start, n_to)
    return


def process_drag_actions(data, action_file, n_from, n_to):
    if st.GLOBAL_DEBUG:
        print("MM*DD:" + str(n_from) + "-" + str(n_to))
    x = []
    y = []
    t = []
    start = n_from
    stop = start
    counter = 0
    prev_time = 0
    for item in data:
        act_button = item['button']
        act_state = item['state']
        act_time = float(item['t'])
        counter += 1
        if act_button == 'NoButton' and act_state == 'Move':
            if act_time - prev_time > st.GLOBAL_DELTA_TIME:
                stop = n_from + counter - 2
                if len(t) > st.GLOBAL_MIN_ACTION_LENGTH:
                    if st.GLOBAL_DEBUG:
                        print("\tMM:" + str(start) + "-" + str(stop))
                    process_mouse_move(x, y, t, action_file, start, stop)
                x = []
                y = []
                t = []
                start = stop + 1
            x.append(item['x'])
            y.append(item['y'])
            t.append(act_time)

        if act_button == 'Left' and act_state == 'Pressed':
            if len(t) > st.GLOBAL_MIN_ACTION_LENGTH:
                stop = n_from + counter - 2
                if st.GLOBAL_DEBUG:
                    print("\tMM:" + str(start) + "-" + str(stop))
                process_mouse_move(x, y, t, action_file, start, stop)
            x = []
            y = []
            t = []
            start = stop + 1
            x.append(item['x'])
            y.append(item['y'])
            t.append(act_time)
        if act_button == 'Left' and act_state == 'Released':
            x.append(item['x'])
            y.append(item['y'])
            t.append(act_time)
            if st.GLOBAL_DEBUG:
                print("\tDD:" + str(start) + "-" + str(n_to))
            process_drag_action(x, y, t, action_file, start, n_to)
        if act_button == 'NoButton' and act_state == 'Drag':
            x.append(item['x'])
            y.append(item['y'])
            t.append(act_time)
        prev_time = act_time
    return


def compute_direction(theta):
    direction = 0
    if 0 <= theta < math.pi / 4:
        direction = 0
    if math.pi / 4 <= theta < math.pi / 2:
        direction = 1
    if math.pi / 2 <= theta < 3 * math.pi / 4:
        direction = 2
    if 3 * math.pi / 4 <= theta < math.pi:
        direction = 3
    if -math.pi / 4 <= theta < 0:
        direction = 7
    if -math.pi / 2 <= theta < -math.pi / 4:
        direction = 6
    if -3 * math.pi / 4 <= theta < -math.pi / 2:
        direction = 5
    if -math.pi <= theta < -3 * math.pi / 4:
        direction = 4
    return direction
