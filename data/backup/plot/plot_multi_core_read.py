import itertools as it
import os
from pathlib import Path
from plot_fio_comon import *
import subprocess
import sys
import tempfile

root_dir = os.getcwd()

data_dir = os.path.join(root_dir, "data", "driver")
plot_dir = os.path.join(root_dir, "fig")

csv_name = "data_multi_cores"
input_csv = os.path.join(data_dir, csv_name + ".csv")

baselines = [iou_dfl, posix, aeolia, iou_poll, spdk]
# baselines = [io_uring, psync, spdk]
for idx, base in enumerate(baselines, start=id_start):
    base.id = idx
nr_base = len(baselines)

# Parameters used to filter data rows
iotypes_param = Param("iotype", ["randread"])
iodepths_param = Param("iodepth", ["1"])
iosizes_param = Param("iosize", ["4K"])
num_cpus_param = Param("numcpu", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

data_files = []

# For P99.9 latency
output_csv = os.path.join(data_dir, f"tmp_" + csv_name + f"_p999.csv")
data_files.append(output_csv)

params = [iotypes_param, iodepths_param, iosizes_param, num_cpus_param]
# Metrics used to filter data columns
metrics = [f"{base.name}_lat_p50" for base in baselines]
metrics += [f"{base.name}_lat_p99" for base in baselines]
metrics += [f"{base.name}_lat_p999" for base in baselines]
filter_csv_multicore(input_csv, output_csv, params, metrics)

# For throughput
output_csv = os.path.join(data_dir, f"tmp_" + csv_name + f"_bw.csv")
data_files.append(output_csv)

params = [iotypes_param, iodepths_param, iosizes_param, num_cpus_param]
metrics = [f"{base.name}_bw" for base in baselines]
filter_csv_multicore(input_csv, output_csv, params, metrics)

# For throughput-per-core
output_csv = os.path.join(data_dir, f"tmp_" + csv_name + f"_bw_percore.csv")
data_files.append(output_csv)

params = [iotypes_param, iodepths_param, iosizes_param, num_cpus_param]
metrics = [f"{base.name}_bw" for base in baselines]
filter_csv_percore_tp_multicore(input_csv, output_csv, params, metrics)

env = {
    key: value.format(
        target=target,
    )
    for key, value in base_env.items()
}

# Preset
width = 4.8
height = 4.8
file_name = output_name(__file__)
output = os.path.join(plot_dir, file_name)

# MP Layout
mp_layout = MPLayout(
    mp_startx=0.075,
    mp_starty=0.04,
    mp_width=0.87,
    mp_height=0.4,
    mp_rowgap=0.092,
    mp_colgap=0.05,
    num_rows=2,
    num_cols=1,
)
mp_layout_dict = asdict(mp_layout)

# Style
border = 3
line_width = 0.5
boxwidth = 0.658

# Font
font_dict = asdict(font)

# Offset
offset.xlabel_offset="0,0.4"
offset.title_offset="0,-0.6"
offset_dict = asdict(offset)

plot_script = base_preset.format(
    root_dir=root_dir, width=width, height=height, output=output
)
plot_script += base_mp_layout.format(**mp_layout_dict)
plot_script += base_style.format(
    border=border, line_width=line_width, boxwidth=boxwidth
)
plot_script += base_font.format(**font_dict)
plot_script += base_offset.format(**offset_dict)

plot_script += """
set style data histogram
set style histogram clustered
set style fill pattern
"""

# First subplot
plot_script += base_next_plot.format(title=r"(a) p50 latency")
plot_script += """
set key right top maxrows 1
set xtics noenhanced
set ylabel "P50 Latency (us)"
set yrange [0:80]
set ytic 20
"""
plot_script += f'plot "{data_files[0]}" \\'
base = baselines[0]
plot_script += base_bar.format(
    entry=f"(${base.id}):xtic(4)",
    color=base.color,
    pattern=3,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar.format(
        entry=f"(${base.id})",
        color=base.color,
        pattern=3,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Second subplot
plot_script += base_next_plot.format(title=r"(b) p99 latency")
plot_script += """
set xtics noenhanced
set ylabel "P99 Latency (us)" offset 1,0
set yrange [0:128]
set ytic 32
"""
plot_script += f'plot "{data_files[0]}" \\'
base = baselines[0]
plot_script += base_bar_notitle.format(
    entry=f"{next_col(base.id, nr_base, 1)}:xtic(4)",
    color=base.color,
    pattern=3,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar_notitle.format(
        entry=next_col(base.id, nr_base, 1),
        color=base.color,
        pattern=3,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Third subplot
plot_script += base_next_plot.format(title=r"(c) p99.9 latency")
plot_script += """
set xtics noenhanced
set ylabel "P99.9 Latency (ms)" offset 2,0
set yrange [0:50]
set ytic 12.5
"""
plot_script += f'plot "{data_files[0]}" \\'
base = baselines[0]
plot_script += base_bar_notitle.format(
    entry=f"{div_1000(next_col(base.id, nr_base, 2))}:xtic(4)",
    color=base.color,
    pattern=3,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar_notitle.format(
        entry=div_1000(next_col(base.id, nr_base, 2)),
        color=base.color,
        pattern=3,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Fourth subplot
plot_script += base_next_plot.format(title=r"(d) throughput")
plot_script += """
set xtics noenhanced
set xlabel "# cores"
set ylabel "Total Throughput (GB/s)" offset 1,0
set yrange [0:6.1]
set ytic 1.5
"""
plot_script += f'plot "{data_files[1]}" \\'
base = baselines[0]
plot_script += base_bar_notitle.format(
    entry=f"(${base.id} / 1000):xtic(4)",
    color=base.color,
    pattern=3,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar_notitle.format(
        entry=f"(${base.id} / 1000)",
        color=base.color,
        pattern=3,
        title=base.title,
    )
    plot_script += "'' \\" + curve

with tempfile.NamedTemporaryFile(mode="w+", suffix=".gp") as f:
    f.write(plot_script)
    f.flush()
    subprocess.run(["gnuplot", f.name], env=env)

for file in data_files:
    os.remove(file)
