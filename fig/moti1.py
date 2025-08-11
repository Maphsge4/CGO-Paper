import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# 图 1
models = ["Qwen2-beta-7B", "OPT-13B", "LLaMA-13B"]
P_values = [1.33, 1.20, 1.59]
D_values = [7.43, 6.80, 7.06]
C_values = [0.88, 0.95, 1.01]  # Chunked Prefill

x1 = np.arange(len(models))
width1 = 0.25

# 图 2
groups = ["Prefill", "Decode", "Chunked Prefill"]
compute_values = [5.268, 1.312, 0.974]
transfer_values = [18.128, 18.128, 18.128]

x2 = np.arange(len(groups))
width2 = 0.2

fig = plt.figure(figsize=(8, 3))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.7])

# 图1
axs0 = fig.add_subplot(gs[0])
colors1 = ['#5DADE2', '#FFD700', '#006400']  # 天蓝，深黄，深绿
axs0.bar(x1 - width1, P_values, width1, label="Prefill", color=colors1[0])
axs0.bar(x1, D_values, width1, label="Decode", color="white", edgecolor=colors1[1], hatch="/")
axs0.bar(x1 + width1, C_values, width1, label="Chunked Prefill", color="white", edgecolor=colors1[2], hatch="|")
axs0.set_ylabel("Ratio of Latency to SLO.", fontsize=14, fontweight="bold")
axs0.set_title("(a) Prefill vs Decode vs Chunked Prefill", fontsize=16, fontweight="bold")
axs0.set_xticks(x1)
axs0.set_xticklabels(models)
axs0.legend(
    fontsize=12,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.05),
    ncol=3,
    frameon=False
)
axs0.set_box_aspect(0.5)

# 图2
axs1 = fig.add_subplot(gs[1])
colors2 = ['#d55e00', '#6a3d9a']  # 深橙和深紫
axs1.bar(x2 - width2 / 2, compute_values, width2, label="Compute", color=colors2[0])
axs1.bar(
    x2 + width2 / 2, transfer_values, width2, label="Transfer",
    color="white", edgecolor=colors2[1], hatch="x"
)
axs1.set_ylabel("Latency (ms)", fontsize=14, fontweight="bold")
axs1.set_title("(b) Compute vs Transfer", fontsize=16, fontweight="bold")
axs1.set_xticks(x2)
axs1.set_xticklabels(groups)
axs1.legend(
    fontsize=12,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.05),
    ncol=2,
    frameon=False
)
axs1.set_box_aspect(1.5)

plt.subplots_adjust(wspace=0.4)
tikzplotlib.save("figures/moti1.tex")
plt.show()
