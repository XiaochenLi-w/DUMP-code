import math
import argparse
import yaml
from multiprocessing import Process, Lock, Manager
from operator import itemgetter
import numpy as np

def gen_dummy(n, s, k):
    dummy_set = np.random.randint(0, k, math.ceil(n*s))
    return dummy_set

def pure_dummy (data, k, epsilon, delta):
    n = len(data)
    # compute the number of dummy data
    s = (14 * k * math.log(2/delta) / (epsilon**2) + 1 ) / n

    # generate dummy data
    dummy_set = gen_dummy(n, s, k)
    # get shuffled data
    shuffled_data = np.append(data, dummy_set)

    # estimation
    freq = np.zeros(k, dtype = int)
    freq = np.bincount(shuffled_data) - math.ceil(n * s) / k

    return freq

def compute_mse(lock, data, k, true_freq, mse, **kwargs):
    results = {}
    n = len(data)
    results["epsilon"] = kwargs["epsilon"]
    error=0
    for r in range(kwargs["nround"]): 
        pre_freq = pure_dummy(data, k, kwargs["epsilon"], kwargs["delta"])
        error += np.square((pre_freq - true_freq) / n).sum()
    results["mse"] = error/(k * kwargs["nround"])
    with lock:
        mse.append(results)
    print(results)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./config/pDUMP_kosarak1.yml")
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
                kwargs = pconfig ))

    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    
    mse = sorted(mse, key = itemgetter("epsilon"))
    print(mse)


if __name__ == "__main__":
    main()