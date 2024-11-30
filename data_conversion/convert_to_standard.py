import os
import re
from tqdm import tqdm
import numpy as np
from collections import defaultdict

LEGIT_BASES = {'A', 'C', 'G', 'T'}

def map_seq_name_to_chr(file_name, line):
    postfix = None
    if file_name == 'GCF_000001405.26_GRCh38_genomic.fna':
        if not line.startswith('>NC_0000'): return None
        chr_num = line.split('.')[0][-2:].replace('23', 'X').replace('24', 'Y')
        postfix = ''
    elif file_name == 'GCA_011064465.2_Ash1_v2.2_genomic.fna':
        if not line.startswith('>CM0215'): return None
        if 'chromosome' not in line: return None
        chr_num = line.split(' ')[6].replace(',', '')
        postfix = 'ash'
    elif file_name == 'GCF_009914755.1_T2T-CHM13v2.0_genomic.fna':
        chr_num = line.split(' ')[6].replace(',', '')
        postfix = 't2t'
    elif file_name == 'GCA_022833125.2_ASM2283312v2_genomic.fna':
        if not line.startswith('>CM000'): return None
        chr_num = line.split(' ')[4].replace(',', '')
        postfix = 'asm'
    elif file_name == 'GCA_018873775.2_hg01243.v3.0_genomic.fna':
        if not line.startswith('>CM034'): return None
        chr_num = line.split(' ')[6].replace(',', '')
        postfix = 'hg01'
    elif file_name == 'GCF_002263795.3_ARS-UCD2.0_genomic.fna':
        if not line.startswith('>NC'): return None
        if 'chromosome' not in line: return None
        chr_num = line.split(' ')[13].replace(',', '')
        postfix = 'ars'
    elif file_name == 'GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.fna':
        if not line.startswith('>NC'): return None
        chr_num = line.split(' ')[10].replace(',', '')
        postfix = 'cfam'
    elif file_name == 'GCF_000003025.6_Sscrofa11.1_genomic.fna':
        if not line.startswith('>NC_01'): return None
        chr_num = line.split(' ')[9].replace(',', '')
        postfix = 'ssc'
    elif file_name == 'GCF_000001635.27_GRCm39_genomic.fna':
        if not line.startswith('>NC_000'): return None
        chr_num = chr_num = line.split(' ')[6].replace(',', '')
        postfix = 'mm'
    else:
        return None
    return f"chr{chr_num}_{postfix}"

def process(file_path, save_path, dry_run=False):
    chr_seq_dict = {}
    chr_name = None
    curr_chr_seq = ''
    f = open(file_path, 'r')
    basename = os.path.basename(file_path)
    save_path = os.path.join(os.path.dirname(save_path), basename.replace('.fna', '.ml.fa'))
    print(f"Processing {file_path}..., saving to {save_path}")
    num_lines, num_tracked = 0, 0
    with open(file_path) as tmp_f:
        for line in tmp_f:
            num_lines += 1
    for line in tqdm(f, total=num_lines):
        line = line.strip()
        if line.startswith('>'):
            # add the current chromosome sequence to the dictionary
            if curr_chr_seq:
                chr_seq_dict[chr_name] = curr_chr_seq
                curr_chr_seq = ''
            chr_name = map_seq_name_to_chr(basename, line)
            if dry_run:
                print(f"line: {line}, chr_name: {chr_name}")
        elif chr_name and not dry_run:
            for base in line.upper():
                base = base if base in LEGIT_BASES else 'N'
                curr_chr_seq += base
            num_tracked += len(line)
    # Add the last chromosome sequence
    if curr_chr_seq:
        chr_seq_dict[chr_name] = curr_chr_seq
    
    combined_sequence = ''
    curr_line = ''
    for chr_name, seq in tqdm(chr_seq_dict.items()):
        combined_sequence += f">{chr_name}\n"
        for i in range(0, len(seq), 50):
            curr_line = seq[i:i+50]
            combined_sequence += f"{curr_line}\n"
    
    with open(save_path, 'w') as out_file:
        out_file.write(combined_sequence)
    print(f"Processed sequences written to {save_path}")
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert a .fna file to a standard format.")
    parser.add_argument("--file_path", help="Path to the .fna file.")
    parser.add_argument("--save_path", help="Path to the output file.")
    parser.add_argument("--dry-run", action="store_true", help="Print the chromosome names without writing to the output file.")
    args = parser.parse_args()

    process(args.file_path, args.save_path, args.dry_run)
