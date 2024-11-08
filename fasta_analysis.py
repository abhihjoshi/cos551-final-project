from Bio import SeqIO
from Bio import motifs
import numpy as np

import matplotlib.pyplot as plt

def load_sequences(fasta_file):
    sequences = list(SeqIO.parse(fasta_file, "fasta"))
    return sequences

if __name__ == "__main__":

    fasta_path = "/Users/abhishek/Documents/classes/cos551/data/ncbi_dataset_mouse/ncbi_dataset/data/GCF_000001635.27/GCF_000001635.27_GRCm39_genomic.fna"
    sequences = load_sequences(fasta_path)

    seq_length = [len(seq) for seq in sequences]
    
    min_length = np.min(seq_length)
    max_length = np.max(seq_length)
    mean_length = np.mean(seq_length)
    median_length = np.median(seq_length)
    std_dev_length = np.std(seq_length)
    percentiles = np.percentile(seq_length, [25, 50, 75])

    # Display the results
    print("Sequence Length Statistics:")
    print(f"Total: {len(seq_length)}")
    print(f"Minimum Length: {min_length:.1e}")
    print(f"Maximum Length: {max_length:.1e}")
    print(f"Mean Length: {mean_length:.1e}")
    print(f"Standard Deviation: {std_dev_length:.1e}")

