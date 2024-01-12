import numpy as np
import os
import matplotlib.pyplot as plt

def compute_s(n, k, epsilon_l, epsilon, delta):
    lambda_ = k / (np.exp(epsilon_l) + k - 1)
    s = (14 * k * np.log(4 / delta) / epsilon**2 + 1 + np.sqrt(2 * (n-1) * lambda_ * np.log(2 / delta)) - (n-1) * lambda_) / n
    #s = 14 * np.sqrt(k) * np.log(4 / delta) * np.sqrt(np.exp(epsilon_l) + k - 1) / (epsilon**2 * n)

    return s

def main():
    epsilon_l = [6, 7, 8, 9, 10]
    epsilon1 = 0.1
    epsilon2 = 0.2
    epsilon3 = 0.3
    delta = 1.0e-6
    n = 500000
    k = 50

    s1 = np.zeros(len(epsilon_l), dtype = float)
    s2 = np.zeros(len(epsilon_l), dtype = float)
    s3 = np.zeros(len(epsilon_l), dtype = float)
    
    for i, epsl in enumerate(epsilon_l):
        s1[i] = compute_s(n, k, epsl, epsilon1, delta)
        s2[i] = compute_s(n, k, epsl, epsilon2, delta)
        s3[i] = compute_s(n, k, epsl, epsilon3, delta)

    plt.style.use("seaborn-whitegrid")

    fig, ax = plt.subplots(figsize = (4, 3))
    ax.set_ylabel("s", fontsize = 12)
    ax.set_xlabel(r"$\epsilon_l$", fontsize = 12)
    ax.set_xticks(epsilon_l)
    ax.tick_params(axis="both", labelsize=8.5)
    
    ax.plot(epsilon_l,
            s1,
            label = r"$\epsilon=0.1$",
            marker = "*",
            markerfacecolor = 'none')
 
    ax.plot(epsilon_l,
            s2,
            label = r"$\epsilon=0.2$",
            marker = "o",
            markerfacecolor = 'none')

    ax.plot(epsilon_l,
            s3,
            label = r"$\epsilon=0.3$",
            marker = "s",
            markerfacecolor = 'none')

    ax.legend(fontsize=8.5)

    fig.tight_layout()
    filename = "happy"
    fig.savefig(os.path.join("./fig", filename + ".png"), dpi=1200)
    #fig.savefig(os.path.join("./fig/eps", filename + ".eps"), dpi=1200)

if __name__ == "__main__":
    main()



