import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# Data
batch_sizes = ["GPU:0", "GPU:1"]
nova_serve_opt = [76.99, 39.91]
nova_serve_qwen = [81.756375, 40.63]
nova_serve_yi = [82.5, 42.5]  # mock
flex_gen_opt = [114.75, 100.43]

# New data
# nova_serve_qwen = [84.5, 43.5, 21.75]  # Example data for NovaServe-Qwen
# flex_gen_qwen = [123.3, 105.0, 60.0]  # Example data for FlexGen-Qwen
# flex_gen_GLM = [110.2, 95.0, 55.0]  # Example data for FlexGen-GLM

# Positions
x = np.arange(len(batch_sizes))
width = 0.28  # Adjust width to accommodate more bars

# Color and hatch setup
colors = [
    "#d55e00",
    "#1f77b4",
    "#006400",
    "#FF8C00",
    "#800080",
    "#00BFFF",
]  # Deep orange, blue, deep green, etc.
hatches = [
    None,
    "/",
    "|",
    "+",
    "x",
    "*",
]  # No hatch, diagonal, backslash, plus, cross, star

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 6))  # Increase the width of the plot

# Plot bars
ax.bar(x - width, nova_serve_opt, width, label="NovaServe-OPT", color=colors[0])
ax.bar(
    x,
    nova_serve_qwen,
    width,
    label="NovaServe-Qwen",
    color="white",
    edgecolor=colors[3],
    hatch=hatches[3],
    linewidth=1.5,
)
ax.bar(x - width, 
       nova_serve_yi, width, 
       label='NovaServe-yi', 
       color="white", 
       edgecolor=colors[1], hatch=hatches[1], linewidth=1.5)
ax.bar(
    x + width,
    flex_gen_opt,
    width,
    label="FlexGen-OPT",
    color="white",
    edgecolor=colors[2],
    hatch=hatches[2],
    linewidth=1.5,
)
# ax.bar(x + 2*width, flex_gen_qwen, width, label='FlexGen-Qwen', color="white", edgecolor=colors[4], hatch=hatches[4], linewidth=1.5)
# ax.bar(x + 3*width, flex_gen_GLM, width, label='FlexGen-GLM', color="white", edgecolor=colors[5], hatch=hatches[5], linewidth=1.5)

# SLO line
slo_value = 100
ax.axhline(y=slo_value, color="gray", linestyle="--", linewidth=1)

# Axis labels and ticks
ax.set_xlabel("Batch Size", fontsize=14)
ax.set_ylabel("TPOT (ms)", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(batch_sizes, fontsize=12)

# Legend on top
ax.legend(
    fontsize=10, loc="upper center", bbox_to_anchor=(0.5, 1.2), frameon=False, ncol=3
)

# Layout
fig.tight_layout()

# Save as TikZ
output_path = "figures/evalbandwidth.tex"
tikzplotlib.save(
    output_path,
    axis_width="14cm",  # 横轴宽度加长
    axis_height="6cm",  # 保持纵轴高度不变
)

print(f"TikZ file has been saved to {output_path}")
