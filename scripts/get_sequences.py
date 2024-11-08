import tqdm
import pprint
import argparse
import pandas as pd

from Bio import SeqIO

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
    args = parser.parse_args()

    df = pd.read_csv(args.seq_report_path, sep='\t')
    id_name_mapping = {}
    for index, row in df.iterrows():
        if row["Molecule type"] == "Chromosome" and row["RefSeq seq accession"].startswith("NC_"):
            id_name_mapping[row["RefSeq seq accession"]] = row["UCSC style name"]

    chromosome_seqs = {}
    for record in tqdm.tqdm(SeqIO.parse(args.fasta_path, "fasta")):
        recid = record.id
        recseq = record.seq
        if recid in id_name_mapping:
            chromosome_seqs[id_name_mapping[recid]] = recseq

    
        