import math
import yaml
import random
import copy
import argparse
from multiprocessing import Process, Lock, Manager
from operator import itemgetter
import numpy as np
import numba as nb

@nb.jit(nopython=True)
def randomized_response(data, k, p):
    for idx, num in enumerate(data):
        randomized_value = num
        if random.random() > p:
            while randomized_value == num:
                randomized_value = np.random.randint(0, k)
        data[idx] = randomized_value

def shuffle_based(data, k, epsilon, delta):
    n = len(data)
    # if epsilon out of the valid range, there is no amplification effect
    if epsilon > math.sqrt(14 * k * math.log(2 / delta) / (n - 1)):
        epsilon_l = math.log((epsilon**2) * (n-1) / (14 * math.log(2 / delta)) + 1 - k)
    else:
        epsilon_l = epsilon
    
    # randomize real data to satisfy ldp
    p = math.exp(epsilon_l) / (math.exp(epsilon_l) + k - 1)
    q = 1 / (math.exp(epsilon_l) + k - 1)
    randomized_response(data, k, p)

    # estimation
    freq = np.zeros(k, dtype = int)
    freq = (np.bincount(data) - q * n) / (p - q)
    
    return freq

def compute_mse(lock, data, k, true_freq, mse, **kwargs):
    n = len(data)
    results = {}
    results["epsilon"] = kwargs["epsilon"]
    error = 0

    for r in range(kwargs["nround"]):
        pre_freq = shuffle_based(copy.deepcopy(data), k, kwargs["epsilon"], kwargs["delta"])
        error += np.square((true_freq - pre_freq) / n).sum()
    
    results["mse"] = error / (k * kwargs["nround"])

    with lock:
        mse.append(results)
    print(results)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./config/shuffle_based_ipums1.yml")
    args = parser.parse_args()
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    data = np.loadtxt(config["data_path"], dtype = int)
    k = np.max(data)+1
    true_freq = np.zeros(k, dtype = int)
    true_freq = np.bincount(data)

    pconfig={}
    epsilon_list = config["epsilon_list"]
    pconfig["delta"] = config["delta"]
    pconfig["nround"] = config["nround"]

    p_list = []
    lock = Lock()
    manager = Manager()
    mse = manager.list()

    for epsilon in epsilon_list:
        pconfig["epsilon"] = epsilon
        p_list.append(
            Process(
                target = compute_mse,
                args = (lock, data, k, true_freq, mse),
                kwargs = pconfig))

    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    
    mse = sorted(mse, key = itemgetter("epsilon"))
    print(mse)


if __name__ == "__main__":
    main()