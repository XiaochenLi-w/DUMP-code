import math
import yaml
import random
import argparse
import copy
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

def gen_dummy(n, s, k):
    dummy_set = np.random.randint(0, k, math.ceil(n * s))
    return dummy_set

def mix_dummy(data, k, epsl, epsilon, delta):
    n=len(data)
    p = math.exp(epsl) / (math.exp(epsl) + k - 1)
    q = 1 / (math.exp(epsl) + k - 1)
    
    # randomize real data
    randomized_response(data, k, p)

    # compute the number of dummy data
    lambda_ = k / ((math.exp(epsl) + k - 1) * (k - 1))
    s = (14 * k * math.log(4 / delta) / (epsilon**2) + 1 + math.sqrt(2 * (n - 1) * lambda_ * math.log(2 / delta)) - (n - 1) * lambda_) / n

    # generate dummy data
    dummy_set = gen_dummy(n, s, k)
    # get shuffled data
    shuffled_data = np.append(data, dummy_set)

    # estimation
    freq = np.zeros(k, dtype = int)
    freq = (np.bincount(shuffled_data) - n * q - (math.ceil(n * s)) / k) / (p - q)

    return freq

def compute_mse(lock, data, k, true_freq, mse, **kwargs):
    results = {}
    n = len(data)
    results["epsilon"] = kwargs["epsilon"]
    error=0
    for r in range(kwargs["nround"]): 
        pre_freq = mix_dummy(copy.deepcopy(data), k, kwargs["epsilon_l"], kwargs["epsilon"], kwargs["delta"])
        error += np.square((pre_freq - true_freq) / n).sum()
    results["mse"] = error / (k * kwargs["nround"])
    with lock:
        mse.append(results)
    print(results)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./config/test.yml")
    args = parser.parse_args()
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    data = np.loadtxt(config["data_path"], dtype=int)
    k = np.max(data)+1
    true_freq = np.zeros(k, dtype=int)
    true_freq = np.bincount(data)

    pconfig={}
    epsilon_list = config["epsilon_list"]
    pconfig["delta"] = config["delta"]
    pconfig["nround"] = config["nround"]
    pconfig["epsilon_l"] = config["epsilon_l"]

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