import matplotlib.pyplot as plt
import tikzplotlib

# 数据
batch_sizes = ["4", "8", "16", "32", "64", "128"]  # 横轴为类别型标签
opt_tpot = [88.1, 44.066, 27.8875, 20.9, 10.46, 10.37]  # OPT-13B 的 TPOT
qwen_tpot = [87.5, 43.5, 27.5, 20.5, 10.8, 10.6]  # LLaMA-13B 的 TPOT
GLM4_tpot = [86.5, 42.5, 25.5, 18.5, 9.8, 9.6]  # LLaMA-13B 的 TPOT

# 左图：OPT-13B
fig, ax1 = plt.subplots(figsize=(7, 4))  # 调整图形大小
ax1.plot(batch_sizes, opt_tpot, marker='o', linestyle='-', color='blue', label='OPT')
ax1.plot(batch_sizes, qwen_tpot, marker='^', linestyle='-', color='green', label='Qwen2')
ax1.plot(batch_sizes, GLM4_tpot, marker='x', linestyle='-', color='orange', label='GLM-4')
ax1.set_title('Larger Model', fontsize=12)
ax1.set_xlabel('Batch Size', fontsize=12)
ax1.set_ylabel('TPOT (ms)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(fontsize=10)
# 布局优化
plt.tight_layout()

# 导出 TikZ
tikzplotlib.save("figures/eval3.tex")

# 显示图
plt.show()
