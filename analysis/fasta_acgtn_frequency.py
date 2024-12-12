"""
Author: Abhishek Joshi
Gets the frequency on nucleotides in a genome assembly
"""
import argparse
from tqdm import tqdm
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

from Bio import SeqIO

def count_interval_frequency(sequence, start, end):
    """
    Returns the frequency of the bases within a given range
    """
    counts = defaultdict(int)
    assert start < end
    segment = sequence[start:end]
    for nucleotide in segment:
        n = nucleotide.upper()
        if n in set(["A", "C", "T", "G"]):
            counts[n] += 1
        else:
            counts["N"] += 1

    return counts

def count_frequency_buckets(sequence, 
                            num_buckets: int = 20):
    """
    Returns the frequency of all the characters with bucketing
    """
    frequencies = []
    sequence_len = len(sequence)
    interval_len = sequence_len // num_buckets
    for i in tqdm(range(num_buckets)):
        start = int(sequence_len * (i / num_buckets))
        end = start + interval_len
        # print(f"{i} ==> {start} {end}")
        bucket_freq = count_interval_frequency(sequence, start, end)
        frequencies.append(bucket_freq)
    return frequencies

def count_frequency(sequence):
    """
    Returns the frequency of all the characters in the sequence
    """
    return count_interval_frequency(sequence, 0, len(sequence))

def plot_frequencies(data):
    """
    Plot the normalized frequencies

    GPT Assist:
    Prompt: I have 5 lists with the same number of elements. I want to 
    divide each index of each list by the total at that index across 
    the differeent lists. How can I do this
    """

    buckets = len(data)
    x = np.arange(buckets)
    width = 0.8

    # Extract counts for each character across all buckets
    a_counts = [bucket["A"] for bucket in data]
    c_counts = [bucket["C"] for bucket in data]
    g_counts = [bucket["G"] for bucket in data]
    t_counts = [bucket["T"] for bucket in data]
    n_counts = [bucket["N"] for bucket in data]

    lists = [a_counts, c_counts, g_counts, t_counts, n_counts]

    # Normalize each index
    normalized_lists = []
    for i in range(buckets):  # Assuming all lists have the same length
        total = sum(l[i] for l in lists)  # Total across all lists at index i
        normalized_lists.append([l[i] / total for l in lists])

    # Transpose normalized_lists back to original structure
    a_counts, c_counts, g_counts, t_counts, n_counts = list(map(list, zip(*normalized_lists)))

    # Plot stacked bar chart
    plt.bar(x, a_counts, width, label="A")
    plt.bar(x, c_counts, width, bottom=a_counts, label="C")
    plt.bar(x, g_counts, width, bottom=np.add(a_counts, c_counts), label="G")
    plt.bar(x, t_counts, width, bottom=np.add(np.add(a_counts, c_counts), g_counts), label="T")
    plt.bar(x, n_counts, width, bottom=np.add(np.add(np.add(a_counts, c_counts), g_counts), t_counts), label="N")

    plt.xlabel("Chromosome")
    plt.ylabel("Frequency")
    plt.title("Nucleotide Frequencies Across Buckets")
    plt.xticks(x, [f"{i+1}" for i in range(buckets)])
    plt.legend(title="Nucleotide")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()

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

    for seq in sequences:
        f = count_frequency_buckets(seq, num_buckets=50)
        plot_frequencies(f)
        break

    # freqs = []
    # for seq in tqdm(sequences):
    #     if "NC" in seq.id:
    #         print(f"Including {seq.id}")
    #         f = count_frequency(seq)
    #         freqs.append(f)
    # plot_frequencies(freqs)