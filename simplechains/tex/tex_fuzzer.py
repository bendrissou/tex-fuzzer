#!/usr/bin/env python3

import subprocess
import os
import re
from stateless.status import *

def validate_tex(input_str, min_input_len, trace):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        # cmd stores the unix command that invokes the binary tex on the input string.
        cmd = "echo '" + input_str + "' | sudo tee test.tex > /dev/null 2>&1 && sed -i -e 's/(backslash)/\\\/g' test.tex && echo 'test.tex \\\end' | tex > test.log"
        excode = os.system(cmd)

        # file_out stores the output of the tex program.
        file_out = ''

        file = open('test.log', 'r')
        Lines = file.readlines()
        file.close()
        for line in Lines:
            file_out = file_out + ' ' + line.strip()
        nout = len(Lines)
        input_len = len(input_str)

        if excode != 0 and excode != 256:
            print("\n++++++++++++++++ Crash or Bug found! ++++++++++++++++")
            print("Exit code: " + str(excode))
            print("String: " + input_str)
            save_crash(input_str, str(excode))

        if nout == 4: # Valid input
            if input_len > min_input_len:
                if min_input_len != -1: # -1 means we are inside a recursion and we are testing if input is incomplete. Hence don't save input.
                    save_valid_input(input_str)
                return Status.Complete,-1,""
            else: return Status.Incomplete,-1,"" # Append more

        elif file_out.find("Missing $ inserted.") != -1:
            if 'a$' in trace:
                input_str = close_string(input_str, trace)
                rv, n, x = validate_tex(input_str, -1, [])
                if rv == Status.Complete:
                    return Status.Incomplete,-1,"" # Append more
                else:
                    return Status.Incorrect,-1,""
            else:
                return Status.Incorrect,-1,""

        elif file_out.find("Runaway argument?") != -1 or file_out.find("Runaway text?") != -1 or file_out.find("Missing } inserted.") != -1 or file_out.find("Missing { inserted.") != -1  or file_out.find("(\end occurred inside a group at level") != -1:
            if not trace: return Status.Incorrect,-1,""
            input_str = close_string(input_str, trace)
            rv, n, x = validate_tex(input_str, -1, [])
            if rv == Status.Complete:
                return Status.Incomplete,-1,"" # Append more
            else:
                return Status.Incorrect,-1,""

        else:
            return Status.Incorrect,-1,""

    except Exception as e:
        return Status.Incorrect,-1,""


def close_string(curr_input, trace):
    i = len(trace)
    while 0 < i:
        i = i-1
        char = trace[i]
        curr_input = curr_input + char
    return curr_input

import time
os.remove("valid_inputs.txt")
def save_valid_input(created_string):
    with open("valid_inputs.txt", "a") as myfile:
        var = repr(created_string) + "\n"
        myfile.write(var)
        myfile.close()

def save_crash(created_string, code):
    with open("crashes.txt", "a") as myfile:
        var = "Exit code: " + code + " Input: " + repr(created_string) + "\n"
        myfile.write(var)
        myfile.close()
