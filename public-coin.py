import numpy as np
import math
import random
import xxhash
import copy
import argparse
import yaml
from multiprocessing import Process, Lock, Manager
from operator import itemgetter

def public_coin(data, k, epsilon, delta):
    # public parameters
    n = len(data)
    tau_ = math.ceil(np.log(2 * k))
    s = 2 * n
    gamma_ = 90 * tau_**2 * np.log(2 * tau_ / delta) / (n * epsilon**2)

    # public randomness
    hash_family = np.random.randint(0, 1.0e8, tau_) #select tau_ hash functions

    # encode
    T = np.zeros([tau_, s], dtype = int)

    for j, value in enumerate(data): # encode data
        for t, seed_ in enumerate(hash_family):
            h = xxhash.xxh32(str(value), seed=seed_).intdigest() % s 
            T[t, h] += 1

    for t in range(tau_): #add noise
        for l in range(s):
            T[t, l] += np.random.binomial(n, gamma_)
    
    # decode
    pre_fre = np.zeros(k, dtype = int)

    for value in range(k):
        min_ = 2 * n + 1
        for t, seed_ in enumerate(hash_family):
            h = xxhash.xxh32(str(value), seed=seed_).intdigest() % s
            if min_ > T[t, h]:
                min_ = T[t, h]
        pre_fre[value] = max(min_ - gamma_ * n, 0)

    return pre_fre

def compute_mse(lock, data, k, true_freq, mse, **kwargs):
    
    n = len(data)
    results = {}
    results["epsilon"] = kwargs["epsilon"]
    error = 0

    for r in range(kwargs["nround"]):
        pre_freq = public_coin(copy.deepcopy(data), k, kwargs["epsilon"], kwargs["delta"])
        error += np.square((true_freq - pre_freq) / n).sum()
    
    results["mse"] = error / (k * kwargs["nround"])

    with lock:
        mse.append(results)
    print(results)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./config/public_coin.yml")
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