import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# Data
x = [2, 3, 4, 5, 6, 7, 8]
y = [20080, 15440, 13904, 12352, 11584, 10816, 10816]
horizontal_value = 9376

# FlexGen (random data generated for demonstration purposes)
flexgen_y = [0.8 * value for value in y]  # 80% of the original values

# DeepSpeed horizontal line value (a very large number)
deepspeed_value = 25000

# Create figure and axes for two subplots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Plot for the first graph
ax1.plot(
    x, y, marker="o", linestyle="-", color="#1f77b4", label="Original"
)  # Line plot with deep blue
ax1.plot(
    x, flexgen_y, marker="^", linestyle="-", color="#ff7f0e", label="FlexGen"
)  # FlexGen curve
ax1.axhline(
    y=deepspeed_value, color="#2ca02c", linestyle="--", label="DeepSpeed"
)  # DeepSpeed horizontal line
ax1.axhline(
    y=horizontal_value, color="red", linestyle="--", label="Naive"
)  # DeepSpeed horizontal line
ax1.set_title("Qwen2 Model", fontsize=12)
ax1.set_xlabel("Interval", fontsize=12)
ax1.set_ylabel("Max Length", fontsize=12)
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend(fontsize=10)

# Plot for the second graph
ax2.plot(
    x, y, marker="o", linestyle="-", color="#1f77b4", label="Original"
)  # Line plot with deep blue
ax2.plot(
    x, flexgen_y, marker="^", linestyle="-", color="#ff7f0e", label="FlexGen"
)  # FlexGen curve
ax2.axhline(
    y=deepspeed_value, color="#2ca02c", linestyle="--", label="DeepSpeed"
)  # DeepSpeed horizontal line
ax2.axhline(
    y=horizontal_value, color="red", linestyle="--", label="Naive"
)  # DeepSpeed horizontal line
ax2.set_title("GLM-4 Model", fontsize=12)
ax2.set_xlabel("Interval", fontsize=12)
ax2.set_ylabel("Max Length", fontsize=12)
ax2.grid(True, linestyle="--", alpha=0.2)
ax2.legend(fontsize=10)

# Layout adjustment for better appearance
plt.tight_layout()

# Save the plot as a TikZ file
output_path = "figures/eval4.tex"
tikzplotlib.save(output_path)

print(f"TikZ file has been saved to {output_path}")

# Show the plot
plt.show()
