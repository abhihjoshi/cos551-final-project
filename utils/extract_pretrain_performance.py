from glob import glob
import re
import numpy as np

def extract_metrics(file):
    best_val_loss = None
    d_model = None
    n_layer = None
    bed_file = None
    fasta_file = None
    max_epochs = None
    current_epoch = None

    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'd_model' in line:
                match = re.search(r'd_model:\s*(\d+)', line)
                if match:
                    d_model = int(match.group(1))
                    print(f'Width: {d_model}')
            elif 'n_layer' in line:
                match = re.search(r'n_layer:\s*(\d+)', line)
                if match:
                    n_layer = int(match.group(1))
                    print(f'Depth: {n_layer}')
            elif 'bed_file' in line:
                match = re.search(r'bed_file:\s*(\S+)', line)
                if match:
                    bed_file = match.group(1)
                    print(f'Bed file: {bed_file}')
            elif 'fasta_file' in line:
                match = re.search(r'fasta_file:\s*(\S+)', line)
                if match:
                    fasta_file = match.group(1)
                    print(f'Fasta file: {fasta_file}')
            elif 'max_epochs' in line:
                match = re.search(r'max_epochs:\s*(\d+)', line)
                if match:
                    max_epochs = int(match.group(1))
                    print(f'Max epochs: {max_epochs}')
            elif 'best' in line:
                match = re.search(r'(?<=best )\d+\.\d+', line)
                if match:
                    curr_best = float(match.group(0))
                    if best_val_loss is None or curr_best < best_val_loss:
                        best_val_loss = curr_best
            elif 'Epoch' in line:
                match = re.search(r'Epoch\s+(\d+)', line)
                if match:
                    epoch = int(match.group(1))
                    if current_epoch is None or epoch > current_epoch:
                        current_epoch = epoch
        print(f'Epoch {current_epoch}')
        
        if best_val_loss is not None:
            ppl = np.exp(best_val_loss)
            print(f'PPL: {ppl}')
        else:
            ppl = None

        return d_model, n_layer, bed_file, fasta_file, max_epochs, ppl

directory = '/scratch/gpfs/zw1300/misc/COS551/hyena-dna/slurm'
files = glob(f'{directory}/*.out')

for file in files:
    extract_metrics(file)
    print()
