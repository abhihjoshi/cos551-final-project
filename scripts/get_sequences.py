import os
import tqdm
import gzip
import pprint
import argparse
import pandas as pd

from Bio import SeqIO

def generate_txt_seqs(
    chromosome_seqs: dict,
    fasta_path: str,
    benchmark_dataset: str
):
    """
    Generates a series of txt files where each file corresponds 
    to a sequence
    """
    split = ["train", "test"]
    classes = ["positive", "negative"]

    for s in split:
        for c in classes:
            benchmark_path = os.path.join("genomic_benchmarks/datasets", benchmark_dataset, s, f"{c}.csv.gz")
            with gzip.open(benchmark_path, "r") as data:
                df = pd.read_csv(data, sep=',')
                output_dir = os.path.join(os.path.dirname(fasta_path), "generated_sequences", s, c)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                for i, row in tqdm.tqdm(df.iterrows()):
                    region = row["region"]
                    seq = str(chromosome_seqs[region][row["start"]:row["end"]]).upper()
                    output_file = os.path.join(output_dir, f"{i}.txt")
                    with open(output_file, "w") as f:
                        f.write(seq)
            print(f"Completed generating txt seqs for {s}, {c}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fasta_path",
        type=str,
        required=True,
        help="path to fasta file"
    )
    parser.add_argument(
        "--seq_report_path",
        type=str,
        required=True,
        help="path to .tsv sequence report (information about chromosome to id mapping)"
    )
    parser.add_argument(
        "--benchmark_dataset",
        type=str,
        required=True,
        help="genomic benchmarks dataset (i.e. dummy_mouse_enhancers_ensembl)"
    )
    args = parser.parse_args()

    # creates mapping from refseq id and chromosome number
    df = pd.read_csv(args.seq_report_path, sep='\t')
    id_name_mapping = {}
    for _, row in df.iterrows():
        if row["Molecule type"] == "Chromosome" and row["RefSeq seq accession"].startswith("NC_"):
            id_name_mapping[row["RefSeq seq accession"]] = row["UCSC style name"]

    # parses the fasta file and gets the sequences
    chromosome_seqs = {}
    for record in tqdm.tqdm(SeqIO.parse(args.fasta_path, "fasta")):
        recid = record.id
        recseq = record.seq
        if recid in id_name_mapping:
            chromosome_seqs[id_name_mapping[recid]] = recseq

    generate_txt_seqs(chromosome_seqs=chromosome_seqs,
                      fasta_path=args.fasta_path,
                      benchmark_dataset=args.benchmark_dataset)

    




    
        