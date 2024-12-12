# Author: Colin Wang

from genomic_benchmarks.loc2seq import download_dataset

path = "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/data/genomic_benchmark"
dataset_names = [
    "dummy_mouse_enhancers_ensembl",
    "demo_coding_vs_intergenomic_seqs",
    "demo_human_or_worm",
    "human_enhancers_cohn",
    "human_enhancers_ensembl",
    "human_ensembl_regulatory",
    "human_nontata_promoters",
    "human_ocr_ensembl",
]

for dataset_name in dataset_names:
    download_dataset(dataset_name, version=0, dest_path=path)
