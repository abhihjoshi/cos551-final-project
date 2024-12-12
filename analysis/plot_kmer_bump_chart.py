# Author: Colin Wang, drafted by chatgpt

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
        'font.size': 14,         # Base font size for labels, titles, and legend
        'axes.titlesize': 16,    # Title size for each subplot
        'axes.labelsize': 14,    # Label size for x and y axes
        'xtick.labelsize': 12,   # X-axis tick labels
        'ytick.labelsize': 12,   # Y-axis tick labels
        'legend.fontsize': 12,   # Legend font size
        'figure.titlesize': 18   # Overall figure title size (if used)
    })

# Define file paths for kmer4 and kmer16
kmer_types = ["kmer4", "kmer16"]
file_paths_base = {
    "GCA_011064465.2_Ash1_v2.2": "/scratch/gpfs/zw1300/misc/COS551/data/ash/ncbi_dataset/data/GCA_011064465.2/GCA_011064465.2_Ash1_v2.2_genomic_kmer4.csv",
    "GCA_022833125.2_ASM2283312v2": "/scratch/gpfs/zw1300/misc/COS551/data/asm/ncbi_dataset/data/GCA_022833125.2/GCA_022833125.2_ASM2283312v2_genomic_kmer4.csv",
    "GCA_018873775.2_hg01243.v3.0": "/scratch/gpfs/zw1300/misc/COS551/data/hg01/ncbi_dataset/data/GCA_018873775.2/GCA_018873775.2_hg01243.v3.0_genomic_kmer4.csv",
    "GCF_000001405.26_GRCh38": "/scratch/gpfs/zw1300/misc/COS551/data/hg38/data/GCF_000001405.26/GCF_000001405.26_GRCh38_genomic_kmer4.csv",
    "GCF_009914755.1_T2T-CHM13v2.0": "/scratch/gpfs/zw1300/misc/COS551/data/t2t/ncbi_dataset/data/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic_kmer4.csv"
}

# Update paths for kmer16
file_paths = {
    kmer_type: {name.replace("kmer4", kmer_type): path.replace("kmer4", kmer_type)
                for name, path in file_paths_base.items()}
    for kmer_type in kmer_types
}

# Load data for all kmer types
all_dataframes = {
    kmer_type: {name: pd.read_csv(path) for name, path in files.items()}
    for kmer_type, files in file_paths.items()
}

# Function to find top 15 kmers that appear in all datasets for a specific kmer type
def find_common_top_kmers(dataframes, top_n=15):
    first_dataset = list(dataframes.keys())[0]
    candidate_kmers = dataframes[first_dataset].nlargest(100, "count")["kmer"]
    
    common_kmers = []
    for kmer in candidate_kmers:
        if all(kmer in df["kmer"].values for df in dataframes.values()):
            common_kmers.append(kmer)
        if len(common_kmers) == top_n:
            break
            
    return common_kmers

# Prepare ranked data
def filter_and_rank_kmers(dataframes, common_kmers):
    ranked_data = {}
    for name, df in dataframes.items():
        filtered_df = df[df["kmer"].isin(common_kmers)].set_index("kmer")
        ranked_data[name] = filtered_df["count"].rank(ascending=False, method="min").reindex(common_kmers).astype(int)
    return pd.DataFrame(ranked_data)

# Find common top kmers and rank data for each kmer type
ranked_data_dict = {}
for kmer_type in kmer_types:
    common_kmers = find_common_top_kmers(all_dataframes[kmer_type])
    ranked_data_dict[kmer_type] = filter_and_rank_kmers(all_dataframes[kmer_type], common_kmers)

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(18, 6), sharey=True)
colors = plt.cm.tab20.colors  # Define the colors properly here

for ax, (kmer_type, ranked_data) in zip(axes, ranked_data_dict.items()):
    for i, kmer in enumerate(ranked_data.index):
        ax.plot(ranked_data.columns, ranked_data.loc[kmer], label=kmer, marker='o', color=colors[i % len(colors)])
    ax.set_title(f"Top 15 {kmer_type} Rankings")
    ax.set_xlabel("Dataset")
    ax.tick_params(axis='x', rotation=15)
    ax.set_ylabel("Rank")
    ax.set_ylim(16, 0)  # Explicitly set the y-axis limits so that 1 is at the top and 15 at the bottom

axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
axes[1].legend(bbox_to_anchor=(1.05, 1), loc="upper left")



plt.tight_layout()
plt.savefig("kmer_bump_chart.pdf")
plt.show()
