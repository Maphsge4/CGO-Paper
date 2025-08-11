import itertools as it
import os
from plot_fio_comon import *
import subprocess
import sys
import tempfile

root_dir = os.getcwd()

data_dir = os.path.join(root_dir, "data", "driver")
plot_dir = os.path.join(root_dir, "fig")

csv_name = "data_single_overview"
input_csv = os.path.join(data_dir, csv_name + ".csv")

# Baselines
baselines = [posix, iou_dfl, iou_poll, spdk, aeolia]
for idx, base in enumerate(baselines, start=id_start):
    base.id = idx
nr_base = len(baselines)

# Parameters used to filter data rows
iotypes = ["randread", "randwrite"]

iotypes_param = Param("iotype", "")
iodepths_param = Param("iodepth", ["1"])
num_threads_param = Param("numjobs", ["1"])

data_files = []

# Metrics used to filter data columns
metrics = [f"{base.name}_bw" for base in baselines]
metrics += [f"{base.name}_lat_p50" for base in baselines]
metrics += [f"{base.name}_lat_p99" for base in baselines]
metrics += [f"{base.name}_lat_p999" for base in baselines]

iosizes_param = Param("iosize", ["512B", "1K", "2K", "4K", "8K"])   # For small I/O size
for iotype in iotypes:
    output_csv = os.path.join(data_dir, f"tmp_{iotype}_small_" + csv_name + ".csv")
    data_files.append(output_csv)

    iotypes_param.values = iotype
    params = [iotypes_param, iodepths_param, iosizes_param, num_threads_param]

    filter_csv(input_csv, output_csv, params, metrics)

iosizes_param = Param("iosize", ["16K", "64K", "256K", "1M", "2M"])   # For overview
for iotype in iotypes:
    output_csv = os.path.join(data_dir, f"tmp_{iotype}_overview_" + csv_name + ".csv")
    data_files.append(output_csv)

    iotypes_param.values = iotype
    params = [iotypes_param, iodepths_param, iosizes_param, num_threads_param]

    filter_csv(input_csv, output_csv, params, metrics)

env = {
    key: value.format(
        target=target,
    )
    for key, value in base_env.items()
}

# Preset
width = 4.8
height = 9.6
file_name = output_name(__file__)
output = os.path.join(plot_dir, file_name)

# MP Layout
mp_layout = MPLayout(
    mp_startx   =   0.09,
    mp_starty   =   0.026,
    mp_width    =   0.85,
    mp_height   =   0.28,
    mp_rowgap   =   0.047,
    mp_colgap   =   0.1,
    num_rows    =   2,
    num_cols    =   2,
)
mp_layout_dict = asdict(mp_layout)

# Style
border = 3
line_width = 0.5
boxwidth = 1

# Font
font_dict = asdict(font)

# Offset
offset.title_offset="0,-0.6"
offset_dict = asdict(offset)

plot_script = base_preset.format(width=width, height=height, output=output)
plot_script += base_mp_layout.format(**mp_layout_dict)
plot_script += base_style.format(border=border, line_width=line_width, boxwidth=boxwidth)
plot_script += base_font.format(**font_dict)
plot_script += base_offset.format(**offset_dict)

# Fist subplot
plot_script += base_next_plot.format(title=r"(a) small read: p50 latency")
plot_script += """
set key noenhanced right top
set ylabel "P50 Latency (us)"
set yrange [0:]
set ytic 4
"""
plot_script += f"plot \"{data_files[0]}\" \\"
base = baselines[0]
plot_script += base_line_curve.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
    color=base.color,
    pt=base.point_t,
    title=base.title,
)
for base in baselines[1:2]:
    curve = base_line_curve.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
        title=base.title,
    )
    plot_script += "'' \\" + curve
for base in baselines[2:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randread_small_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}:3",
    offset="0,1",
    color="C0",
)
plot_script += "\\" + labels

# Second subplot
plot_script += base_next_plot.format(title=r"(b) small write: p50 latency")
plot_script += """
unset ylabel
set ytic 3
"""
plot_script += f"plot \"{data_files[1]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
    color=base.color,
    pt=base.point_t,
)
for base in baselines[1:2]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
for base in baselines[2:3]:
    curve = base_line_curve.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
        title=base.title,
    )
    plot_script += "'' \\" + curve
for base in baselines[3:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randwrite_small_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}:3",
    offset="0,1",
    color="C0",
)
plot_script += "\\" + labels

# Third subplot
plot_script += base_font.format(**font_dict)
plot_script += base_next_plot.format(title=r"(c) small read: p99 latency")
plot_script += """
set key noenhanced
set ylabel "P99 Latency (us)"
set ytic 4
"""
plot_script += f"plot \"{data_files[0]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
    color=base.color,
    pt=base.point_t,
    title=base.title,
)
for base in baselines[1:3]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
        title=base.title,
    )
    plot_script += "'' \\" + curve
for base in baselines[3:]:
    curve = base_line_curve.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
        title=base.title,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randread_small_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}:3",
    offset="0,1",
    color="C0",
)
plot_script += "\\" + labels

# Fourth subplot
plot_script += base_next_plot.format(title=r"(d) small write: p99 latency")
plot_script += """
unset ylabel
set ytic 4
"""
plot_script += f"plot \"{data_files[1]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
    color=base.color,
    pt=base.point_t,
)
for base in baselines[1:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randwrite_small_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}:3",
    offset="0,1",
    color="C0",
)
plot_script += "\\" + labels

# Fifth subplot
plot_script += base_font.format(**font_dict)
plot_script += base_next_plot.format(title=r"(e) small read: p99.9 latency")
plot_script += """
set key noenhanced
set ylabel "P99.9 Latency (us)"
set ytic 5
"""
plot_script += f"plot \"{data_files[0]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}",
    color=base.color,
    pt=base.point_t,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}",
        color=base.color,
        pt=base.point_t,
        title=base.title,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randread_small_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}:3",
    offset="0,1",
    color="C0",
)
plot_script += "\\" + labels

# Sixth subplot
plot_script += base_next_plot.format(title=r"(f) small write: p99.9 latency")
plot_script += """
unset ylabel
set ytic 5
"""
plot_script += f"plot \"{data_files[1]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}",
    color=base.color,
    pt=base.point_t,
)
for base in baselines[1:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randwrite_small_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}:3",
    offset="0,0.6",
    color="C0",
)
plot_script += "\\" + labels

###############################################################################

# Fist subplot
plot_script += base_font.format(**font_dict)
plot_script += base_next_plot.format(title=r"(g) large read: p50 latency")
plot_script += """
set key noenhanced
set ylabel "P50 Latency (us)"
set ytic 100
"""
plot_script += f"plot \"{data_files[2]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
    color=base.color,
    pt=base.point_t,
    title=base.title,
)
for base in baselines[1:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
        title=base.title,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randread_overview_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}:3",
    offset="-1.5,1",
    color="C0",
)
plot_script += "\\" + labels

# Second subplot
plot_script += base_next_plot.format(title=r"(h) large write: p50 latency")
plot_script += """
unset ylabel
set ytic 150
"""
plot_script += f"plot \"{data_files[3]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
    color=base.color,
    pt=base.point_t,
)
for base in baselines[1:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
plot_script += "\\"
plot_script += """
"data/driver/label_randwrite_overview_data_single_overview.csv" \
"""
base = baselines[2]
labels = base_line_labels.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 1)}:3",
    offset="-1.5,1",
    color="C0",
)
plot_script += "\\" + labels

# Third subplot
plot_script += base_font.format(**font_dict)
plot_script += base_next_plot.format(title=r"(i) large read: p99 latency")
plot_script += """
set key noenhanced
set ylabel "P99 Latency (us)"
set ytic 150
set yrange [0:600]
"""
plot_script += f"plot \"{data_files[2]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
    color=base.color,
    pt=base.point_t,
    title=base.title,
)
for base in baselines[1:2]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
for base in baselines[3:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
# plot_script += "\\"
# plot_script += """
# "data/driver/label_randread_overview_data_single_overview.csv" \
# """
# base = baselines[2]
# labels = base_line_labels.format(
#     entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}:3",
#     offset="-1.5,1",
#     color="C0",
# )
# plot_script += "\\" + labels

# Fourth subplot
plot_script += base_next_plot.format(title=r"(j) large write: p99 latency")
plot_script += """
unset ylabel
"""
plot_script += f"plot \"{data_files[3]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
    color=base.color,
    pt=base.point_t,
)
for base in baselines[1:2]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
for base in baselines[3:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
# plot_script += "\\"
# plot_script += """
# "data/driver/label_randwrite_overview_data_single_overview.csv" \
# """
# base = baselines[2]
# labels = base_line_labels.format(
#     entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}:3",
#     offset="-1.5,1",
#     color="C0",
# )
# plot_script += "\\" + labels

# Fifth subplot
plot_script += base_font.format(**font_dict)
plot_script += base_next_plot.format(title=r"(k) large read: p99.9 latency")
plot_script += """
set key noenhanced
set ylabel "P99.9 Latency (us)"
set xlabel "Throughput (GB/s)"
"""
plot_script += f"plot \"{data_files[2]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}",
    color=base.color,
    pt=base.point_t,
    title=base.title,
)
for base in baselines[1:2]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
for base in baselines[3:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
# plot_script += "\\"
# plot_script += """
# "data/driver/label_randread_overview_data_single_overview.csv" \
# """
# base = baselines[2]
# labels = base_line_labels.format(
#     entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}:3",
#     offset="-1.5,1",
#     color="C0",
# )
# plot_script += "\\" + labels

# Sixth subplot
plot_script += base_next_plot.format(title=r"(l) large write: p99.9 latency")
plot_script += """
unset ylabel
"""
plot_script += f"plot \"{data_files[3]}\" \\"
base = baselines[0]
plot_script += base_line_curve_notitle.format(
    entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}",
    color=base.color,
    pt=base.point_t,
)
for base in baselines[1:2]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
for base in baselines[3:]:
    curve = base_line_curve_notitle.format(
        entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 2)}",
        color=base.color,
        pt=base.point_t,
    )
    plot_script += "'' \\" + curve
# Labels
# plot_script += "\\"
# plot_script += """
# "data/driver/label_randwrite_overview_data_single_overview.csv" \
# """
# base = baselines[2]
# labels = base_line_labels.format(
#     entry=f"{div_1000(base.id)}:{next_col(base.id, nr_base, 3)}:3",
#     offset="-1.5,1",
#     color="C0",
# )
# plot_script += "\\" + labels

with tempfile.NamedTemporaryFile(mode="w+", suffix=".gp") as f:
    f.write(plot_script)
    f.flush()
    subprocess.run(["gnuplot", f.name], env=env)

for file in data_files:
    os.remove(file)
