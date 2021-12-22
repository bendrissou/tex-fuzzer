
MIN_INPUT_LEN = [40, 700]

MAX_INPUT_LEN = 10000

ITERATION_LIMIT = (256*256 + 10000)

ALL_BYTES = [i for i in range(30, 128)]
PREF_BYTES = [32, 36, 125] # ' ', '$' and '}'
DISALLOWED_BYTES = [37, 39, 92] # '%' and "'" "\\"

LOG = False

TIME_TO_RUN = 3600 # 86400 s --> 24 h
