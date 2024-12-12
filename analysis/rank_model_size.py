"""
Rank plot for the success rate for each model on
the eval dataset (models differ in size).
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# Dataset names
datasets = [
    "Human vs. Worm Classification",
    "Protein Coding vs. non-Coding",
    "Human Regulatory Classification",
    "Human Enhancers Ensembl",
    "Human Enhancers (Cohn et al.)",
    "Human non-TATA Promoters",
    "Human OCR Ensembl"
]

# Model names
models = ["2", "4", "8", "16"]

# Example ranks for each model on each dataset (ensure dimensions match)
# Replace with actual rank data
ranks = [
    [4, 4, 4, 4, 4, 4, 4],
    [3, 3, 2, 3, 3, 3, 3],
    [1, 1, 3, 1, 2, 2, 2],
    [2, 2, 1, 2, 1, 1, 1],
]

# Colors for the models
colors = ['red', 'darkorange', 'green', 'skyblue', 'plum']

# Create the plot
plt.figure(figsize=(12, 8))

for i, model in enumerate(models):
    plt.plot(datasets, ranks[i], label=model, marker='o', color=colors[i], linewidth=3)

# Customizing the plot
plt.xlabel('Datasets', size=20)
plt.ylabel('Rank', size=20)
plt.title('Model Sizes Ranks for Genomic\nBenchmarks Evaluations', size=20)
plt.xticks(rotation=45, ha='right', fontsize=20)
plt.yticks(fontsize=20)

plt.gca().invert_yaxis()  # Invert y-axis so rank 1 is at the top
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="Model Layers", fontsize=18)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

# Show the plot
plt.tight_layout()
# plt.show()

plt.savefig('model_rankings.pdf')
