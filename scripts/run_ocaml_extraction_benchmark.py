#! /usr/bin/python

import sys
import os
import subprocess
from datetime import datetime as dt

CMD = "dune exec -- ./proof_checker/main_program.exe".split(' ')
LOG_FILE = "./experiments.log"
RESULT_FILE = "./timing.csv"

TIMEOUT=5*3600  # in seconds

TEST_FILES = [
    "json/acasxu_2_9_3_LEMMAS.json",
    "json/acasxu_3_7_3_LEMMAS.json", 
    "json/acasxu_5_7_3_LEMMAS.json",  
    "json/acasxu_5_9_3_LEMMAS.json",
    "json/acasxu_2_9_4_LEMMAS.json",  
    # "json/acasxu_2_9_p3_NL.json",
    # "json/acasxu_2_9_p4_NL.json",
    # "json/acasxu_3_7_p3_NL.json",  
    # "json/acasxu_5_7_p3_NL.json",  
    # "json/acasxu_5_9_p3_NL.json",
]

def log(msg):
    with open(LOG_FILE, "a+") as f:
        f.write(f"\n{dt.now()}: {msg}\n")

def record_result(input_config, status, time):
    with open(RESULT_FILE, "a") as f:
        f.write(f"{input_config};{status};{time}\n")    

def main():
    files = TEST_FILES

    try:
        for file_name in files:
            print(file_name)
            status = "OK"
            start = dt.now()
            try:
                res = subprocess.run(
                    CMD + [file_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=TIMEOUT
                )
            except (TimeoutError):
                status = "TIMEOUT"
            end = dt.now()
            if res.returncode == 1:
                status = "KO"

            record_result(file_name,status, (end - start))
            log(f"Proof {file_name} finished; status: {status}\n")
            log(res.stdout)
            log("==========")
            print(f"{file_name}: {status}")
    except KeyboardInterrupt:
        print('interrupted')
        sys.exit(1)

if __name__ == "__main__":
    main()
