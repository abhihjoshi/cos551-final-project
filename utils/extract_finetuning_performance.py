# Author: Colin Wang

from glob import glob
import re
import numpy as np
import os

def extract_metrics(file):
    task_perf = {}
    d_model = None
    n_layer = None
    bed_file = None
    fasta_file = None
    curr_bench = None

    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'd_model' in line:
                match = re.search(r'd_model:\s*(\d+)', line)
                if match:
                    d_model = int(match.group(1))
            elif 'n_layer' in line:
                match = re.search(r'n_layer:\s*(\d+)', line)
                if match:
                    n_layer = int(match.group(1))
            elif 'bed_file' in line:
                match = re.search(r'bed_file:\s*(\S+)', line)
                if match:
                    bed_file = match.group(1)
            elif 'fasta_file' in line:
                match = re.search(r'fasta_file:\s*(\S+)', line)
                if match:
                    fasta_file = match.group(1)
            elif 'Current Benchmark: ' in line:
                curr_bench = line.split(': ')[1].strip()
                task_perf[curr_bench] = 0
            elif 'best' in line:
                match = re.search(r'(?<=best )\d+\.\d+', line)
                if match:
                    curr_best = float(match.group(0)) * 100
                    if curr_bench is not None:
                        task_perf[curr_bench] = curr_best if curr_best > task_perf[curr_bench] \
                            else task_perf[curr_bench]

        print(f'Width: {d_model}')
        print(f'Depth: {n_layer}')
        print(f'Bed file: {bed_file}')
        print(f'Fasta file: {fasta_file}')
        for task, perf in task_perf.items():
            print(f'{task}: {perf}')
        
        return task_perf

directory = '/scratch/gpfs/zw1300/misc/COS551/hyena-dna/slurm'
files = glob(f'{directory}/*.out')
# Sort by the numeric part after the last '-'
sorted_files = sorted(files, key=lambda x: int(os.path.basename(x).split('-')[-1].split('.')[0]))

# print("\n".join(sorted_files))
# configs = [
#     "100 human seq",
#     "20 diverse h",
#     "100 base h",
#     "20 diverse s",
#     "100 human seq",
#     "10 diverse hs",
#     "100 base h",
#     "20 diverse s",
#     "20 diverse h",
#     "100 human seq",
#     "10 diverse hs",
#     "100 base h",
#     "10 diverse hs",
#     "20 diverse h",
#     "20 diverse s",
# ]

configs = [
    "Base",
    "Diverse",
    "Base",
    "Base",
    "Diverse",
    "Base",
    "Diverse",
    "Diverse",
]
for i, file in enumerate(sorted_files):
    print(configs[i])
    extract_metrics(file)
    print()
