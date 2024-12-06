import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# Dataset names
datasets = [
    "dummy_mouse_enhancers_ensembl",
    "demo_coding_vs_intergenomic_seqs",
    "demo_human_or_worm",
    "human_enhancers_cohn",
    "human_enhancers_ensembl",
    "human_ensembl_regulatory",
    "human_nontata_promoters",
    "human_ocr_ensembl"
]

# Model names
mixtures = ["True Baseline", "Baseline", "Diverse Human", "Diverse Species", "Diverse Human + Species"]

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
    plt.plot(datasets, ranks[i], label=model, marker='o', color=colors[i])

# Customizing the plot
plt.xlabel('Datasets')
plt.ylabel('Rank', size=20)
plt.title('Data Mixture Ranks for Genomic\nBenchmarks Evaluations', size=20)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(fontsize=20)
plt.gca().invert_yaxis()  # Invert y-axis so rank 1 is at the top
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="Data Mixture")
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

# Show the plot
plt.tight_layout()
# plt.show()

plt.savefig('mixture_rankings.png')
