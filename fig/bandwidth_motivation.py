import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib  # 导入 tikzplotlib 库

# 模拟时间
time = np.linspace(0, 10, 50)  # 时间范围（从0到10，减少为50个点）

# 第一张图：Available Bandwidth（随机锯齿波形）
available_bandwidth = 50 + 10 * np.sin(2 * np.pi * 0.25 * time)  # 减小波动频率
available_bandwidth += np.random.normal(0, 5, len(time))  # 添加随机噪声和振幅变化
available_bandwidth = np.clip(available_bandwidth, 30, 80)  # 限制范围

# 第二张图：TPOT（随机锯齿波形，走势相反）
tpot = 90 - (available_bandwidth - 50)  # 反向变化
tpot += np.random.normal(0, 2, len(time))  # 添加噪声
SLO = 95  # SLO值，确保虚线穿过锯齿部分

# 图形设置
fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=False)  # 两张图左右排列，不共享y轴

# 第一张图：Available Bandwidth
axs[0].plot(time, available_bandwidth, color='#4c78a8', linewidth=2)
axs[0].set_ylabel('Available Bandwidth', fontsize=12, labelpad=15)  # 纵轴标题侧边居中，调整labelpad
axs[0].grid(False)  # 完全移除网格线
axs[0].set_xticks([])  # 去掉横坐标具体数值
axs[0].set_yticks([])  # 去掉纵坐标具体数值

# 第二张图：TPOT
axs[1].plot(time, tpot, color='#f58518', linewidth=2, label='TPOT')
axs[1].axhline(SLO, color='#e45756', linestyle='--', linewidth=2, label=f'SLO')
axs[1].set_ylabel('TPOT', fontsize=12, labelpad=15)  # 纵轴标题侧边居中，调整labelpad
axs[1].legend(fontsize=11, loc='upper right')  # 第二张图保留图例
axs[1].grid(False)  # 完全移除网格线
axs[1].set_xticks([])  # 去掉横坐标具体数值
axs[1].set_yticks([])  # 去掉纵坐标具体数值

# 设置横轴标题
for ax in axs:
    ax.set_xlabel('time', fontsize=12, labelpad=10)  # 横轴标题底部居中，调整labelpad

# 美化布局
plt.tight_layout()  # 自动调整布局

# 导出为 TikZ 文件
tikzplotlib.save("figures/bandwidth_tpot_over_time.tex")  # 保存为 TikZ 文件
plt.show()
