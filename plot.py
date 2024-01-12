import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
import yaml

plt.style.use("seaborn-whitegrid")

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="./config/plot/syn_k_50.yml")
args = parser.parse_args()
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

mse_pureDUMP = config["mse_pureDUMP"]
mse_mixDUMP = config["mse_mixDUMP"]
mse_private_shuffle = config["mse_private_shuffle"]
mse_private_coin = config["mse_private_coin"]
mse_public_coin = config["mse_public_coin"]
mse_shuffle_based = config["mse_shuffle_based"]
#mse_laplace = config["mse_laplace"]
mse_solh = config["mse_SOLH"]
#--------------------------------------------------------
mse_pureDUMP1 = config["mse_pureDUMP1"]
mse_mixDUMP1 = config["mse_mixDUMP1"]
mse_private_shuffle1 = config["mse_private_shuffle1"]
mse_private_coin1 = config["mse_private_coin1"]
mse_public_coin1 = config["mse_public_coin1"]
mse_shuffle_based1 = config["mse_shuffle_based1"]
mse_solh1 = config["mse_SOLH1"]
#--------------------------------------------------------
epsilon_list = config["epsilon_list"]
epsilon_liste = epsilon_list.copy()
epsilon_liste.pop(0)
epsilon_liste.pop(0)
#epsilon_liste.pop(0)

epsilon_liste1 = epsilon_liste.copy()
epsilon_liste1.pop(0)
#-------------------------------------------------------
color_list = sns.color_palette("bright", 8)
fig = plt.figure(figsize = (10, 5))

ax = plt.subplot(1,2,1)
ax.set_ylabel("MSE", fontsize = 14)
ax.set_xlabel(r"$\epsilon$", fontsize = 14)
ax.set_xticks(epsilon_list)
ax.tick_params(axis="both", labelsize=13)
ax.set_title(r"(a) $\delta=10^{-6}$",y=-0.4, fontsize = 20)

l1 = ax.semilogy(epsilon_list,
            mse_shuffle_based,
            label = "shuffle_based",
            color = color_list[4],
            # linestyle = "-",
            marker = "d",
            markersize = 8,
            markerfacecolor = 'none')

l2 = ax.semilogy(epsilon_list,
            mse_private_coin,
            label = "private-coin",
            color = color_list[1],
            # linestyle = "-.",
            marker = "s",
            markersize = 8,
            markerfacecolor = 'none')

l3 = ax.semilogy(epsilon_liste,
            mse_public_coin,
            label = "public-coin",
            color = color_list[2],
            # linestyle = "--",
            marker = "^",
            markersize = 8,
            markerfacecolor = 'none')

l4 = ax.semilogy(epsilon_list,
            mse_private_shuffle,
            label = "private-shuffle",
            color = color_list[5],
            # linestyle = ":",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

l5 = ax.semilogy(epsilon_list,
            mse_pureDUMP,
            label = "pureDUMP",
            color = color_list[0],
            # linestyle = "-",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

l6 = ax.semilogy(epsilon_list,
            mse_mixDUMP,
            label = "mixDUMP",
            color = color_list[3],
            # linestyle = "-.",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

l7 = ax.semilogy(epsilon_list,
            mse_solh,
            label = "SOLH",
            color = color_list[6],
            # linestyle = "--",
            marker = "x",
            markersize = 8,
            markerfacecolor = 'none')
#--------------------------------------------------
ax1 = plt.subplot(1,2,2)
ax1.set_ylabel("MSE", fontsize = 14)
ax1.set_xlabel(r"$\epsilon$", fontsize = 14)
ax1.set_xticks(epsilon_list)
ax1.tick_params(axis="both", labelsize=13)
ax1.set_title(r"(b) $\delta=10^{-8}$",y=-0.4, fontsize = 20)

ax1.semilogy(epsilon_list,
            mse_shuffle_based1,
            label = "shuffle_based",
            color = color_list[4],
            # linestyle = "-",
            marker = "d",
            markersize = 8,
            markerfacecolor = 'none')

ax1.semilogy(epsilon_list,
            mse_private_coin1,
            label = "private-coin",
            color = color_list[1],
            # linestyle = "-.",
            marker = "s",
            markersize = 8,
            markerfacecolor = 'none')

ax1.semilogy(epsilon_liste1,
            mse_public_coin1,
            label = "public-coin",
            color = color_list[2],
            # linestyle = "--",
            marker = "^",
            markersize = 8,
            markerfacecolor = 'none')

ax1.semilogy(epsilon_list,
            mse_private_shuffle1,
            label = "private-shuffle",
            color = color_list[5],
            # linestyle = ":",
            marker = "+",
            markersize = 8,
            markerfacecolor = 'none')

ax1.semilogy(epsilon_list,
            mse_pureDUMP1,
            label = "pureDUMP",
            color = color_list[0],
            # linestyle = "-",
            marker = "*",
            markersize = 8,
            markerfacecolor = 'none')

ax1.semilogy(epsilon_list,
            mse_mixDUMP1,
            label = "mixDUMP",
            color = color_list[3],
            # linestyle = "-.",
            marker = "o",
            markersize = 8,
            markerfacecolor = 'none')

ax1.semilogy(epsilon_list,
            mse_solh1,
            label = "SOLH",
            color = color_list[6],
            # linestyle = "--",
            marker = "x",
            markersize = 8,
            markerfacecolor = 'none')
#----------------------------------------------
legend_list = ['shuffle_based', 'private-coin', 'public-coin', 'private-shuffle', 'pureDUMP', 'mixDUMP','SOLH'] 
fig.legend([l1, l2, l3, l4, l5, l6, l7], labels =legend_list, loc='center', bbox_to_anchor=(0.5, 0.92), ncol=4, prop = {'size':14}, frameon = True, edgecolor = 'gray')

fig.tight_layout()
fig.subplots_adjust(left = 0.067, bottom = 0.252, right = 0.974, top = 0.845, wspace = 0.171, hspace = 0.2)
plt.show()
# filename = "k_500_solh"
# fig.savefig(os.path.join("./fig/syn_dataset", filename + ".png"), dpi=3000)
# fig.savefig(os.path.join("./fig/eps", filename + ".pdf"), dpi=3000)
filename = "k_50"
fig.savefig(os.path.join("./fig_v/syn_dataset", filename + ".png"), dpi=3000)
fig.savefig(os.path.join("./fig_v/eps", filename + ".pdf"), dpi=3000)