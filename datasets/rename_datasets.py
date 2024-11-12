import os
import argparse
import pandas as pd

def main(args):
    df = pd.read_csv(args.seq_report_path, sep='\t')
    id_name_mapping = {}
    for _, row in df.iterrows():
        if row["Molecule type"] == "Chromosome" and row["RefSeq seq accession"].startswith("NC_"):
            id_name_mapping[row["RefSeq seq accession"]] = row["UCSC style name"]

    # Directory containing the files
    directory_path = args.dir_path

    # Rename files in the directory based on the mapping
    for filename in os.listdir(directory_path):
        # Extract the base name (without extension) and extension
        base_name, ext = os.path.splitext(filename)
        
        # Check if the base name exists in the mapping
        if base_name in id_name_mapping:
            # Construct the new name
            new_name = id_name_mapping[base_name] + ext
            
            # Get full paths for renaming
            old_file_path = os.path.join(directory_path, filename)
            new_file_path = os.path.join(directory_path, new_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_name}")
        else:
            print(f"Skipped: {filename} (no mapping found)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir_path",
        type=str
    )
    parser.add_argument(
        "--seq_report_path",
        type=str
    )
    args = parser.parse_args()
    main(args)