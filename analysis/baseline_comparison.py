"""
Plots the success of the baseline model against models trained with
our custom data mixture (specifically diverse species).
"""

import matplotlib.pyplot as plt
import numpy as np

datasets = [
    "Mouse Enhancer Ensemble",
    "Protein Coding vs. non-Coding",
    "Human vs. Worm Classification",
    "Human Enhancers (Cohn et al.)",
    "Human Enhancers Ensembl",
    "human_ensembl_regulatory",
    "Human non-TATA Promoters",
    "Human OCR Ensembl"
]

x = [2, 4, 8, 16]

# testing dataset sizes
dataset_sizes = [242, 25000, 25000, 6984, 30970, 57713, 9034, 34952]

baseline_2 = [.7933, .9076, .9604, .7270, .8931, .8727, .9619, .7691]
baseline_4 = [.7851, .9107, .9620, .7296, .9011, .8708, .9583, .7858]
baseline_8 = [.7686, .9139, .9635, .7257, .9047, .8710, .9600, .7929]
baseline_16 = [.7769, .9170, .9637, .7296, .9056, .8727, .9659, .7945]
baseline = np.array([baseline_2, baseline_4, baseline_8, baseline_16])

div_spec_2 = [.7810, .9065, .9590, .7242, .9007, .8708, .9615, .7697]
div_spec_4 = [.7644, .9118, .9622, .7339, .9036, .8722, .9657, .7861]
div_spec_8 = [.7769, .9170, .9637, .7296, .9056, .8727, .9659, .7945]
div_spec_16 = [.7934, .9155, .9632, .7345, .9045, .8730, .9667, .8005]
div_spec = np.array([div_spec_2, div_spec_4, div_spec_8, div_spec_16])

fig, axes = plt.subplots(2, 4, figsize=(12, 6))
fig.suptitle("Comparision of Evaluation Success\nAcross Model Sizes", size=20)

axes = axes.flatten()

for i, ax in enumerate(axes):
    # plots the baseline with confidence intervals
    ci_baseline = []
    for acc in baseline[:, i]:
        std_err = (acc * (1 - acc) / dataset_sizes[i]) ** 0.5
        margin_of_err = 1.96 * std_err
        ci_baseline.append(margin_of_err)

    # plot the diverse species with confidence intervals
    ci_div_spec = []
    for acc in div_spec[:, i]:
        std_err = (acc * (1 - acc) / dataset_sizes[i]) ** 0.5
        margin_of_err = 1.96 * std_err
        ci_div_spec.append(margin_of_err)

    print(ci_baseline)
    print(ci_div_spec)

    ax.plot(x, baseline[:, i], c="lightcoral", marker='o', label="Baseline") 
    ax.fill_between(x, (baseline[:, i]-ci_baseline), (baseline[:, i]+ci_baseline), color='lightcoral', alpha=.1)
    ax.plot(x, div_spec[:, i], c="lightseagreen", marker='o', label="Diverse Species")
    ax.fill_between(x, (div_spec[:, i]-ci_div_spec), (div_spec[:, i]+ci_div_spec), color='lightseagreen', alpha=.1)

    ax.set_xticks(x)
    ax.set_title(datasets[i], fontdict={'size': 10.5})
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Model Layers")

plt.legend()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

plt.savefig('baseline_comparision.pdf')