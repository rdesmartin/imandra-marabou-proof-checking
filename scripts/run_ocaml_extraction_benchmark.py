#! /usr/bin/python

import sys
import os
import subprocess
from datetime import datetime as dt

CMD = "dune exec -- ./proof_checker/main_extract.exe".split(' ')
LOG_FILE = "./experiments.log"
RESULT_FILE = "./timing.csv"

TIMEOUT=5*3600  # in seconds

TEST_SIMPLE = [
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

TEST_ROBOTICS = [
    "./examples/robotics_proofs/DDQN_id215_ep43595_right_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id352_ep25386_left_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id35_ep25031_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id35_ep27214_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id418_ep26849_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id425_ep46171_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id444_ep31867_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id491_ep31556_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id502_ep62496_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id502_ep62529_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id518_ep33724_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id530_ep73981_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id530_ep77583_forward_collision_k_1_ipq_proof.json",
    "./examples/robotics_proofs/DDQN_id530_ep92129_forward_collision_k_1_ipq_proof.json"
    ]

TEST_ROBOTICS_PPO = [
    "PPO_id234_ep13098_forward_collision_k_1_ipq_proof.json",
    "PPO_id234_ep13140_forward_collision_k_1_ipq_proof.json",
    "PPO_id234_ep13140_left_collision_k_1_ipq_proof.json",
    "PPO_id234_ep13751_forward_collision_k_1_ipq_proof.json",
    "PPO_id234_ep14428_forward_collision_k_1_ipq_proof.json",
    "PPO_id239_ep17701_forward_collision_k_1_ipq_proof.json",
    "PPO_id239_ep17701_left_collision_k_1_ipq_proof.json",
    "PPO_id239_ep17701_right_collision_k_1_ipq_proof.json",
    "PPO_id240_ep26126_forward_collision_k_1_ipq_proof.json",
    "PPO_id240_ep26126_left_collision_k_1_ipq_proof.json",
    "PPO_id240_ep26126_right_collision_k_1_ipq_proof.json",
    "PPO_id240_ep43701_forward_collision_k_1_ipq_proof.json",
    "PPO_id240_ep43701_left_collision_k_1_ipq_proof.json",
    "PPO_id240_ep43701_right_collision_k_1_ipq_proof.json",
    "PPO_id240_ep73010_right_collision_k_1_ipq_proof.json",
    "PPO_id240_ep80772_right_collision_k_1_ipq_proof.json",
    "PPO_id240_ep83225_right_collision_k_1_ipq_proof.json",
    "PPO_id286_ep18520_forward_collision_k_1_ipq_proof.json",
    "PPO_id286_ep18520_right_collision_k_1_ipq_proof.json",
    "PPO_id286_ep22990_forward_collision_k_1_ipq_proof.json",
    "PPO_id286_ep26930_forward_collision_k_1_ipq_proof.json",
    "PPO_id286_ep26974_forward_collision_k_1_ipq_proof.json",
    "PPO_id379_ep22249_left_collision_k_1_ipq_proof.json",
    "PPO_id379_ep22249_right_collision_k_1_ipq_proof.json",
    "PPO_id379_ep27426_left_collision_k_1_ipq_proof.json",
    "PPO_id379_ep27426_right_collision_k_1_ipq_proof.json",
    "PPO_id379_ep28018_left_collision_k_1_ipq_proof.json",
    "PPO_id379_ep29231_left_collision_k_1_ipq_proof.json",
    "PPO_id379_ep29231_right_collision_k_1_ipq_proof.json",
    "PPO_id381_ep8730_forward_collision_k_1_ipq_proof.json",
    "PPO_id381_ep8730_left_collision_k_1_ipq_proof.json",
    "PPO_id381_ep8730_right_collision_k_1_ipq_proof.json",
    "PPO_id381_ep8763_forward_collision_k_1_ipq_proof.json",
    "PPO_id381_ep8763_left_collision_k_1_ipq_proof.json",
    "PPO_id381_ep8763_right_collision_k_1_ipq_proof.json",
    "PPO_id425_ep32806_left_collision_k_1_ipq_proof.json",
    "PPO_id425_ep37270_left_collision_k_1_ipq_proof.json",
    "PPO_id444_ep35805_right_collision_k_1_ipq_proof.json",
    "PPO_id444_ep36332_right_collision_k_1_ipq_proof.json",
    "PPO_id444_ep37351_right_collision_k_1_ipq_proof.json",
    "PPO_id444_ep38082_right_collision_k_1_ipq_proof.json",
    "PPO_id457_ep22066_left_collision_k_1_ipq_proof.json",
    "PPO_id457_ep22066_right_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13575_forward_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13575_left_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13597_forward_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13597_left_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13597_right_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13753_forward_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13753_left_collision_k_1_ipq_proof.json",
    "PPO_id502_ep13753_right_collision_k_1_ipq_proof.json",
    "PPO_id502_ep15459_forward_collision_k_1_ipq_proof.json",
    "PPO_id502_ep15459_left_collision_k_1_ipq_proof.json",
    "PPO_id502_ep15459_right_collision_k_1_ipq_proof.json",
    "PPO_id502_ep16596_forward_collision_k_1_ipq_proof.json",
    "PPO_id502_ep16596_left_collision_k_1_ipq_proof.json",
    "PPO_id502_ep16596_right_collision_k_1_ipq_proof.json",
    "PPO_id512_ep20664_left_collision_k_1_ipq_proof.json",
    "PPO_id549_ep15436_forward_collision_k_1_ipq_proof.json",
    "PPO_id549_ep16970_forward_collision_k_1_ipq_proof.json",
    "PPO_id73_ep10941_right_collision_k_1_ipq_proof.json",
    "PPO_id77_ep27458_forward_collision_k_1_ipq_proof.json",
    "PPO_id77_ep28078_forward_collision_k_1_ipq_proof.json",
    "PPO_id90_ep11133_forward_collision_k_1_ipq_proof.json",
    "PPO_id90_ep11133_left_collision_k_1_ipq_proof.json",
    "PPO_id90_ep11133_right_collision_k_1_ipq_proof.json",
    "REI_id158_ep53113_forward_collision_k_1_ipq_proof.json",
    "REI_id158_ep53113_left_collision_k_1_ipq_proof.json",
    "REI_id158_ep53113_right_collision_k_1_ipq_proof.json",
    "REI_id158_ep53499_forward_collision_k_1_ipq_proof.json",
    "REI_id158_ep53499_right_collision_k_1_ipq_proof.json",
    "REI_id158_ep53554_forward_collision_k_1_ipq_proof.json",
    "REI_id158_ep59378_forward_collision_k_1_ipq_proof.json",
    "REI_id77_ep49509_forward_collision_k_1_ipq_proof.json",
    "REI_id77_ep49509_left_collision_k_1_ipq_proof.json",
    "REI_id77_ep75183_forward_collision_k_1_ipq_proof.json"
]


def log(msg):
    with open(LOG_FILE, "a+") as f:
        f.write(f"\n{dt.now()}: {msg}\n")

def record_result(input_config, status, result, time):
    with open(RESULT_FILE, "a") as f:
        f.write(f"{input_config};{status};{result};{time}\n")    

def main():
    files = TEST_SIMPLE

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
