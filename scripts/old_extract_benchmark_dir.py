#! /usr/bin/python

import argparse
import sys
import os
import subprocess
from datetime import datetime as dt
 
DATE = dt.now().isoformat()
CMD = "dune exec -- ./proof_checker/main_extract.exe".split(' ')
LOG_FILE = f"{DATE}_old_experiment.log"
RESULT_FILE = f"{DATE}_old_timing.csv"

TIMEOUT=5*3600  # in seconds
TEST_DIR = "./json"

def create_parser():
    parser = argparse.ArgumentParser(description="Process some options with default values.")

    parser.add_argument(
        "-d", "--directory",
        type=str,
        default=TEST_DIR,
        help=f"Path to the input directory (default: '{TEST_DIR}')"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./experiments/",
        help="Path to the output directory (default: 'default_output_directory')"
    )

    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=TIMEOUT,
        help=f"Timeout value in seconds (default: {TIMEOUT})"
    )

    return parser

def log(log_file, msg):
    with open(log_file, "a+") as f:
        f.write(f"\n{dt.now()}: {msg}\n")

def record_result(results_file, input_config, status, result, time):
    with open(results_file, "a") as f:
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
            json_paths.append('/'.join([dir_path, file_path]))
    return json_paths


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    log_file = '/'.join([args.output, 'log.txt'])
    results_file = '/'.join([args.output, 'results.csv'])

    files = get_json_files(args.directory)

    try:
        for file_path in files:
            print(file_path)
            status = "OK"
            start = dt.now()
            try:
                res = subprocess.run(
                    CMD + [file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=args.timeout
                )
            except (TimeoutError):
                status = "TIMEOUT"
            end = dt.now()
            if res.returncode == 1:
                status = "KO"
            result = res.stdout.split()[-1]
            record_result(results_file, file_path, status, result, (end - start))
            log(log_file, f"Proof {file_path} finished; status: {status}\n")
            log(log_file, res.stdout)
            log(log_file, "==========")
            print(f"{file_path}: {status}; result: {result}")
    except KeyboardInterrupt:
        print('interrupted')
        sys.exit(1)