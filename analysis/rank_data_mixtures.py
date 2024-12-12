"""
Author: Abhishek Joshi
Rank plot for the success rate for each model on
the eval dataset (models differ in pretraining data).

GPT Prompt: 
Can you write me code that will make a rank plot where each line represents a new model and there are 8 ticks for the 8 datasets
can you actually write me code so that I create 8 different plots, 1 for each dataset. Here are my dataset names: "dummy_mouse_enhancers_ensembl",
            "demo_coding_vs_intergenomic_seqs",
            "demo_human_or_worm",
            "human_enhancers_cohn",
            "human_enhancers_ensembl",
            "human_ensembl_regulatory",
            "human_nontata_promoters",
            "human_ocr_ensembl"
how can i move the legend out of the box to the right
how can i make the y axis have only integer values
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# Dataset names
datasets = [
    "Mouse Enhancer Ensemble",
    "Human vs. Worm Classification",
    "Protein Coding vs. non-Coding",
    "Human Regulatory Classification",
    "Human Enhancers Ensembl",
    "Human Enhancers (Cohn et al.)",
    "Human non-TATA Promoters",
    "Human OCR Ensembl"
]

# Model names
mixtures = ["H1 True", "H1 Pseudo", "H5 Pseudo", "H1S4 Pseudo", "H5S4 Pseudo"]

ranks = [
    [2, 4, 1, 2, 3, 4, 4, 4],
    [2, 3, 3, 4, 4, 5, 5, 3],
    [1, 2, 4, 3, 5, 2, 2, 2],
    [5, 1, 2, 1, 1, 1, 1, 1],
    [4, 5, 5, 5, 2, 2, 2, 5],
]

# Colors for the models
colors = ['red', 'darkorange', 'green', 'skyblue', 'plum']

# Create the plot
plt.figure(figsize=(12, 8))

for i, model in enumerate(mixtures):
    plt.plot(datasets, ranks[i], label=model, marker='o', color=colors[i], linewidth=3)

# Customizing the plot
plt.xlabel('Datasets', size=20)
plt.ylabel('Rank', size=20)
plt.title('Data Mixture Ranks for Genomic\nBenchmarks Evaluations', size=20)
plt.xticks(rotation=45, ha='right', fontsize=20)
plt.yticks(fontsize=20)
plt.gca().invert_yaxis()  # Invert y-axis so rank 1 is at the top
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="Data Mixture")
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

# Show the plot
plt.tight_layout()
# plt.show()

plt.savefig('mixture_rankings.pdf')
