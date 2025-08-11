import itertools as it
import os
from pathlib import Path
from data.plot_common import *
import subprocess
import sys
import tempfile

root_dir = os.getcwd()

data_dir = os.path.join(root_dir, "data", "fs")
plot_dir = os.path.join(root_dir, "fig", "fs")

csv_name = "data_fs_breakdown"
input_csv = os.path.join(data_dir, csv_name + ".csv")

baselines = [ext4, posix, iou_opt, aeofs, iou_poll]
for idx, base in enumerate(baselines, start=0):
    base.id = idx
titles = ["ext4", "aeofs+ksched+kintr", "aeofs+ksched+uintr", "aeofs+aeosched+uintr", "aeofs+poll"]

env = {
    key: value.format(
        target=target,
    )
    for key, value in base_env.items()
}

# Preset
width = 2.4
height = 1.2
file_name = output_name(__file__)
output = os.path.join(plot_dir, file_name)

# MP Layout
mp_layout = MPLayout(
    mp_startx   =   0.14,
    mp_starty   =   0.04,
    mp_width    =   0.8,
    mp_height   =   0.92,
    mp_rowgap   =   0.05,
    mp_colgap   =   0.1,
    num_rows    =   1,
    num_cols    =   1,
)
mp_layout_dict = asdict(mp_layout)

# Style
border = 3
line_width = 0.5
boxwidth = 0.8

# Font
font_dict = asdict(font)

# Offset
offset.xtic_offset = "-2,0.2"
offset.ylabel_offset = "1.5,0"
offset_dict = asdict(offset)

plot_script = base_preset.format(root_dir=root_dir, width=width, height=height, output=output)
plot_script += base_mp_layout.format(**mp_layout_dict)
plot_script += base_style.format(border=border, line_width=line_width, boxwidth=boxwidth)
plot_script += base_font.format(**font_dict)
plot_script += base_offset.format(**offset_dict)

plot_script += """
set style fill pattern
"""

off = 0.5

# First subplot
plot_script += base_next_plot_notitle
plot_script += """
set key reverse spacing 1.6 at 2.2,1.6 maxcolumns 1 noenhanced
set boxwidth 0.2 absolute
set xtics rotate by -45
set xtics add ('' -0.5, '' 0, '' 0.5, '' 1, '' 1.5, '' 2, '' 2.5, '' 3, ''3.5)
set xrange [-0.5:3.5]
set ylabel "Throughput (GB/s)"
set yrange [0:1.6]
set ytic 0.4
"""
# set xtics add ('' -0.5, 'ext4' 0, 'aeolia^{1}' 0.5, 'aeolia^{2}' 1, 'aeolia' 1.5, 'aeolia^{3}' 2, '' 2.5, '' 3)

plot_script += """
set label "ext4" at 2.58,1.485 font "Times New Roman,12"
set label "+k\\\_intr" at 2.58,1.17 font "Times New Roman,12"
set label "+k\\\_yield" at 2.58,0.88 font "Times New Roman,12"
set label "aeolia" at 2.58,0.61 font "Times New Roman,12"
set label "+poll" at 2.58,0.3 font "Times New Roman,12"
"""

plot_script += f"plot \"{input_csv}\" \\"
base = baselines[0]
plot_script += base_y1_bar.format(
    row=base.id,
    entry=f"($0 + {base.id} * {off}):2",
    color=base.color,
    pattern=base.pattern,
    title=" ",
)
for base in baselines[1:]:
    curve = base_y1_bar.format(
        row=base.id,
        entry=f"($0 + {base.id} * {off}):2",
        color=base.color,
        pattern=base.pattern,
        title=" ",
    )
    plot_script += "'' \\" + curve
plot_script += "'' "
labels = base_line_labels.format(
    entry="3:2:2",
    offset="0,0.5",
    color="C0",
)
plot_script += "\\" + labels

with tempfile.NamedTemporaryFile(mode="w+", suffix=".gp") as f:
    f.write(plot_script)
    f.flush()
    subprocess.run(["gnuplot", f.name], env=env)
