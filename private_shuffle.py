import math
import yaml
import random
import argparse
from multiprocessing import Process, Lock, Manager
from operator import itemgetter
import numpy as np


def randomize_hist(data, k, true_freq, epsilon, delta):
    n = len(data)
    randomize_freq = np.zeros(k, dtype = int)

    p = 1 - 50 * math.log(2 / delta) / ((epsilon**2) * n)
    if p < 0:
        p = 0
 
    for i in range(k):
        randomize_freq[i] = true_freq[i] + np.random.binomial(n, p)
    
    '''
    pre_freq = np.zeros(k, dtype = int)
    for i in range(k):
        if randomize_freq[i] - n * p < 0:
            pre_freq[i] = randomize_freq[i] - n * p
    '''
    pre_freq = randomize_freq - n * p
    return pre_freq

def compute_mse(lock, data, k, true_freq, mse, **kwargs):
    n = len(data)
   
    results = {}
    error = 0
    results["epsilon"] = kwargs["epsilon"]

    for r in range(kwargs["nround"]):
        pre_freq = randomize_hist(data, k, true_freq, kwargs["epsilon"], kwargs["delta"])
        error += np.square((pre_freq - true_freq) / n).sum()

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
