#! /usr/bin/python

import sys
import os
import subprocess
from datetime import datetime as dt

CMD = "dune exec -- ./proof_checker/main_extract.exe".split(' ')
LOG_FILE = "./experiments.log"
RESULT_FILE = "./timing.csv"

TIMEOUT=5*3600  # in seconds

TEST_FILES = [
    "./examples/proof_reluBenchmark0.05650806427s.json", 
    "./examples/proof_reluBenchmark0.05650806427s_lemmas.json", 
    "./examples/proof_reluBenchmark0.15145778656s.json", 
    "./examples/proof_reluBenchmark0.15145778656s_lemmas.json", 
    "./examples/proof_reluBenchmark0.19238615036s.json", 
    "./examples/proof_reluBenchmark0.19238615036s_lemmas.json", 
    "./examples/proof_reluBenchmark0.24204993248s.json", 
    "./examples/proof_reluBenchmark0.24204993248s_lemmas.json", 
    "./examples/proof_reluBenchmark0.24551987648s.json", 
    "./examples/proof_reluBenchmark0.24551987648s_lemmas.json", 
    "./examples/proof_reluBenchmark0.359375s.json", 
    "./examples/proof_reluBenchmark0.359375s_lemmas.json", 
    "./examples/proof_reluBenchmark0.479170084s.json", 
    "./examples/proof_reluBenchmark0.479170084s_lemmas.json"
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
