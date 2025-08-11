import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# Data
batch_sizes = ["2", "4", "8", "16", "32", "64", "128"]
memory_savings_novaserve = [0, 7.77, 7.77, 11.97, 11.97, 0, 0]
memory_savings_flexgen = [0, 4.672, 4.8, 5.05, 5.57, 0, 0]

# Bar width and positions
width = 0.35
x = np.arange(len(batch_sizes))

# Colors and hatches
colors = ["#5DADE2", "#FFD700"]  # 深橙 (NovaServe), 深粉 (FlexGen)
colors2 = ["#d55e00", "#A6206A"]  # Deep orange for NovaServe, Deep pink for FlexGen
hatch_style = "/"  # FlexGen hatch style

# Create figure and subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left plot: Memory usage
axes[0, 0].bar(
    x - width / 2, memory_savings_novaserve, width, label="NovaServe", color=colors[0]
)
axes[0, 0].bar(
    x + width / 2,
    memory_savings_flexgen,
    width,
    label="FlexGen",
    color="white",
    edgecolor=colors[1],
    hatch=hatch_style,
)

axes[0, 0].set_title("(a) Memory Usage on Alpaca", fontsize=16)
axes[0, 0].set_xlabel("Batch Size", fontsize=14)
axes[0, 0].set_ylabel("Memory Usage (GB)", fontsize=14)
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(batch_sizes, fontsize=12)
axes[0, 0].legend(fontsize=12, loc="best", frameon=False)

# Annotate bars
for i, v in enumerate(memory_savings_novaserve):
    axes[0, 0].text(i - 0.2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10)
for i, v in enumerate(memory_savings_flexgen):
    axes[0, 0].text(i + 0.2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10)

# Left plot: Memory usage
axes[0, 1].bar(
    x - width / 2, memory_savings_novaserve, width, label="NovaServe", color=colors[0]
)
axes[0, 1].bar(
    x + width / 2,
    memory_savings_flexgen,
    width,
    label="FlexGen",
    color="white",
    edgecolor=colors[1],
    hatch=hatch_style,
)

axes[0, 1].set_title("(b) Memory Usage on LongBench", fontsize=16)
axes[0, 1].set_xlabel("Batch Size", fontsize=14)
# axes[0, 1].set_ylabel("Memory Usage (GB)", fontsize=14)
axes[0, 1].set_xticks(x)
axes[0, 1].set_xticklabels(batch_sizes, fontsize=12)
axes[0, 1].legend(fontsize=12, loc="best", frameon=False)

# Annotate bars
for i, v in enumerate(memory_savings_novaserve):
    axes[0, 1].text(i - 0.2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10)
for i, v in enumerate(memory_savings_flexgen):
    axes[0, 1].text(i + 0.2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10)



# Adjust layout
plt.tight_layout()
output_path = "figures/evalMemory.tex"
tikzplotlib.save(output_path)

