import matplotlib.pyplot as plt
import tikzplotlib

# 左图数据 (sequence length=512)
batch_sizes = [2, 4, 8, 16, 32, 64]
latenct_actual_left = [32.85, 36.17, 42.91, 56.72, 83.74, 136.7]
latenct_estimated_left = [16.41, 18.091, 21.79, 30.277, 49.604, 84.493]

# 右图数据 (batch size=16)
sequence_lengths = [64, 128, 256, 512, 1024]
latenct_actual_right = [33.04, 36.06, 42.54, 56.72, 87.42]
latenct_estimated_right = [17.043, 18.709, 21.87, 29.08, 49.196]


# 创建画布
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# 左图: sequence length = 512
axes[0].plot(batch_sizes, latenct_estimated_left, marker='o', linestyle='--', color='blue', label='Estimated')
axes[0].plot(batch_sizes, latenct_actual_left, marker='^', linestyle='-', color='green', label='Actual')
axes[0].set_title('(a) Sequence Length = 512', fontsize=14)
axes[0].set_xlabel('Batch Size', fontsize=12)
axes[0].set_ylabel('Latency (ms)', fontsize=12)
axes[0].set_xticks(batch_sizes)  # 设置横坐标刻度
axes[0].grid(True, linestyle='--', alpha=0.6)
axes[0].legend(fontsize=10)

# 右图: batch size = 16
axes[1].plot(sequence_lengths, latenct_estimated_right, marker='o', linestyle='--', color='blue', label='Estimated')
axes[1].plot(sequence_lengths, latenct_actual_right, marker='^', linestyle='-', color='green', label='Actual')
axes[1].set_title('(b) Batch Size = 16', fontsize=14)
axes[1].set_xlabel('Sequence Length', fontsize=12)
axes[1].set_ylabel('Latency (ms)', fontsize=12)
axes[1].set_xticks(sequence_lengths)  # 设置横坐标刻度
axes[1].grid(True, linestyle='--', alpha=0.6)
axes[1].legend(fontsize=10)


# 调整布局
plt.tight_layout()

# 保存为 TikZ 文件
tikzplotlib.save("figures/moti2.tex")

# 显示图表
plt.show()