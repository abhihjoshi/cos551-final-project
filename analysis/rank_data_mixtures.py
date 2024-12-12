"""
Rank plot for the success rate for each model on
the eval dataset (models differ in pretraining data).
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

# Example ranks for each model on each dataset (ensure dimensions match)
# Replace with actual rank data
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
