import numpy as np
import numba as nb
import math
import argparse
import yaml
import random
import copy
import xxhash
from multiprocessing import Process, Lock, Manager
from operator import itemgetter

def olh(data, k, epsilon, delta):
    n = len(data)
    # compute optimal size of hash domain
    m = epsilon**2 * (n-1) / (14 * np.log(2 / delta))
    d = np.floor((m + 2) / 3)
    
    #compute local privacy budget, out of range has no privacy amplification
    epsilon_l = epsilon**2 * (n - 1) / (14 * np.log(2 / delta)) + 1 - d
    if epsilon_l < 1:
        epsilon_l = epsilon
    else:
        epsilon_l = np.log(epsilon_l)

    p = np.exp(epsilon_l) / (np.exp(epsilon_l) + d - 1)
    #q = 1 / (np.exp(epsilon_l) + d - 1)

    for i in range(n):
        v = data[i]
        x = (xxhash.xxh32(str(v), seed=i).intdigest() % d)
        y = x

        if random.random() > p:
            while y == x:
                y = np.random.randint(0, d)

        data[i] = y

    #estimate randimized data
    pre_freq = np.zeros(k, dtype = int)
    for i in range(n):
        for v in range(k):
            if data[i] == (xxhash.xxh32(str(v), seed=i).intdigest() % d):
                pre_freq[v] += 1
    a = 1.0 * d / (p * d - 1)
    b = 1.0 * n / (p * d - 1)
    pre_freq = a * pre_freq - b

    return pre_freq

def compute_mse(lock, data, k, true_freq, mse, **kwargs):
    n = len(data)
    results = {}
    results["epsilon"] = kwargs["epsilon"]
    error = 0

    for r in range(kwargs["nround"]):
        pre_freq = olh(copy.deepcopy(data), k, kwargs["epsilon"], kwargs["delta"])
        error += np.square((true_freq - pre_freq) / n).sum()
    
    results["mse"] = error / (k * kwargs["nround"])

    with lock:
        mse.append(results)
    print(results)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./config/syn.yml")
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
