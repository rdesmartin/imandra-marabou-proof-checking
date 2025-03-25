#! /usr/bin/python

import argparse
import sys
import os
import subprocess
from datetime import datetime as dt
import concurrent.futures
from threading import Lock 
 
DATE = dt.now().isoformat()
# CMD = "dune exec -- ./imandrax/main_extract.exe".split(' ')
CMD = "./_build/default/imandrax/main_extract.exe".split(' ')
LOG_FILE = f"{DATE}_experiment.log"
RESULT_FILE = f"{DATE}_timing.csv"

TIMEOUT=5*3600  # in seconds
TEST_DIR = "./json"

# Create a lock for thread-safe file writing
log_lock = Lock()

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

def process_file(file_path):
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
    with log_lock:
        record_result(results_file, file_path, status, result, (end - start))
        log(log_file, f"Proof {file_path} finished; status: {status}\n")
        log(log_file, res.stdout)
        log(log_file, "==========")
        print(f"{file_path}: {status}; result: {result}")
        return file_path, status

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    log_file = '/'.join([args.output, LOG_FILE])
    results_file = '/'.join([args.output, RESULT_FILE])

    files = get_json_files(args.directory)
    num_threads = min(32, os.cpu_count() + 4)

    try:
        # for file_path in files:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit all files for processing
                futures = {
                    executor.submit(process_file, file_path): file_path 
                    for file_path in files
                }
        
            # Process completed futures
            for future in concurrent.futures.as_completed(futures):
                try:
                    file_path, status = future.result()
                    # Optional: print completion status
                    print(f"Completed: {file_path} - {status}")
                except Exception as exc:
                    print(f"{futures[future]} generated an exception: {exc}")

    except KeyboardInterrupt:
        print('interrupted')
        sys.exit(1)