# COS 551 Final Project - Pretraining Compute-Optimal Genomic Foundation Models

Team Members: Zirui "Colin" Wang, Abhishek Joshi, Supraj Gunda

## Cloning the repo

Run the following command to clone the repo including submodules.
```
git clone --recurse-submodules git@github.com:abhihjoshi/cos551-final-project.git
```

**Note**: The genomics_benchmark submodule provides .tsv data corresponding to the start and env positions of sequences. For replication and benchmarking purposes, we include this repo as a submodule to get access to the data provided.

## Gerating data

Before generating data, please ensure you have the genomics_benchmarks submodule present in you directory.

Please download NCBI data from [here](https://www.ncbi.nlm.nih.gov/datasets/genome/). Search for the dataset you require and download both the FASTA data and the data corresponding to information about the chromosomes (sequence report). We recommend you download the FASTA data and store it under a directory called `ncbi_data`.

To generate a series of .txt files corresponding to individual sequences of smaller length, run the `scripts/get_sequences.py` file. This takes in three arguments:

- fasta_path: path to the fasta file containing all sequences
- seq_report_path: path to sequence report path downloaded from the NCBI website corresponding to your FASTA data
- benchmark_dataset: name of benchmark dataset from `genomic_benchmarks/datasets`

An example command is shown below:
```
python scripts/get_sequences.py --fasta_path ncbi_data/ncbi_dataset_mouse/ncbi_dataset/data/GCF_000001635.27/GCF_000001635.27_GRCm39_genomic.fna --seq_report_path ncbi_data/ncbi_dataset_mouse/sequence_report.tsv --benchmark_dataset dummy_mouse_enhancers_ensembl
```