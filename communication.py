import argparse
import os
import math
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import yaml

def messages_pureDUMP(n, k, epsilon, delta):
    s = (14 * k * math.log(2 / delta) / epsilon**2 + 1) / n

    return s

def messages_mixDUMP(n, k, epsilon_l, epsilon, delta):
    lambda_ = k / (math.exp(epsilon_l) + k - 1)
    s = (14 * k * math.log(4 / delta) / epsilon**2 + 1 + math.sqrt(2 * (n - 1) * lambda_ * math.log(2 / delta)) - (n-1) * lambda_) / n

    return s

def messages_private_coin(epsilon, delta):
    s = 36 * math.log(math.exp(1) / (epsilon * delta)) / epsilon**2 + 1

    return s

def messages_private_shuffle(n, k, epsilon, delta):
    p = 1 - 50 * math.log(2 / delta) / (epsilon**2 * n)

    sum_ = 0
    for r in range(100):
        sum_ += np.random.binomial(k, p)

    sum_ = sum_ / 100 + 1

    return sum_

def messages_public_coin(n, k, epsilon, delta):
    s = 2 * n
    tau_ = math.ceil(np.log(2 * k))
    gamma_ = 90 * tau_**2 * np.log(2 * tau_ / delta) / (n * epsilon**2)

    sum_ = 0
    for r in range(100):
        sum_ += np.random.binomial(tau_ * s, gamma_)

    sum_ = sum_ / 100 + tau_

    return sum_

def messages_correlated_noise(n, k, epsilon, delta):
    sum_ = 1 + k * np.log(1 / delta)**2 / (epsilon**2 * n)

    return sum_

def main():
    # n = 990002
    # k = 41267
    # n = 70187
    # k = 900
    # n = 494352
    # k = 2000
    n = 500000
    k = 50
    delta = 1.0e-6
    delta1 = 1.0e-8
    epsilon_l = 8
    #epsilon_l1 = 5
    epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    epsilone = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    epsilone1 = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
#----------------------------------------------------------------
    pureDUMP_mess = np.zeros(len(epsilon), dtype = float)
    mixDUMP_mess = np.zeros(len(epsilon), dtype = float)
    private_coin_mess = np.zeros(len(epsilon), dtype = float)
    private_shuffle_mess = np.zeros(len(epsilon), dtype = float)
    public_coin_mess = np.zeros(len(epsilone), dtype = float)
    #correlated_noise = np.zeros(len(epsilon), dtype = float)
#---------------------------------------------------------------
    pureDUMP_mess1 = np.zeros(len(epsilon), dtype = float)
    mixDUMP_mess1 = np.zeros(len(epsilon), dtype = float)
    private_coin_mess1 = np.zeros(len(epsilon), dtype = float)
    private_shuffle_mess1 = np.zeros(len(epsilon), dtype = float)
    public_coin_mess1 = np.zeros(len(epsilone1), dtype = float)
    #correlated_noise1 = np.zeros(len(epsilon), dtype = float)
#---------------------------------------------------------------
    for idex, eps in enumerate(epsilon):
        pureDUMP_mess[idex] = messages_pureDUMP(n, k, eps, delta)
        mixDUMP_mess[idex] = messages_mixDUMP(n, k, epsilon_l, eps, delta)
        private_coin_mess[idex] = messages_private_coin(eps, delta)
        private_shuffle_mess[idex] = messages_private_shuffle(n, k, eps, delta)
        #correlated_noise[idex] = messages_correlated_noise(n, k, eps, delta)

    for idex, eps in enumerate(epsilone):
        #private_shuffle_mess[idex] = messages_private_shuffle(n, k, eps, delta)
        public_coin_mess[idex] = messages_public_coin(n, k, eps, delta)
#----------------------------------------------------------------
    for idex, eps in enumerate(epsilon):
        pureDUMP_mess1[idex] = messages_pureDUMP(n, k, eps, delta1)
        mixDUMP_mess1[idex] = messages_mixDUMP(n, k, epsilon_l, eps, delta1)
        private_coin_mess1[idex] = messages_private_coin(eps, delta1)
        private_shuffle_mess1[idex] = messages_private_shuffle(n, k, eps, delta1)
        #correlated_noise1[idex] = messages_correlated_noise(n, k, eps, delta1)

    for idex, eps in enumerate(epsilone1):
        #private_shuffle_mess1[idex] = messages_private_shuffle(n, k, eps, delta1)
        public_coin_mess1[idex] = messages_public_coin(n, k, eps, delta1)
#-----------------------------------------------------------------
    plt.style.use("seaborn-whitegrid")

    color_list = sns.color_palette("bright", 9)
    fig = plt.figure(figsize = (10, 5))

    ax = plt.subplot(1,2,1)
    ax.set_ylabel("number of messages", fontsize = 14)
    ax.set_xlabel(r"$\epsilon$", fontsize = 14)
    ax.set_xticks(epsilon)
    ax.tick_params(axis="both", labelsize=13)
    ax.set_title(r"(a) $\delta=10^{-6}$",y=-0.4, fontsize = 20)

    l2 = ax.semilogy(epsilon,
            private_coin_mess,
            label = "private-coin",
            color = color_list[1],
            marker = "s",
            markersize = 8,
            markerfacecolor = 'none')

    l3 = ax.semilogy(epsilone,
            public_coin_mess,
            label = "public-coin",
            color = color_list[2],
            marker = "^",
            markersize = 8,
            markerfacecolor = 'none')

    l4 = ax.semilogy(epsilon,
            private_shuffle_mess,
            label = "private-shuffle",
            color = color_list[5],
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

    l5 = ax.semilogy(epsilon,
            pureDUMP_mess,
            label = "pureDUMP",
            color = color_list[0],
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

    l6 = ax.semilogy(epsilon,
            mixDUMP_mess,
            label = "mixDUMP",
            color = color_list[3],
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

    # l7 = ax.semilogy(epsilon,
    #         correlated_noise,
    #         label = "correlated_noise",
    #         color = color_list[8],
    #         marker = "p",
    #         markersize = 8,
    #         markerfacecolor = 'none')
#--------------------------------------------------------------------
    ax1 = plt.subplot(1,2,2)
    ax1.set_ylabel("number of messages", fontsize = 14)
    ax1.set_xlabel(r"$\epsilon$", fontsize = 14)
    ax1.set_xticks(epsilon)
    ax1.tick_params(axis="both", labelsize=13)
    ax1.set_title(r"(b) $\delta=10^{-8}$",y=-0.4, fontsize = 20)

    ax1.semilogy(epsilon,
            private_coin_mess1,
            label = "private-coin",
            color = color_list[1],
            marker = "s",
            markersize = 8,
            markerfacecolor = 'none')

    ax1.semilogy(epsilone1,
            public_coin_mess1,
            label = "public-coin",
            color = color_list[2],
            marker = "^",
            markersize = 8,
            markerfacecolor = 'none')

    ax1.semilogy(epsilon,
            private_shuffle_mess1,
            label = "private-shuffle",
            color = color_list[5],
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

    ax1.semilogy(epsilon,
            pureDUMP_mess1,
            label = "pureDUMP",
            color = color_list[0],
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

    ax1.semilogy(epsilon,
            mixDUMP_mess1,
            label = "mixDUMP",
            color = color_list[3],
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

    # ax1.semilogy(epsilon,
    #         correlated_noise1,
    #         label = "correlated_noise",
    #         color = color_list[8],
    #         marker = "p",
    #         markersize = 8,
    #         markerfacecolor = 'none')
#--------------------------------------------------------------------
    legend_list = ['private-coin', 'public-coin', 'truncation-based', 'pureDUMP', 'mixDUMP'] 
    fig.legend([l2, l3, l4, l5, l6], labels =legend_list, loc='center', bbox_to_anchor=(0.5, 0.92), ncol=3, prop = {'size':14}, frameon = True, edgecolor = 'gray')

    fig.tight_layout()
    fig.subplots_adjust(left = 0.067, bottom = 0.252, right = 0.974, top = 0.845, wspace = 0.171, hspace = 0.2)
    plt.show()
    filename = "k_50_com"
    #fig.savefig(os.path.join("./fig_v/communication", filename + ".png"), dpi=3000)
    fig.savefig(os.path.join("./fig/eps1", filename + ".pdf"), dpi=3000)

if __name__ == "__main__":
    main()