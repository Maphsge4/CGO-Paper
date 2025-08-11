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

csv_name = "data_corun_io_io_4_cores"
input_csv = os.path.join(data_dir, csv_name + ".csv")

baselines = [psync, io_uring, spdk, aeolia]
for idx, base in enumerate(baselines, start=id_start):
    base.id = idx

# Parameters used to filter data rows
iotypes_param = Param("iotype", ["randwrite"])
iodepths_param = Param("iodepth", ["1"])
iosizes_param = Param("iosize", ["4K"])
num_threads_param = Param("numjobs", ["1", "2", "4", "8"])

data_files = []

# For p99 latency
output_csv = os.path.join(data_dir, f"tmp_" + csv_name + f"_p99.csv")
data_files.append(output_csv)

params = [iotypes_param, iodepths_param, iosizes_param, num_threads_param]
metrics = [f"{base.name}_lat_p99" for base in baselines]
filter_csv(input_csv, output_csv, params, metrics)

# For throughput
output_csv = os.path.join(data_dir, f"tmp_" + csv_name + f"_bw.csv")
data_files.append(output_csv)

params = [iotypes_param, iodepths_param, iosizes_param, num_threads_param]
metrics = [f"{base.name}_bw" for base in baselines]
filter_csv(input_csv, output_csv, params, metrics)

# For throughput-per-core
output_csv = os.path.join(data_dir, f"tmp_" + csv_name + f"_bw_percore.csv")
data_files.append(output_csv)

params = [iotypes_param, iodepths_param, iosizes_param, num_threads_param]
metrics = [f"{base.name}_bw" for base in baselines]
filter_csv_percore_tp(input_csv, output_csv, params, metrics)

env = {
    key: value.format(
        target=target,
    )
    for key, value in base_env.items()
}

# Preset
width = 9.6
height = 1.8
file_name = output_name(__file__)
output = os.path.join(plot_dir, file_name)

# MP Layout
mp_layout = MPLayout(
    mp_startx=0.045,
    mp_starty=0.14,
    mp_width=0.93,
    mp_height=0.7,
    mp_rowgap=0.05,
    mp_colgap=0.062,
    num_rows=1,
    num_cols=3,
)
mp_layout_dict = asdict(mp_layout)

# Style
border = 3
line_width = 0.5
boxwidth = 0.75

# Font
font_dict = asdict(font)

# Offset
offset.xlabel_offset = "0,0.4"

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

# Fist subplot
plot_script += base_next_plot_notitle
plot_script += """
set key horizontal at 0,305
set xtics noenhanced
set xlabel "# Threads"
set ylabel "P99 Latency (us)"
set yrange [0:]

"""
plot_script += f'plot "{data_files[0]}" \\'
base = baselines[0]
plot_script += base_bar.format(
    entry=f"{base.id}:xtic(4)",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar.format(
        entry=base.id,
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Second subplot
plot_script += base_next_plot_notitle
plot_script += """
set key horizontal at 0,6.100
set xtics noenhanced
set ylabel "Total Throughput (GB/s)"
set ylabel offset "1.5,0"
"""
plot_script += f'plot "{data_files[1]}" \\'
base = baselines[0]
plot_script += base_bar.format(
    entry=f"(${base.id} / 1000):xtic(4)",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar.format(
        entry=f"(${base.id} / 1000)",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

# Third subplot
plot_script += base_next_plot_notitle
plot_script += """
set key horizontal at 0,1.710
set xtics noenhanced
set ylabel "Throughput-per-core (GB/s)"
"""
plot_script += f'plot "{data_files[2]}" \\'
base = baselines[0]
plot_script += base_bar.format(
    entry=f"(${base.id} / 1000):xtic(4)",
    color=base.color,
    pattern=base.pattern,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_bar.format(
        entry=f"(${base.id} / 1000)",
        color=base.color,
        pattern=base.pattern,
        title=base.title,
    )
    plot_script += "'' \\" + curve

with tempfile.NamedTemporaryFile(mode="w+", suffix=".gp") as f:
    f.write(plot_script)
    f.flush()
    subprocess.run(["gnuplot", f.name], env=env)

for file in data_files:
    os.remove(file)
