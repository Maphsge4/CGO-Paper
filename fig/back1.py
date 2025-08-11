import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib  # 导出 TikZ

# 数据
models = ['Qwen2-72B', 'OPT-66B', 'LLaMA-70B', 'GLM4-32B']
memory_usage = [167, 153, 162, 64]  # 添加 GLM4-32B 数据
HBM_capacity = 80
additional_line = 40  # 第二条参考线位置

# 位置与宽度
x = np.arange(len(models))
width = 0.3

# 自定义颜色和 hatch（深橙、蓝斜线、绿反斜线、黄竖线）
colors = ['#d55e00', '#1f77b4', '#006400', '#FFD700']  # 深橙、蓝、深绿、金黄
hatches = [None, '///', '\\\\\\', '|||']  # 实心、斜线、反斜线、竖线

# 创建图表
fig, ax = plt.subplots(figsize=(9, 5.5))

# 绘制柱状图
bars = []
for i in range(len(models)):
    bar = ax.bar(x[i], memory_usage[i], width,
                 color='white' if hatches[i] else colors[i],  # 有纹理就白底
                 edgecolor=colors[i],
                 hatch=hatches[i],
                 linewidth=1.5)
    bars.append(bar)

# 添加 HBM 线和 40G 线
ax.axhline(HBM_capacity, color='gray', linestyle='--', linewidth=1.5, label='HBM Capacity (80 GB)')
ax.axhline(additional_line, color='black', linestyle='dotted', linewidth=1.2, label='Offloading Threshold (40 GB)')

# 轴标签与刻度
ax.set_xlabel('Models', fontsize=16)
ax.set_ylabel('Memory Usage (GB)', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=14)

# 美化边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1)
ax.spines['bottom'].set_linewidth(1)

# Y轴范围
ax.set_ylim(0, max(memory_usage) + 30)

# 图例
ax.legend(loc='upper right', fontsize=11, frameon=False)

# 布局优化
plt.tight_layout()

# 导出 TikZ
tikzplotlib.save("figures/back1_extended.tex")

# 显示图
plt.show()
