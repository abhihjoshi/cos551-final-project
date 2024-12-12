"""
Author: Abhishek Joshi
Compares the a set of out files (used for context experiments)
"""

import re
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
from collections import defaultdict

DATASETS = ["dummy_mouse_enhancers_ensembl",
            "demo_coding_vs_intergenomic_seqs",
            "demo_human_or_worm",
            "human_enhancers_cohn",
            "human_enhancers_ensembl",
            "human_ensembl_regulatory",
            "human_nontata_promoters",
            "human_ocr_ensembl"]

dataset_names = [
    "Mouse Enhancer Ensemble",
    "Protein Coding vs. non-Coding",
    "Human vs. Worm Classification",
    "Human Enhancers (Cohn et al.)",
    "Human Enhancers Ensembl",
    "Human Regulatory Classification",
    "Human non-TATA Promoters",
    "Human OCR Ensembl"
]

def extract_acc(out_path):

    results = {}
    for dataset in DATASETS:
        results[dataset] = {}

    # reads through each line an extract information regarding 
    with open(out_path, "r") as f:
        lines = f.readlines()
        current_dataset = ""
        current_epoch = 0
        val_acc = 0.0
        dataset_pattern = r"already downloaded val-(\S+)"
        epoch_pattern = r"Epoch (\d+):"
        acc_pattern = r"val/accuracy=([\d\.]+)"
        for i, line in tqdm(enumerate(lines)):

            # set the current dataset
            match = re.search(dataset_pattern, line)
            if match:
                current_dataset = match.group(1)

            # set the current epoch
            match = re.search(epoch_pattern, line)
            if match:
                epoch_number = int(match.group(1))
                current_epoch = epoch_number
                val_acc = 0.0

            # set the current validation acc
            match = re.search(acc_pattern, line)
            if match:
                assert current_dataset
                new_val_acc = float(match.group(1))
                if val_acc < new_val_acc:
                    results[current_dataset][current_epoch] = new_val_acc
                    val_acc = new_val_acc

    return results

def main(args):

    # get the validation accuracies for each epoch for each out path
    results = [extract_acc(args.out_paths[i]) for i in range(len(args.out_paths))]

    plot_epochs = 100
    x = [i for i in range(plot_epochs)]
    
    # plot the comparision
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    fig.suptitle("Comparison of Context Lengths", size=20)
    axes = axes.flatten()
    for i, ax in enumerate(axes):
        dataset = DATASETS[i]
        for j, result in enumerate(results):
            line_1 = [result[dataset][i] for i in range(plot_epochs)]
            ax.plot(x, line_1, label=f"Length {100 * 2**j}") 

        ax.set_title(dataset_names[i], fontdict={'size': 10.5})
        ax.set_ylabel("Accuracy")
        ax.set_xlabel("Epoch")

        if i == 0:
            ax.legend(title="Context Lengths")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('compare_context.pdf')

if __name__ == "__main__":

    # user argument for the slurm outfile to extract information from
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out_paths",
        type=str,
        nargs="+",
        required=True
    )
    args = parser.parse_args()
    main(args)