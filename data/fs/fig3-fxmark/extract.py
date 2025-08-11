import csv
from collections import defaultdict
import itertools as it
import importlib as il
import json
import os
import re
import sys

def nested_defaultdict():
    return defaultdict(lambda: nested_defaultdict())

def parse_filename(filename):
    """
    filename format: nvme_{base_name}_{bench}_bufferedio.json
    """
    parts = filename.split("_")
    n = len(parts)
    base_name = "_".join(parts[1:-2])
    bench = parts[n-2]
    
    return {
        "base_name" : base_name,
        "bench" : bench,
    }

def parse_dat_file(file_path, comment_chars="#!%", delimiter=None):
    rows = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty/commented lines
            if not line or line[0] in comment_chars:
                continue
            
            # Auto-detect delimiter if not specified
            if delimiter is None:
                for test_delim in ['\t', ',', ';', '|', ' ']:
                    if test_delim in line:
                        delimiter = test_delim
                        break
            
            # Split line and clean columns
            columns = [col.strip() for col in re.split(delimiter, line) if col.strip()]
            if columns:  # Only add non-empty rows
                rows.append(columns)
    
    return rows

def process_directory(directory):
    data = nested_defaultdict()

    with os.scandir(directory) as files:
        for file in files:
            if file.is_file():
                file_name = file.name
                if file_name.startswith("nvme_") and file_name.endswith(".dat"):
                    file_path = file.path
                    file_info = parse_filename(file_name)
                    file_data = parse_dat_file(file_path)

                    for row in file_data:
                        key = row[0]
                        val = row[1]
                        data[file_info["bench"]]\
                            [key][file_info["base_name"]] = val
    return data

def write_tables_to_csv(data, output_dir, baselines, benchmarks, keys):
    os.makedirs(output_dir, exist_ok=True)

    headers = ["thread"] + [f"{base}" for base in baselines]

    for bench in benchmarks:
        csv_file = os.path.join(output_dir, f"fxmark_{bench}.csv")

        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key in keys:
                row = [key]
                for base in baselines:

                    row.append(str(data[bench][key][base]))
                writer.writerow(row)

results_dir = os.path.join("data", "fs", "fig3-fxmark")
data_dir = results_dir

baselines = ["ext4", "f2fs", "ufs", "sys"]
benchmarks = ["DWTL", "MRPL", "MRPM", "MRPH", "MRDL", "MRDM", "MWCL", "MWCM", "MWUL", "MWUM", "MWRL", "MWRM"]
keys = ["1", "2", "4", "8", "16", "24", "32", "48", "56", "64"]

data = process_directory(results_dir)
write_tables_to_csv(data, data_dir, baselines, benchmarks, keys)
