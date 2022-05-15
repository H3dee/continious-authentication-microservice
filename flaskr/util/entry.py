from flaskr.util import settings as st
from flaskr.util import rawdata2actions as rd

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def start_features_extracting(path=None):
    st.SESSION_CUT = 2
    print("Computing features")

    rd.process_files(path)

    return
