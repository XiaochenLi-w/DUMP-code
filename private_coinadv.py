import numpy as np
import numba as nb
import math
import copy
from scipy.linalg import hadamard
import argparse
import yaml
from multiprocessing import Process, Lock, Manager
from operator import itemgetter
import time

def codeword_gen(k):
    codewords = np.empty([2 * k - 1, k], dtype = int)
    hadamard_ = hadamard(2 * k)
    
    for value in range(2 * k - 1): # the first row in hadamard cannot be used
        codeword = 0
        for index in range(2 * k): # select idex of 1 per row, half of values equal to 1 per row
            if hadamard_[value + 1, index] == 1:
                codewords[value, codeword] = index # save the index as the hadamard codeword
                codeword += 1
    
    return codewords

@nb.jit(nopython=True)
def encode_data(data, n, k, tau, rho, codewords, data_encoded):

    for data_idex in range(n):
        for codeword_idex in range(tau):
            data_encoded[data_idex, codeword_idex] = codewords[data[data_idex], np.random.randint(0, k)]

    for rho_idex in range(n, n + rho * n):
        data_encoded[rho_idex] = np.random.randint(0, 2 * k, tau)

@nb.jit(nopython=True)
def decode_data(n, k, rho, codewords, data_encoded, freq):
    data_encoded_size = rho * n + n

    for item in range(k):
        print(time.time())
        for idex in range(data_encoded_size):
            if set(data_encoded[idex]).issubset(set(codewords[item])):
               freq[item] += 1
        print(time.time())

def private_coin(data, k, codewords, epsilon, delta):
    n = len(data)
    rho = math.ceil(36 * math.log(1 / (delta)) / (epsilon**2))
    tau = math.ceil(math.log2(n))

    data_encoded = np.zeros([n + n * rho, tau], dtype = int)

    # encode data
    encode_data(data, n, k, tau, rho, copy.deepcopy(codewords), data_encoded)

    dummy_encoded = np.random.randint(0, 2 * k, tau * n * rho).reshape(n * rho, tau)
    data_encoded = np.concatenate((data_encoded, dummy_encoded), axis = 0)

    # decode data
    freq = np.zeros(k, dtype = int)
    decode_data(n, k, rho, copy.deepcopy(codewords), data_encoded, freq)

    pre_freq = (freq - (rho + 1) * n / np.power(2, tau)) / (1 - 1 / np.power(2, tau))

    return pre_freq

def compute_mse(lock, data, k, codewords, true_freq, mse, **kwarges):
    n = len(data)
    results = {}
    error = 0
    results["epsilon"] = kwarges["epsilon"]

    for r in range(kwarges["nround"]):
        pre_freq = private_coin(data, k, codewords, kwarges["epsilon"], kwarges["delta"])
        error += np.square((pre_freq - true_freq) / n).sum()
    
    results["mse"] = error / (kwarges["nround"] * k)
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
    true_freq = np.zeros(k, dtype = int)
    true_freq = np.bincount(data)
    
    codewords = codeword_gen(k)
    
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
                args = (lock, data, k, codewords, true_freq, mse),
                kwargs = pconfig))

    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    
    mse = sorted(mse, key = itemgetter("epsilon"))
    print(mse) 

if __name__ == "__main__":
    main()