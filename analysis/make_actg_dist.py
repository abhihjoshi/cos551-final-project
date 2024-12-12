# Author: Colin Wang

import matplotlib.pyplot as plt
import os
import re
import pandas as pd
from tqdm import tqdm
import numpy as np
from collections import defaultdict
import sys

BASE_MAPPING = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3,
    'N': 4
}

BASENAME_MAPPING = {
    'GCF_000001405.26_GRCh38_genomic.fna': 'hg38',
    'GCA_011064465.2_Ash1_v2.2_genomic.fna': 'ash',
    'GCF_009914755.1_T2T-CHM13v2.0_genomic.fna': 't2t',
    'GCA_022833125.2_ASM2283312v2_genomic.fna': 'asm',
    'GCA_018873775.2_hg01243.v3.0_genomic.fna': 'hg01'
}

def map_seq_name_to_chr(file_name, line):
    if file_name == 'GCF_000001405.26_GRCh38_genomic.fna':
        if not line.startswith('>NC_0000'): return None
        chr_num = line.split('.')[0][-2:].replace('23', 'X').replace('24', 'Y')
    elif file_name == 'GCA_011064465.2_Ash1_v2.2_genomic.fna':
        if not line.startswith('>CM0215'): return None
        if 'chromosome' not in line: return None
        chr_num = line.split(' ')[6].replace(',', '')
    elif file_name == 'GCF_009914755.1_T2T-CHM13v2.0_genomic.fna':
        chr_num = line.split(' ')[6].replace(',', '')
    elif file_name == 'GCA_022833125.2_ASM2283312v2_genomic.fna':
        if not line.startswith('>CM000'): return None
        chr_num = line.split(' ')[4].replace(',', '')
    elif file_name == 'GCA_018873775.2_hg01243.v3.0_genomic.fna':
        if not line.startswith('>CM034'): return None
        chr_num = line.split(' ')[6].replace(',', '')
    else:
        return None
    return f"chr{chr_num}"

def print_named_lines(file_path, header_only=False):
    file_name = os.path.basename(file_path)
    with open(file_path) as f:
        for line in f:
            if header_only:
                if line[0] == '>':
                    print(file_name, line.strip())
            else:
                print(file_name, line.strip())

def count_actg_by_chr(fasta_file, save_path):
    chr_actg_counts = defaultdict(lambda: np.zeros(5, dtype=int))
    basename = os.path.basename(fasta_file)
    
    chr_name = None
    with open(fasta_file) as f:
        for line in tqdm(f):
            line = line.strip()
            if line.startswith('>'):
                chr_name = map_seq_name_to_chr(basename, line)
            elif chr_name:
                for base in line.upper():
                    base = base if base in BASE_MAPPING else 'N'
                    chr_actg_counts[chr_name][BASE_MAPPING[base]] += 1
    
    df = pd.DataFrame.from_dict(chr_actg_counts, orient='index', columns=['A', 'C', 'G', 'T', 'N'])
    df.to_csv(save_path, index=True)
    return True

def count_acgt_by_bins(fasta_file, save_path, num_bins=50):
    chr_actg_counts = defaultdict(lambda: np.zeros(5, dtype=int))
    basename = os.path.basename(fasta_file)
    all_nucleotides = ''
    
    chr_name = None
    with open(fasta_file) as f:
        for line in tqdm(f):
            line = line.strip()
            if line.startswith('>'):
                chr_name = map_seq_name_to_chr(basename, line)
            elif chr_name:
                all_nucleotides += line
    length = len(all_nucleotides)
    bin_size = length // num_bins
    for i in range(num_bins):
        start = i * bin_size
        end = (i + 1) * bin_size
        if i == num_bins - 1:
            end = length
        for base in all_nucleotides[start:end].upper():
            base = base if base in BASE_MAPPING else 'N'
            chr_actg_counts[i][BASE_MAPPING[base]] += 1
    
    df = pd.DataFrame.from_dict(chr_actg_counts, orient='index', columns=['A', 'C', 'G', 'T', 'N'])
    df.to_csv(save_path, index=True)
    return True

def kmer_counts(fasta_file, save_path, k=5, top_seq_to_save=10000, max_kmer=100000):
    kmer_counts = defaultdict(int)
    basename = os.path.basename(fasta_file)
    all_nucleotides = ''
    chr_name = None
    reached_max_kmer = False
    with open(fasta_file) as f:
        for line in tqdm(f):
            line = line.strip()
            if line.startswith('>'):
                chr_name = map_seq_name_to_chr(basename, line)
            elif chr_name:
                all_nucleotides += line
    length = len(all_nucleotides)
    for i in tqdm(range(length - k + 1)):
        if len(kmer_counts) >= max_kmer:
            reached_max_kmer = True
        kmer = all_nucleotides[i:i+k]
        kmer = kmer.upper()
        if reached_max_kmer and kmer not in kmer_counts:
            continue
        kmer_counts[kmer] += 1
    
    sorted_kmers = sorted(kmer_counts.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_kmers) > top_seq_to_save:
        sorted_kmers = sorted_kmers[:top_seq_to_save]
    else:
        sorted_kmers = sorted_kmers[:len(sorted_kmers)]
    df = pd.DataFrame(sorted_kmers, columns=['kmer', 'count'])
    df.to_csv(save_path, index=False)


if __name__ == '__main__':
    fp1 = '/scratch/gpfs/zw1300/misc/COS551/data/hg38/data/GCF_000001405.26/GCF_000001405.26_GRCh38_genomic.fna'
    fp2 = '/scratch/gpfs/zw1300/misc/COS551/data/ash/ncbi_dataset/data/GCA_011064465.2/GCA_011064465.2_Ash1_v2.2_genomic.fna'
    fp3 = '/scratch/gpfs/zw1300/misc/COS551/data/t2t/ncbi_dataset/data/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna'
    fp4 = '/scratch/gpfs/zw1300/misc/COS551/data/asm/ncbi_dataset/data/GCA_022833125.2/GCA_022833125.2_ASM2283312v2_genomic.fna'
    fp5 = '/scratch/gpfs/zw1300/misc/COS551/data/hg01/ncbi_dataset/data/GCA_018873775.2/GCA_018873775.2_hg01243.v3.0_genomic.fna'
    fps = [fp1, fp2, fp3, fp4, fp5]
    fp = fps[int(sys.argv[1])]
    k = int(sys.argv[2])
    
    save_path = fp.replace('.fna', f'_kmer{k}.csv')
    kmer_counts(fp, save_path, k=k, top_seq_to_save=10000)
