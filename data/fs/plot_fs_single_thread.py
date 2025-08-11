import itertools as it
import os
from pathlib import Path
from data.plot_common import *
import subprocess
import sys
import tempfile

root_dir = os.getcwd()
plot_dir = os.path.join(root_dir, "fig", "fs")
os.makedirs(plot_dir, exist_ok=True)

###############################################################################
# Data Preparation
baselines = fs_baselines
nr_base = nr_fs_base
id_start = 0
for idx, base in enumerate(baselines, start=id_start):
    base.id = idx

data_dir = os.path.join(root_dir, "data", "fs", "fig1-fio-single-thread")
data_file_names = ["4K_data", "2M_data", "meta_data"]
data_files = data_file_path(data_dir, data_file_names, "csv")

###############################################################################
# Plot Preparation
env = {
    key: value.format(
        target=target,
    )
    for key, value in base_env.items()
}

# Preset
width = 4.8
height = 2.8
file_name = output_name(__file__)
output = os.path.join(plot_dir, file_name)

# MP Layout
mp_layout = MPLayout(
    mp_startx=0.085,
    mp_starty=0.08,
    mp_width=0.84,
    mp_height=0.86,
    mp_rowgap=0.16,
    mp_colgap=0.1,
    num_rows=2,
    num_cols=2,
)
mp_layout_dict = asdict(mp_layout)

# Style
border = 3
line_width = 0.5
boxwidth = 0.75

# Font
font_dict = asdict(font)

# Offset
offset.xtic_offset="0,0.2"
offset_dict = asdict(offset)

plot_script = base_preset.format(root_dir=root_dir, width=width, height=height, output=output)
plot_script += base_mp_layout.format(**mp_layout_dict)
plot_script += base_style.format(border=border, line_width=line_width, boxwidth=boxwidth)
plot_script += base_font.format(**font_dict)
plot_script += base_offset.format(**offset_dict)

plot_script += """
set style fill pattern
"""

off = 0.7
left_base = 1.25
right_base = 0.95

###############################################################################
# First subplot
plot_script += base_next_plot.format(title="(a) 4KB data")
plot_script += """
set boxwidth 0.5 absolute
set xtics noenhanced
set xtics add ('' -5, '' -4, '' -3, 'read' -2, '' -1, '' 0, '' 1, 'write' 2, '' 3, '' 4, '' 5)
set xrange [-5:5]
set ylabel "Throughput (GB/s)"
set yrange [0:6]
set ytic 1.5
unset y2tic
"""

# Left Bar
plot_script += f"plot \"{data_files[0]}\" \\"
base = baselines[0]
plot_script += base_y1_bar.format(
    row=base.id,
    entry=f"{bar_shift(base.id - id_start, nr_base, left_base, off, True)}:2",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_y1_bar.format(
        row=base.id,
        entry=f"{bar_shift(base.id - id_start, nr_base, left_base, off, True)}:2",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Right Bar
for base in baselines:
    curve = base_y1_bar_notitle.format(
        row=base.id + nr_base,
        entry=f"{bar_shift(base.id - id_start, nr_base, right_base, off, False)}:2",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

###############################################################################
# Second subplot
plot_script += base_next_plot.format(title="(b) 2MB data")
plot_script += """
set xtics noenhanced
unset ylabel
set yrange [0:10]
set ytic 2.5
"""
# Left Bar
plot_script += f"plot \"{data_files[1]}\" \\"
base = baselines[0]
plot_script += base_y1_bar_notitle.format(
    row=base.id,
    entry=f"{bar_shift(base.id - id_start, nr_base, left_base, off, True)}:2",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_y1_bar_notitle.format(
        row=base.id,
        entry=f"{bar_shift(base.id - id_start, nr_base, left_base, off, True)}:2",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Right Bar
for base in baselines:
    curve = base_y1_bar_notitle.format(
        row=base.id + nr_base,
        entry=f"{bar_shift(base.id - id_start, nr_base, right_base, off, False)}:2",
        color=base.color,
        pattern=base.pattern,
    )
    plot_script += "'' \\" + curve

###############################################################################
# Third subplot
basic = -1.05

plot_script += base_font.format(**font_dict)

plot_script += base_next_plot.format(title="(c) read metadata")
plot_script += """
set boxwidth 0.5 absolute
set xrange [-5:5]
set xtics noenhanced
set xtics add ('' -5, '' -4, '' -3, '' -2, '' -1, 'open & stat' 0, '' 1, '' 2, '' 3, '' 4, '' 5)
set ylabel "OPS (m)" offset -2,0
set yrange [0:8]
set ytic 2
"""

plot_script += f"plot \"{data_files[2]}\" \\"
base = baselines[0]
plot_script += base_y1_bar_notitle.format(
    row=base.id,
    entry=f"{bar_shift(base.id - id_start, nr_base, basic, off, False)}:2",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_y1_bar_notitle.format(
        row=base.id,
        entry=f"{bar_shift(base.id - id_start, nr_base, basic, off, False)}:2",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

###############################################################################
# Fourth subplot
plot_script += base_next_plot.format(title="(d) write metadata")
plot_script += """
set xrange [-5:5]
set xtics noenhanced
set xtics add ('' -5, '' -4, '' -3, 'create' -2, '' -1, '' 0, '' 1, 'delete' 2, '' 3, '' 4, '' 5)
unset ylabel
set yrange [0:1]
set ytic 0.25
"""
# Left Bar
plot_script += f"plot \"{data_files[2]}\" \\"
base = baselines[0]
plot_script += base_y1_bar_notitle.format(
    row=next_row_g(base.id, nr_base, 1),
    entry=f"{bar_shift(base.id - id_start, nr_base, left_base, off, True)}:2",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_y1_bar_notitle.format(
        row=next_row_g(base.id, nr_base, 1),
        entry=f"{bar_shift(base.id - id_start, nr_base, left_base, off, True)}:2",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Right Bar
for base in baselines:
    curve = base_y1_bar_notitle.format(
        row=next_row_g(base.id, nr_base, 2),
        entry=f"{bar_shift(base.id - id_start, nr_base, right_base, off, False)}:2",
        color=base.color,
        pattern=base.pattern,
    )
    plot_script += "'' \\" + curve

################################################################################
# Execution
with tempfile.NamedTemporaryFile(mode="w+", suffix=".gp") as f:
    f.write(plot_script)
    f.flush()
    subprocess.run(["gnuplot", f.name], env=env)
