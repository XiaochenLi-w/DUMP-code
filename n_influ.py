import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yaml

plt.style.use("seaborn-whitegrid")

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="./config/kn_influ/pureDUMP_n.yml")
args = parser.parse_args()
with open(args.config, "r") as f:
    config = yaml.safe_load(f)
#-----------------------mixDUMP-------------------
parser = argparse.ArgumentParser()
parser.add_argument("--config_m", default="./config/kn_influ/mixDUMP_n.yml")
args = parser.parse_args()
with open(args.config_m, "r") as f_m:
    config_m = yaml.safe_load(f_m)
#------------------------------------------------
n_5000 = config["n_5000"]
n_50000 = config["n_50000"]
n_500000 = config["n_500000"]

nt_5000 = config["nt_5000"]
nt_50000 = config["nt_50000"]
nt_500000 = config["nt_500000"]
#--------------------mixDUMP----------------------
nm_5000 = config_m["n_5000"]
nm_50000 = config_m["n_50000"]
nm_500000 = config_m["n_500000"]

ntm_5000 = config_m["nt_5000"]
ntm_50000 = config_m["nt_50000"]
ntm_500000 = config_m["nt_500000"]
#-------------------------------------------------
epsilon_list = config["epsilon_list"]

color_list = sns.color_palette("bright", 8)

fig = plt.figure(figsize = (10, 5))
#fig, (ax,ax_m) = plt.subplots(1, 2, figsize = (4, 3))

#fig, ax = plt.subplots(figsize = (4, 3))
ax = plt.subplot(1,2,1)
ax.set_ylabel("MSE", fontsize = 14)
ax.set_xlabel(r"$\epsilon$", fontsize = 14)
ax.set_xticks(epsilon_list)
ax.tick_params(axis="both", labelsize=13)
ax.set_title("(a) pureDUMP",y=-0.4, fontsize = 20)

l1 = ax.semilogy(epsilon_list,
            n_5000,
            '-',
            color = color_list[3],
            label = "n_5000",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

l3 = ax.semilogy(epsilon_list,
            n_50000,
            '-',
            color = color_list[2],
            label = "n_50000",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

l5 = ax.semilogy(epsilon_list,
            n_500000,
            '-',
            color = color_list[0],
            label = "n_500000",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

l2 = ax.semilogy(epsilon_list,
            nt_5000,
            ':',
            color = color_list[3],
            label = "n_50000(theoretical)",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

l4 = ax.semilogy(epsilon_list,
            nt_50000,
            ':',
            color = color_list[2],
            label = "n_50000(theoretical)",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

l6 = ax.semilogy(epsilon_list,
            nt_500000,
            ':',
            color = color_list[0],
            label = "n_500000(theoretical)",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')
#------------------------mixDUMP---------------------------
ax_m = plt.subplot(1,2,2)
ax_m.set_ylabel("MSE", fontsize = 14)
ax_m.set_xlabel(r"$\epsilon$", fontsize = 14)
ax_m.set_xticks(epsilon_list)
ax_m.tick_params(axis="both", labelsize=13)
ax_m.set_title("(b) mixDUMP",y=-0.4, fontsize = 20)

ax_m.semilogy(epsilon_list,
            nm_5000,
            '-',
            color = color_list[3],
            label = "k_5000(empirical)",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            ntm_5000,
            ':',
            color = color_list[3],
            label = "k_5000(theoretical)",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            nm_50000,
            '-',
            color = color_list[2],
            label = "k_500(empirical)",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            ntm_50000,
            ':',
            color = color_list[2],
            label = "k_500(theoretical)",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            nm_500000,
            '-',
            color = color_list[0],
            label = "k_50(empirical)",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            ntm_500000,
            ':',
            color = color_list[0],
            label = "k_50(theoretical)",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

#ax.legend(fontsize=8.5)
#fig.legend(fontsize=8.5)
#ax.legend(loc='center', bbox_to_anchor=(0.5, 1.07), ncol=3, prop = {'size':6})
legend_list = ['n_5000', 'n_50000', 'n_500000'] 
fig.legend([l1, l2, l3], labels =legend_list, loc='center', bbox_to_anchor=(0.5, 0.92), ncol=3, prop = {'size':14}, frameon = True, edgecolor = 'gray')

fig.tight_layout()
filename = "n_influ"
fig.subplots_adjust(left = 0.067, bottom = 0.252, right = 0.974, top = 0.845, wspace = 0.171, hspace = 0.2)
plt.show()
fig.savefig(os.path.join("./fig_v/kn_influ", filename + ".png"), dpi = 3000)
fig.savefig(os.path.join("./fig_v/eps/kn_influ", filename + ".pdf"), dpi=3000)
 