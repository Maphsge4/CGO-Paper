import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# Batch sizes
batch_sizes = ['4', '8', '16', '32', '64']
x = np.arange(len(batch_sizes))
width = 0.3

# Filled-in data
memory_savings_novaserve = [6.1, 7.77, 9.5, 11.97, 13.8]
memory_savings_flexgen   = [3.5, 4.8, 5.1, 5.57, 6.2]

throughput_novaserve = [15.2, 21.97, 39.6, 57.14, 72.5]
throughput_flexgen   = [6.8, 11.85, 28.3, 35.46, 45.7]

# Colors
colors = ['#5DADE2', '#FFD700']  # 深橙 (NovaServe), 深粉 (FlexGen)
colors2 = ['#d55e00', '#A6206A']  # Deep orange for NovaServe, Deep pink for FlexGen

# Create figure and subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left plot: GPU Memory Savings
axes[0].bar(x - width/2, memory_savings_novaserve, width, label='NovaServe', color=colors[0])
axes[0].bar(x + width/2, memory_savings_flexgen, width, label='FlexGen', 
            color="white", edgecolor=colors[1], hatch="x")
axes[0].set_title('(a) Memory Usage on Offloading Devices', fontsize=16)
axes[0].set_xlabel('Batch Size', fontsize=14)
axes[0].set_ylabel('Memory Usage (GB)', fontsize=14)
axes[0].set_xticks(x)
axes[0].set_xticklabels(batch_sizes, fontsize=12)
axes[0].legend()

# Annotate bars for the left plot
for i, v in enumerate(memory_savings_novaserve):
    axes[0].text(i - 0.2, v + 0.2, f'{v:.2f}', ha='center', fontsize=10)
for i, v in enumerate(memory_savings_flexgen):
    axes[0].text(i + 0.2, v + 0.2, f'{v:.2f}', ha='center', fontsize=10)

# Right plot: Throughput Comparison
axes[1].bar(x - width/2, throughput_novaserve, width, label='NovaServe', color=colors2[0])
axes[1].bar(x + width/2, throughput_flexgen, width, label='FlexGen', 
            edgecolor=colors2[1], color="white", hatch="/")
axes[1].set_title('(b) Throughput Comparison', fontsize=16)
axes[1].set_xlabel('Batch Size', fontsize=14)
axes[1].set_ylabel('Throughput (tokens/s)', fontsize=14)
axes[1].set_xticks(x)
axes[1].set_xticklabels(batch_sizes, fontsize=12)
axes[1].legend()

# Annotate bars for the right plot
for i, v in enumerate(throughput_novaserve):
    axes[1].text(i - 0.2, v + 2, f'{v:.2f}', ha='center', fontsize=10)
for i, v in enumerate(throughput_flexgen):
    axes[1].text(i + 0.2, v + 2, f'{v:.2f}', ha='center', fontsize=10)

# Adjust layout
fig.tight_layout()

# Save as TikZ file
output_path = "figures/moti2b.tex"
tikzplotlib.save(output_path)