# Author: Colin Wang, drafted by chatgpt

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_nucleotide_composition(file_paths):
    """
    Generates a 2x3 subplot of renormalized stacked bar charts 
    for nucleotide composition from five CSV files.

    Parameters:
    - file_paths: List of 5 file paths to the CSV files.
    """
    if len(file_paths) != 5:
        raise ValueError("Exactly 5 file paths are required.")
    plt.rcParams.update({
        'font.size': 14,         # Base font size for labels, titles, and legend
        'axes.titlesize': 16,    # Title size for each subplot
        'axes.labelsize': 14,    # Label size for x and y axes
        'xtick.labelsize': 12,   # X-axis tick labels
        'ytick.labelsize': 12,   # Y-axis tick labels
        'legend.fontsize': 12,   # Legend font size
        'figure.titlesize': 18   # Overall figure title size (if used)
    })
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 8), sharey=True)
    axes = axes.flatten()  # Flatten the 2D array of axes for easier indexing
    
    for i, file_path in enumerate(file_paths):
        # Load the data
        data = pd.read_csv(file_path)
        data.rename(columns={'Unnamed: 0': 'Bin'}, inplace=True)
        
        # Calculate total including 'N' and renormalized percentages
        data['Total_including_N'] = data[['A', 'C', 'G', 'T', 'N']].sum(axis=1)
        for nucleotide in ['A', 'C', 'G', 'T', 'N']:
            data[f'{nucleotide}_percent_renormalized'] = (data[nucleotide] / data['Total_including_N']) * 100
        
        # Plot for each dataset
        ax = axes[i]
        ax.bar(data['Bin'], data['A_percent_renormalized'], label='A', color='blue')
        ax.bar(data['Bin'], data['C_percent_renormalized'], bottom=data['A_percent_renormalized'], label='C', color='orange')
        ax.bar(data['Bin'], data['G_percent_renormalized'], bottom=data['A_percent_renormalized'] + data['C_percent_renormalized'], label='G', color='green')
        ax.bar(data['Bin'], data['T_percent_renormalized'], bottom=data['A_percent_renormalized'] + data['C_percent_renormalized'] + data['G_percent_renormalized'], label='T', color='red')
        ax.bar(data['Bin'], data['N_percent_renormalized'], bottom=data['A_percent_renormalized'] + data['C_percent_renormalized'] + data['G_percent_renormalized'] + data['T_percent_renormalized'], label='N', color='gray')
        
        basename = os.path.basename(file_path).replace('_actg_50bins.csv', '')
        ax.set_title(basename)
        ax.set_xticklabels(data['Bin'], rotation=90)
        if i == 0:
            ax.set_ylabel('Percentage')
    
    # Remove the unused 6th subplot
    fig.delaxes(axes[-1])
    
    # Add legend to the first subplot
    axes[0].legend(title='Nucleotide', loc='upper left')
    plt.tight_layout()
    plt.savefig('nucleotide_composition_bin_2x3.pdf')
    # plt.show()

# Example usage:
fp1 = '/scratch/gpfs/zw1300/misc/COS551/data/hg38/data/GCF_000001405.26/GCF_000001405.26_GRCh38_genomic.fna'
fp2 = '/scratch/gpfs/zw1300/misc/COS551/data/ash/ncbi_dataset/data/GCA_011064465.2/GCA_011064465.2_Ash1_v2.2_genomic.fna'
fp3 = '/scratch/gpfs/zw1300/misc/COS551/data/t2t/ncbi_dataset/data/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna'
fp4 = '/scratch/gpfs/zw1300/misc/COS551/data/asm/ncbi_dataset/data/GCA_022833125.2/GCA_022833125.2_ASM2283312v2_genomic.fna'
fp5 = '/scratch/gpfs/zw1300/misc/COS551/data/hg01/ncbi_dataset/data/GCA_018873775.2/GCA_018873775.2_hg01243.v3.0_genomic.fna'
fps = [fp1, fp2, fp3, fp4, fp5]
fps = [fp.replace('.fna', '_actg_50bins.csv') for fp in fps]
plot_nucleotide_composition(fps)
