import sys
import itertools
import random
import simplechains.tex.tex_fuzzer as tex_fuzzer
from stateless.status import *
from stateless.exceptions import *
from tokens import pick
import stateless.config as CONFIG

ALLOWED_BYTES = [i for i in CONFIG.ALL_BYTES if i not in CONFIG.DISALLOWED_BYTES]

MYSET_OF_BYTES = []
PREF_OF_BYTES = []

for k in ALLOWED_BYTES:
	MYSET_OF_BYTES.append(bytes([k]))
for k in CONFIG.PREF_BYTES:
	PREF_OF_BYTES.append(bytes([k]))

SEEN_AT = []

def init_set_of_bytes(s_bytes):
    global SET_OF_BYTES
    SET_OF_BYTES = s_bytes

def logit(v):
    if CONFIG.LOG:
        print(v, file=sys.stderr)

def new_byte(choices):
    open_brak = False
    x = random.randrange(7)
    if x == 0:
        token, open_brak = pick()
        v = b''
        v = v + token
    elif x>4:
        v = random.choice(PREF_OF_BYTES)
    else:
        v = random.choice(choices)
    return v, open_brak

def backtrack(prev_bytes, all_choices, limit=0):
    global SEEN_AT
    if not prev_bytes:
        raise BacktrackLimitException('Cant backtrack beyond zero index')
    if limit == -1:
        raise BacktrackLimitException('Cant backtrack beyond last valid inputs')
    # backtrack one byte
    seen = SEEN_AT[len(prev_bytes)-1]
    SEEN_AT = SEEN_AT[:-1]
    last_byte = prev_bytes[-1]
    logit('backtracking %d %s' % (len(prev_bytes), last_byte))
    #assert (last_byte,) in seen
    prev_bytes = prev_bytes[:-1]
    choices = [i for i in all_choices if i not in seen]
    if not choices:
        return backtrack(prev_bytes, all_choices, limit - 1)
    return seen, prev_bytes, choices

def till_n_length_choices(my_choices, rs):
    return my_choices # disable fudging
    all_choices = []
    for r in range(1, rs+1):
        v = [bytes(b''.join(i)) for i in itertools.product(my_choices, repeat=r)]
        #random.shuffle(v)
        all_choices.extend(v)
    return all_choices


def generate(validator, prev_bytes=None, limit=0):
    global SEEN_AT
    all_choices = MYSET_OF_BYTES
    prev_bytes=None
    if prev_bytes is None: prev_bytes = b''
    min_input_len = random.choice(CONFIG.MIN_INPUT_LEN)
	# The trace list works like a stack.
	# The goal is to keep track of open curley braces and open dollar signs in the tex input
    trace = []
    prev_trace = []
    seen = set()
    iter_limit = CONFIG.ITERATION_LIMIT
    while iter_limit:
        if len(prev_bytes) > CONFIG.MAX_INPUT_LEN:
            raise InputLimitException('Exhausted %d bytes' % CONFIG.MAX_INPUT_LEN)
        iter_limit -= 1
        choices = [i for i in all_choices if i not in seen]
        if not choices:
            seen, prev_bytes, choices = backtrack(prev_bytes, all_choices, limit=-1) # disable

        byte, open_brak = new_byte(choices)
        cur_bytes = prev_bytes + byte

        trace = prev_trace.copy()
        if byte == b'{' or open_brak == True:    # Dealing with { byte
            trace.append('}')

        elif byte == b'}' and '}' in trace:
            if trace[-1] == '}':
                trace.pop(-1)
            else:
                continue

        elif byte == b'$' and 'a$' not in trace: # Dealing with $ byte
            trace.append('a$')
        elif byte == b'$' and 'a$' in trace:
            if trace[-1] == 'a$':
                trace.pop(-1)
            else:
                continue


        cur_input = str(cur_bytes)[2:-1]
        rv, n, x = tex_fuzzer.validate_tex(cur_input, min_input_len, trace)
        if rv == Status.Complete:
            prev_trace = trace.copy()
            SEEN_AT.append(seen)
            return cur_bytes
        elif rv == Status.Incomplete:
            prev_trace = trace.copy()

            seen.add(byte)  # dont explore this byte again
            prev_bytes = cur_bytes
            SEEN_AT.append(seen)
            seen = set()

            # reset this if it was modified by incorrect
            all_choices = MYSET_OF_BYTES
        elif rv == Status.Incorrect:
            if n is None or n == -1:
                seen.add(byte)
                continue
            else:
                if n > 0:
                    #raise Exception('Backtrack disabled..')
                    logit("%s %s" % (len(choices), len(seen)))
                    if n < len(SEEN_AT):
                        seen = SEEN_AT[n]
                        SEEN_AT = SEEN_AT[:n]

                    seen.add(byte)
                    rs = len(cur_bytes) - n
                    all_choices = till_n_length_choices(MYSET_OF_BYTES, min(rs, 2))
                    prev_bytes = prev_bytes[:n]
                else:
                    pass
                    # likely a core dump
        else:
            print(str(rv))
            print(str(Status.Incorrect))
            raise Exception(rv)
    raise IterationLimitException('Exhausted %d loops' % CONFIG.ITERATION_LIMIT)
