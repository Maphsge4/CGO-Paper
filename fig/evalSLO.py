import matplotlib.pyplot as plt
import matplotlib as mpl
import tikzplotlib
mpl.rcParams['pdf.fonttype'] = 42  # TrueType 字体 (非 Type-3), 避免乱码
mpl.rcParams['ps.fonttype'] = 42

# OPT + Alpaca
x = ["2", "4", "8", "16", "32", "64", "128"]

sys_tpot = [288.69, 144.34, 93.82, 497.43, 72.172, 36, 19] # √
deepspeed_tpot = [1154, 577.38, 288.7, 144.34, 72.172, 36, 19] # √
flexgen_tpot = [510.2, 279.3, 162.8, 104.16, 74.24, 58.68, 51.54] # √

# Qwen-float32 + Alpaca 少1和2
tpot_sys_qwen = [154.2, 99.13, 98.89, 95.18, 59.27, 39.31, 29.29]  # √
tpot_deepspeed_qwen = [616.8, 326.13, 173.81, 99.007, 59.27, 39.41, 29.29] # √

# Yi-float32 + Alpaca 少1和2
tpot_sys_yi = [390, 195, 97.65, 95.18, 61.48, 43.68, 31.738] # √
tpot_deepspeed_yi = [756, 382, 195, 105.27, 61.48, 43.68, 31.738] # √


# Create figure with four subplots arranged in a 2x2 grid
fig, axes = plt.subplots(1, 6, figsize=(70, 10))


axes[0].plot(
    x,
    sys_tpot,
    marker="o",
    color="green",
    label=r"\sys-TPOT",
    linestyle="-",
    linewidth=2,
)
axes[0].plot(
    x,
    deepspeed_tpot,
    marker="x",
    color="blue",
    label="DeepSpeed-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[0].plot(
    x,
    flexgen_tpot,
    marker="s",
    color="orange",
    label="FlexGen-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[0].set_title("(a) OPT Model on Alpaca", fontsize=25)
axes[0].set_xlabel("Batch Size", fontsize=25)
axes[0].set_ylabel("Latency (ms)", fontsize=25, fontweight="bold")
# axes[0].grid(visible=True, linestyle='--', alpha=0.5)
axes[0].legend(fontsize=25, loc="upper right")
axes[0].tick_params(axis="both", labelsize=25)


axes[1].plot(
    x,
    tpot_sys_qwen,
    marker="o",
    color="green",
    label=r"\sys-TPOT",
    linestyle="-",
    linewidth=2,
)
axes[1].plot(
    x,
    tpot_deepspeed_qwen,
    marker="x",
    color="blue",
    label="DeepSpeed-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[1].set_title("(b) Qwen2 Model on Alpaca", fontsize=25)
axes[1].set_xlabel("Batch Size", fontsize=25)
# axes[1].set_ylabel('Latency (ms)', fontsize=25, fontweight='bold')
# axes[1].grid(visible=True, linestyle='--', alpha=0.5)
# axes[1].legend(fontsize=25)
axes[1].tick_params(axis="both", labelsize=25)


axes[2].plot(
    x,
    tpot_sys_yi,
    marker="o",
    color="green",
    label=r"\sys-TPOT",
    linestyle="-",
    linewidth=2,
)
axes[2].plot(
    x,
    tpot_deepspeed_yi,
    marker="x",
    color="blue",
    label="DeepSpeed-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[2].set_title("(c) Qwen Model on Alpaca", fontsize=25)
axes[2].set_xlabel("Batch Size", fontsize=25)
# axes[2].set_ylabel('Latency (ms)', fontsize=25, fontweight='bold')
# axes[2].grid(visible=True, linestyle='--', alpha=0.5)
# axes[2].legend(fontsize=25)
axes[2].tick_params(axis="both", labelsize=25)

# OPT + LongBench Data
sys_tpot = [0, 89.87, 90.47, 45.83, 23.51, 0, 0]
deepspeed_tpot = [0, 180, 90.47, 45.83, 23.51, 158.54, 0]  # 64√
flexgen_tpot = [1063, 826, 502, 429, 390, 364, 340]

# Qwen + LongBench Data
tpot_deepspeed_qwen = [0, 1040.46, 523.68, 265.3, 136.1, 0, 0]
tpot_sys_qwen = [0, 260.114, 149.6, 94.74, 97.21875, 0, 0]

# Yi-float16 + Alpaca 少1和2
tpot_sys_yi = [0, 260.2, 131.1805, 95.18, 98.25, 0, 0]
tpot_deepspeed_yi = [0, 1041.148, 524.722, 266.509, 137.40, 0, 0]


axes[3].plot(
    x,
    sys_tpot,
    marker="o",
    color="green",
    label=r"\sys-TPOT",
    linestyle="-",
    linewidth=2,
)
axes[3].plot(
    x,
    deepspeed_tpot,
    marker="x",
    color="blue",
    label="DeepSpeed-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[3].plot(
    x,
    flexgen_tpot,
    marker="s",
    color="orange",
    label="FlexGen-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[3].set_title("(d) OPT Model on LongBench", fontsize=25)
axes[3].set_xlabel("Batch Size", fontsize=25)
# axes[3].set_ylabel('Latency (ms)', fontsize=25, fontweight='bold')
# axes[3].grid(visible=True, linestyle='--', alpha=0.5)
# axes[3].legend(fontsize=25)
axes[3].tick_params(axis="both", labelsize=25)


axes[4].plot(
    x,
    tpot_sys_qwen,
    marker="o",
    color="green",
    label=r"\sys-TPOT",
    linestyle="-",
    linewidth=2,
)
axes[4].plot(
    x,
    tpot_deepspeed_qwen,
    marker="x",
    color="blue",
    label="DeepSpeed-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[4].set_title("(e) Qwen2 Model on LongBench", fontsize=25)
axes[4].set_xlabel("Batch Size", fontsize=25)
# axes[4].set_ylabel('Latency (ms)', fontsize=25, fontweight='bold')
# axes[4].grid(visible=True, linestyle='--', alpha=0.5)
# axes[4].legend(fontsize=25)
axes[4].tick_params(axis="both", labelsize=25)

axes[5].plot(
    x,
    tpot_sys_yi,
    marker="o",
    color="green",
    label=r"\sys-TPOT",
    linestyle="-",
    linewidth=2,
)
axes[5].plot(
    x,
    tpot_deepspeed_yi,
    marker="x",
    color="blue",
    label="DeepSpeed-TPOT",
    linestyle=":",
    linewidth=3,
)
axes[5].set_title("(f) Yi Model on LongBench", fontsize=25)
axes[5].set_xlabel("Batch Size", fontsize=25)
# axes[5].set_ylabel('Latency (ms)', fontsize=25, fontweight='bold')
# axes[5].grid(visible=True, linestyle='--', alpha=0.5)
# axes[5].legend(fontsize=25)
axes[5].tick_params(axis="both", labelsize=25)


# Adjust layout
plt.tight_layout()


# Save as TikZ file
output_path = "figures/evalSLO.tex"
tikzplotlib.save(output_path)
# plt.savefig("figures/eval1.pdf", format="pdf", bbox_inches="tight")

