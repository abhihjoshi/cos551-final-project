import random
from tqdm import tqdm
random.seed(42)

fasta_file = '/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species_and_human.ml.fa'
output_file = '/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species_and_human.bed'

seq_length = 131072
train_per_file = 34021
total_val = 2213
total_test = 1937
train_multiplier = 10
total_train = train_per_file * train_multiplier
total = total_train + total_val + total_test

def read_fasta_to_dict(fasta_file):
    """
    Read a fasta file and return a dictionary of sequence IDs and sequences.

    Parameters:
    fasta_file (str): Path to the fasta file.

    Returns:
    dict: Dictionary with sequence IDs as keys and sequences as values.
    """
    sequences = {}
    with open(fasta_file, 'r') as f:
        current_id = None
        current_seq = ''
        for line in tqdm(f):
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = current_seq
                current_id = line[1:]
                current_seq = ''
            else:
                current_seq += line
        sequences[current_id] = current_seq
    return sequences

def create_valid_interval_start(seq_dict, length):
    interval_dict = {}
    for seq_id, seq in tqdm(seq_dict.items()):
        interval_dict[seq_id] = []
        for i in range(0, len(seq), length):
            subseq = seq[i:i+length]
            if 'N' not in subseq and len(subseq) == length:
                interval_dict[seq_id].append(i)
    return interval_dict

def generate_bed_file(interval_dict, length, output_file, 
                      total_train, total_val, total_test):
    bed_dict = {
        'chr': [],
        'start': [],
        'end': [],
        'split': []
    }
    lst_of_chr_intervals = []
    for seq_id, intervals in interval_dict.items():
        for interval in intervals:
            lst_of_chr_intervals.append((seq_id, interval, interval + length))
    random.shuffle(lst_of_chr_intervals)
    train_samples = 0
    for i, (seq_id, start, end) in tqdm(enumerate(lst_of_chr_intervals)):
        if i < total_test:
            split = 'test'
        elif i < total_test + total_val:
            split = 'val'
        elif i < total_test + total_val + total_train:
            split = 'train'
            train_samples += 1
        bed_dict['chr'].append(seq_id)
        bed_dict['start'].append(start)
        bed_dict['end'].append(end)
        bed_dict['split'].append(split)
    if train_samples != total_train:
        train_lst_of_chr_intervals = lst_of_chr_intervals[total_test + total_val:]
        while train_samples < total_train:
            for i, (seq_id, start, end) in enumerate(train_lst_of_chr_intervals):
                if train_samples == total_train:
                    break
                bed_dict['chr'].append(seq_id)
                bed_dict['start'].append(start)
                bed_dict['end'].append(end)
                bed_dict['split'].append('train')
                train_samples += 1

    # generate a tsv file
    with open(output_file, 'w') as f:
        for i in range(len(bed_dict['chr'])):
            f.write(f"{bed_dict['chr'][i]}\t{bed_dict['start'][i]}\t{bed_dict['end'][i]}\t{bed_dict['split'][i]}\n")

print("Reading fasta file...")
sequences = read_fasta_to_dict(fasta_file)
print("Creating valid intervals...")
interval_dict = create_valid_interval_start(sequences, seq_length)
print("Generating bed file...")
generate_bed_file(interval_dict, seq_length, output_file, total_train, total_val, total_test)
print("Done!")
