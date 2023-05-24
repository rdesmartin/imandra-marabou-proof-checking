#! /usr/bin/python

import sys
import os
import regex as re
import subprocess
from datetime import datetime as dt

LOG_FILE = "./experiments.log"
RESULT_FILE = "./timing.csv"
PATH="./acas_xu_verification"
# PATH = "./test_automation"
TIMEOUT=5*3600  # in seconds
IMANDRA_CMD = ["imandra", "core", "repl",
        "-use", "floor.iml",
        "-use", "matrix.iml",
        "-use", "fully_connected.iml",
        "-use", "acas_xu_network.iml",
        "-use", "acas_xu_properties.iml",
        "-use", "acas_xu_proof.iml",
        "-timeout", str((TIMEOUT) * 1000),    # in ms
    ]

def log(msg):
    with open(LOG_FILE, "a+") as f:
        f.write(f"\n{dt.now()}: {msg}\n")

def record_result(p, i,j, status, time):
    with open(RESULT_FILE, "a") as f:
        f.write(f"{p};{i},{j};{status};{time}\n")    

def main():
    files = sorted([f for f in os.listdir(PATH)])
    files = files[32:]
    ex = re.compile('^property_(\d+)_network_(\d+)_(\d+)\.iml$')

    try:
        for f in files:
            print(f)
            m = ex.match(f)
            if not m:
                continue
            [property,i,j] = [m.group(x) for x in range (1,4)]
            status = "OK"
            start = dt.now()
            try:
                with open (f"{PATH}/{f}") as stdin:
                    res = subprocess.run(
                        IMANDRA_CMD,
                        stdin=stdin,
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
            if "Overflow encountered" in res.stdout:
                status = "overflow"
                record_result(property,i,j,status, (end - start))
            log(f"Property {property} Network {i},{j} finished; status: {status}\n")
            log(res.stdout)
            log("==========")
            print(f"{f}: {status}")
    except KeyboardInterrupt:
        print('interrupted')
        sys.exit(1)

if __name__ == "__main__":
    main()
