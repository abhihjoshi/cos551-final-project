"""
Downloads genomic benchmarks datasets to local machine
"""

from genomic_benchmarks.loc2seq import download_dataset
from genomic_benchmarks.data_check import is_downloaded

if __name__ == "__main__":

    dataset_names = [
        "dummy_mouse_enhancers_ensembl",
        "dummy_mouse_enhancers_ensembl",
        "demo_coding_vs_intergenomic_seqs",
        "demo_human_or_worm",
        "human_enhancers_cohn",
        "human_enhancers_ensembl",
        "human_ensembl_regulatory",
        "human_nontata_promoters",
        "human_ocr_ensembl"
    ]

    dest_path = "genomics_benchmarks_data"

    for dataset_name in dataset_names:
        if not is_downloaded(dataset_name, cache_path=dest_path):
            print("downloading {} to {}".format(dataset_name, dest_path))
            download_dataset(dataset_name, version=0, dest_path=dest_path)