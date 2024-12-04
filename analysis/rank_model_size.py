import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# Dataset names
datasets = [
    "demo_coding_vs_intergenomic_seqs",
    "demo_human_or_worm",
    "human_enhancers_cohn",
    "human_enhancers_ensembl",
    "human_ensembl_regulatory",
    "human_nontata_promoters",
    "human_ocr_ensembl"
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
colors = ['lightcoral', 'lightsalmon', 'lightgreen', 'lightskyblue', 'plum']

# Create the plot
plt.figure(figsize=(12, 8))

for i, model in enumerate(models):
    plt.plot(datasets, ranks[i], label=model, marker='o', color=colors[i])

# Customizing the plot
plt.xlabel('Datasets')
plt.ylabel('Rank')
plt.title('Success Rate Across Model Size')
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.gca().invert_yaxis()  # Invert y-axis so rank 1 is at the top
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="Log Model Size")
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

# Show the plot
plt.tight_layout()
# plt.show()

plt.savefig('model_rankings.png')
