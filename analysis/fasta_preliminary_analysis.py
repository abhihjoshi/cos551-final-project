import argparse
import numpy as np
import matplotlib.pyplot as plt

from Bio import SeqIO
from Bio import motifs

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        required=True
    )
    args = parser.parse_args()

    fasta_path = args.path
    sequences = list(SeqIO.parse(fasta_path, "fasta"))

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

