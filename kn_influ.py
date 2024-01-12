import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yaml

plt.style.use("seaborn-whitegrid")

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="./config/kn_influ/pureDUMP_k.yml")
args = parser.parse_args()
with open(args.config, "r") as f:
    config = yaml.safe_load(f)
#-----------------------mixDUMP-------------------
parser = argparse.ArgumentParser()
parser.add_argument("--config_m", default="./config/kn_influ/mixDUMP_k.yml")
args = parser.parse_args()
with open(args.config_m, "r") as f_m:
    config_m = yaml.safe_load(f_m)
#------------------------------------------------
k_50 = config["k_50"]
k_500 = config["k_500"]
k_5000 = config["k_5000"]

kt_50 = config["kt_50"]
kt_500 = config["kt_500"]
kt_5000 = config["kt_5000"]
#--------------------mixDUMP----------------------
km_50 = config_m["k_50"]
km_500 = config_m["k_500"]
km_5000 = config_m["k_5000"]

ktm_50 = config_m["kt_50"]
ktm_500 = config_m["kt_500"]
ktm_5000 = config_m["kt_5000"]
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
            k_5000,
            '-',
            color = color_list[3],
            label = "k_5000",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

l2 = ax.semilogy(epsilon_list,
            k_500,
            '-',
            color = color_list[2],
            label = "k_500",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

l3 = ax.semilogy(epsilon_list,
            k_5000,
            '-',
            color = color_list[0],
            label = "k_50",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

l4 = ax.semilogy(epsilon_list,
            kt_5000,
            ':',
            color = color_list[3],
            label = "k_5000(theoretical)",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

l5 = ax.semilogy(epsilon_list,
            kt_500,
            ':',
            color = color_list[2],
            label = "k_500(theoretical)",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

l6 = ax.semilogy(epsilon_list,
            kt_5000,
            ':',
            color = color_list[0],
            label = "k_50(theoretical)",
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
            km_5000,
            '-',
            color = color_list[3],
            label = "k_5000(empirical)",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            ktm_5000,
            ':',
            color = color_list[3],
            label = "k_5000(theoretical)",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            km_500,
            '-',
            color = color_list[2],
            label = "k_500(empirical)",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            ktm_500,
            ':',
            color = color_list[2],
            label = "k_500(theoretical)",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            km_50,
            '-',
            color = color_list[0],
            label = "k_50(empirical)",
            markersize = 8,
            markerfacecolor = 'none')

ax_m.semilogy(epsilon_list,
            ktm_50,
            ':',
            color = color_list[0],
            label = "k_50(theoretical)",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

#ax.legend(fontsize=8.5)
#fig.legend(fontsize=8.5)
#ax.legend(loc='center', bbox_to_anchor=(0.5, 1.07), ncol=3, prop = {'size':6})
legend_list = ['k_5000', 'k_500', 'k_50'] 
fig.legend([l1, l2, l3], labels =legend_list, loc='center', bbox_to_anchor=(0.5, 0.92), ncol=3, prop = {'size':14}, frameon = True, edgecolor = 'gray')

fig.tight_layout()
filename = "k_influ"
fig.subplots_adjust(left = 0.067, bottom = 0.252, right = 0.974, top = 0.845, wspace = 0.171, hspace = 0.2)
plt.show()
fig.savefig(os.path.join("./fig_v/kn_influ", filename + ".png"), dpi = 3000)
fig.savefig(os.path.join("./fig_v/eps/kn_influ", filename + ".pdf"), dpi=3000)
