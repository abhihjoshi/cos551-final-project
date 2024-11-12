import tqdm
import random
from typing import Dict

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

from Bio import SeqIO

class CombinedGeneticDataset(Dataset):
    """
    Dataset allowing for combination of multiple FASTA datasets
    """

    def __init__(self,
                 fasta_paths: Dict[str, str],
                 seq_reports: Dict[str, str],
                 seq_length: int,
                 dataset_size: int):
        
        self.fasta_paths = fasta_paths
        self.seq_reports = seq_reports
        self.seq_length = seq_length
        self.dataset_size = dataset_size
        
        self.seq_data = {}
        for name, fasta in fasta_paths.items():
            print(f"Parsing sequences for the {name} dataset")
            if name not in seq_reports.keys():
                raise ValueError("Each species dataset requires corresponding sequence report!")
            
            self.seq_data[name] = {}

            # Get list of valid ids for the dataset
            df = pd.read_csv(seq_reports[name], sep='\t')
            valid_ids = set()
            for _, row in df.iterrows():
                if row["Molecule type"] == "Chromosome" and row["RefSeq seq accession"].startswith("NC_"):
                    valid_ids.add(row["RefSeq seq accession"])
            
            chromosome_seqs = list(SeqIO.parse(fasta, "fasta"))
            for chromosome_seq in tqdm.tqdm(chromosome_seqs):
                if chromosome_seq.id in valid_ids:
                    self.seq_data[name][chromosome_seq.id] = str(chromosome_seq.seq).strip('N')

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        _, chromosome_seqs = random.choice(list(self.seq_data.items()))
        _, seq = random.choice(list(chromosome_seqs.items()))

        seq = seq.upper()
        start = random.randint(0, len(seq) - self.seq_length - 1)
        res = seq[start:start + self.seq_length]
        next_token = seq[start + self.seq_length]

        return res, next_token

if __name__ == "__main__":
    
    fasta_paths = {
        "human_1": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_1/ncbi_dataset/data/GCF_000001405.40/GCF_000001405.40_GRCh38.p14_genomic.fna",
        "human_2": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_2/ncbi_dataset/data/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna",
        "dog": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_dog/ncbi_dataset/data/GCF_011100685.1/GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.fna",
        "mouse": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_mouse/ncbi_dataset/data/GCF_000001635.27/GCF_000001635.27_GRCm39_genomic.fna"
    }

    seq_reports = {
        "human_1": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_1/sequence_report.tsv",
        "human_2": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_2/sequence_report.tsv",
        "dog": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_dog/sequence_report.tsv",
        "mouse": "/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_mouse/sequence_report.tsv"
    }

    dataset = CombinedGeneticDataset(fasta_paths=fasta_paths,
                                     seq_reports=seq_reports,
                                     seq_length=50,
                                     dataset_size=100000)
    
    dataloader = DataLoader(dataset=dataset)

    seq, label = next(iter(dataloader))
    print(seq, label)