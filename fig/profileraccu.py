import matplotlib.pyplot as plt
import tikzplotlib
import numpy as np

# 数据
x1 = ["2", "3", "4", "5"]
y1 = [342.42, 229.157, 223.35, 210.9]
y11 = [342.42, 229.157, 223.35, 210.9]
y111 = [342.42, 229.157, 223.35, 210.9]
slo1 = 300.9
x11 = np.arange(len(x1))

x2 = ["5", "6", "8", "10"]
y2 = [123.93, 115.03, 89.388, 68.17]
y22 = [123.93, 115.03, 89.388, 68.17]
y222 = [123.93, 115.03, 89.388, 68.17]
slo2 = 90
x22 = np.arange(len(x2))

x3 = ["2", "3", "4", "5", "6", "8", "10"]
y3 = [11.5, 15.8, 17.25, 18.69, 21.125, 21.5, 21.875]
y33 = [11.5, 15.8, 17.25, 18.69, 21.125, 21.5, 21.875]
y333 = [11.5, 15.8, 17.25, 18.69, 21.125, 21.5, 21.875]
x33 = np.arange(len(x3))

# 配色
colors = {
    "ttft": "#1f77b4",  # 蓝色
    "tpot": "#2ca02c",  # 绿色
    "memory": "#ff7f0e",  # 橙色
    "slo": "#d62728",  # 红色
}

# 创建子图
fig, axs = plt.subplots(1, 2, figsize=(12, 10))


bar_width = 0.35
group_gap = bar_width / 2  # 每组柱之间的空隙

# 修正 x 轴位置，基于每组数量和间隔，确保柱子不重叠
x22 = np.arange(len(x2)) * (1 + group_gap)
x33 = np.arange(len(x3)) * (1 + group_gap)

# -- TPOT 图 --
axs[0].bar(x22 - bar_width / 2, y2, color=colors["ttft"], label="OPT", width=bar_width)
axs[0].bar(x22 + bar_width / 2, y22, color="white", edgecolor=colors["tpot"], label="Qwen2", width=bar_width, hatch="/")
axs[0].axhline(slo2, color=colors["slo"], linestyle="--", label="SLO")

axs[0].set_xlabel("Interval Configuration")
axs[0].set_ylabel("TPOT")
axs[0].set_xticks(x22)
axs[0].set_xticklabels(x2, fontsize=12)
axs[0].set_title("(a) TPOT Analysis")
axs[0].legend()

# -- Memory Usage 图 --
axs[1].bar(x33 - bar_width / 2, y3, color=colors["ttft"], label="OPT", width=bar_width)
axs[1].bar(x33 + bar_width / 2, y33, color="white", edgecolor=colors["tpot"], label="Qwen2", width=bar_width, hatch="/")

axs[1].set_xlabel("Configuration")
axs[1].set_ylabel("Memory Usage (GB)")
axs[1].set_xticks(x33)
axs[1].set_xticklabels(x3, fontsize=12)
axs[1].set_title("(b) Memory Usage Analysis")
axs[1].legend()


# 调整布局
plt.tight_layout()

# 保存 TikZ 文件
tikzplotlib.save("figures/profileraccu.tex")
plt.show()
