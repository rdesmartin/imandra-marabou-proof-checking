#! /usr/bin/python

import sys
import os
import subprocess
from datetime import datetime as dt

CMD = "dune exec -- ./proof_checker/main_extract.exe".split(' ')
LOG_FILE = "./experiments.log"
RESULT_FILE = "./timing.csv"

TIMEOUT=5*3600  # in seconds

TEST_DIR = "./examples"

def log(msg):
    with open(LOG_FILE, "a+") as f:
        f.write(f"\n{dt.now()}: {msg}\n")

def record_result(input_config, status, result, time):
    with open(RESULT_FILE, "a") as f:
        f.write(f"{input_config};{status};{result};{time}\n")    

def get_json_files(dir_path):
    json_paths = []
    # Iterate through files in the directory
    for file in os.listdir(dir_path):
        # Check if the file is a JSON file
        if file.endswith(".json"):
            # Construct the relative path
            file_path = os.path.relpath(os.path.join(dir_path, file), dir_path)
            # Append the relative path to the list
            json_paths.append(file_path)
    return json_paths

def main():
    files = get_json_files(TEST_DIR)

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
            result = res.stdout.split()[-1]
            record_result(file_name,status, result, (end - start))
            log(f"Proof {file_name} finished; status: {status}\n")
            log(res.stdout)
            log("==========")
            print(f"{file_name}: {status}; result: {result}")
    except KeyboardInterrupt:
        print('interrupted')
        sys.exit(1)

if __name__ == "__main__":
    main()
