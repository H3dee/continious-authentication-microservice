GLOBAL_DEBUG = False

INTERPOLATION_TYPE = 'NO'
FREQUENCY = 0.05

SESSION_CUT = 2
EVAL_TEST_UNIT = 0
NUM_EVAL_ACTIONS = 30

# For input
BASE_FOLDER = 'C:/Users/danya/Downloads/'
TRAINING_FOLDER = 'training_files'
TEST_FOLDER = 'test_files'

# For output
PUBLIC_LABELS = 'public_labels.csv'
TRAINING_FEATURE_FILENAME = 'flaskr/util/output/training_features.csv'
ACTION_FILENAME = 'flaskr/util/output/balabit_actions.csv'

GLOBAL_DELTA_TIME = 10
GLOBAL_MIN_ACTION_LENGTH = 4
CURV_THRESHOLD = 0.0005

MM = 1
PC = 3
DD = 4

ACTION_CSV_HEADER = "type_of_action,traveled_distance_pixel,elapsed_time,direction_of_movement,straightness," \
                    "num_points,sum_of_angles,mean_curv,sd_curv,max_curv,min_curv," \
                    "mean_omega,sd_omega,max_omega,min_omega,largest_deviation,dist_end_to_end_line," \
                    "num_critical_points," + \
                    "mean_vx,sd_vx,max_vx,min_vx,mean_vy,sd_vy,max_vy,min_vy,mean_v,sd_v,max_v,min_v,mean_a,sd_a," \
                    "max_a,min_a,mean_jerk,sd_jerk,max_jerk,min_jerk,a_beg_time,n_from,n_to" + \
                    "\n"


X_LIMIT = 4000
Y_LIMIT = 4000
