import matplotlib.pyplot as plt
import tikzplotlib

# 数据
batch_sizes = ['4', '8', '16', '32']
throughput_sys = [51.54, 103, 170, 340]
throughput_deepspeed = [6.26, 12.52, 25, 50]

# 创建柱状图
fig, ax = plt.subplots(figsize=(8, 5))

# 设置柱宽
bar_width = 0.35
x = range(len(batch_sizes))

# Colors
colors = ['#d55e00', '#A6206A']  # Deep orange for NovaServe, Deep pink for FlexGen


# 绘制柱状图
ax.bar(x, throughput_sys, bar_width, label='\\sys', color=colors[0], align='center')
ax.bar([i + bar_width for i in x], throughput_deepspeed, bar_width, label='DeepSpeed', 
       color="white",edgecolor=colors[1], hatch = "/",align='center')

# 设置标题和轴标签
ax.set_title('Throughput Comparison: \\sys vs DeepSpeed', fontsize=16)
ax.set_xlabel('Batch Size', fontsize=12)
ax.set_ylabel('Throughput (tokens/sec)', fontsize=16)
ax.set_xticks([i + bar_width / 2 for i in x])  # 设置横轴刻度位置
ax.set_xticklabels(batch_sizes)  # 设置横轴刻度标签
# ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=14)

# 调整布局
plt.tight_layout()

# 保存为 TikZ 文件
tikzplotlib.save("figures/moti1b.tex")

# 显示图表
plt.show()
