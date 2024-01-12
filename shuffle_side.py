import argparse
import os
import math
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

color_list = sns.color_palette("bright", 8)

k = [10, 20, 30]
epsilon_l = 5
delta = 1.0e-4
s = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
s_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
eps = np.zeros((3,10), dtype = float)

for k_index in range(3):
    for s_index in range(10):
        temp1 = 1 - np.sqrt(2 * k[k_index] * np.log(1 / delta) / s[s_index])
        temp2 = np.exp(epsilon_l) / (s[s_index] * (np.exp(epsilon_l) + 1))
        eps[k_index, s_index] = np.log(k[k_index] / temp1 * (1 + temp2))

fig, ax = plt.subplots(figsize = (5, 3))
ax.set_ylabel(r"$\epsilon_r$", fontsize = 12)
ax.set_xlabel("s", fontsize = 14)
ax.set_xticks(s_x)
plt.text(10, 1.95, r'x 10$^{3}$',fontsize=8)
ax.tick_params(axis="both", labelsize=8.5)

ax.plot(s_x,
        eps[0],
        label = "k=10",
        marker = "*",
        markersize = 8,
        linestyle='-',
        #color = 'k',
        color = color_list[0],
        markerfacecolor = 'none')

ax.plot(s_x,
        eps[1],
        label = "k=20",
        marker = "o",
        markersize = 8,
        linestyle='--',
        #color = 'k',
        color = color_list[2],
        markerfacecolor = 'none')

ax.plot(s_x,
        eps[2],
        label = "k=30",
        marker = "+",
        markersize = 8,
        linestyle='-.',
        #color = 'k',
        color = color_list[3],
        markerfacecolor = 'none')

ax.legend(fontsize=8.5)
fig.tight_layout()
plt.show()
filename = "shuffle"
fig.savefig(os.path.join("./fig_v", filename + ".png"), dpi=1200)
fig.savefig(os.path.join("./fig_v/eps", filename + ".pdf"), dpi=1200)