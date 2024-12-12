# Author: Colin Wang, drafted by chatgpt

from tqdm import tqdm
import re

def extract_chromosome_name(text):
    print(text)
    match = re.search(r'\bCHROMOSOME (\d+|[A-Z])\b', text)
    if match:
        result = f">CHR{match.group(1)}"
        if 'CHM13' not in text:
            return False
        # if 'UNLOCALIZED GENOMIC SCAFFOLD' in text:
        #     return False
        return result
    else:
        print("No match found for text:", text)
        return False

def examine_top_lines(file_path, begin=0, end=10):
    """
    Examine the top few lines of a .fna file.

    Parameters:
    file_path (str): Path to the .fna file.
    num_lines (int): Number of lines to display. Default is 5.

    Returns:
    None
    """
    try:
        with open(file_path, 'r') as file:
            for i in range(end):
                line = file.readline()
                if not line:
                    break  # Stop if file has fewer lines than requested
                if i >= begin:
                    print(line.strip())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_fna(file_path, output_file, num_lines=None):
    """
    Read the first N lines of a .fna file, capitalize all letters, 
    and append every 50 letters to a list, then dump the list to a file.

    Parameters:
    file_path (str): Path to the .fna file.
    output_file (str): Path to the output file.
    num_lines (int): Number of lines to read from the input file. Default is 5.

    Returns:
    None
    """
    chr_dict = {}
    try:
        sequence_list = []
        curr_chr_seq = ""
        curr_chr = False

        with open(file_path, 'r') as file:
            for i, line in tqdm(enumerate(file)):
                line = line.strip().upper()
                if '>' in line:
                    if curr_chr:
                        chr_dict[curr_chr] = curr_chr_seq
                    curr_chr = extract_chromosome_name(line)
                    if curr_chr:
                        curr_chr_seq = "" if curr_chr not in chr_dict else chr_dict[curr_chr]
                else:
                    if curr_chr:
                        curr_chr_seq += line
            
        # sort the dictionary by key
        chr_dict = dict(sorted(chr_dict.items()))
        combined_sequence = ''
        curr_line = ''
        for k, v in tqdm(chr_dict.items()):
            if k == '>CHRY':
                # ignore this chromosome
                continue
            if curr_line != '':
                curr_line += '\n'
                combined_sequence += curr_line
                curr_line = ''
            combined_sequence += k.lower() + '\n'
            for i, elem in enumerate(v):
                # Replace non-ACGT characters with N after the first line
                if elem not in set('ACGT'):
                    elem = 'N'
                if len(curr_line) == 50:
                    curr_line += '\n'
                    combined_sequence += curr_line
                    curr_line = ''
                curr_line += elem

        # Write the sequence list to the output file
        with open(output_file, 'w') as out_file:
            out_file.write(combined_sequence)

        print(f"Processed sequences written to {output_file}")
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def compare_files(file1, file2):
    """
    Compare two files line by line and return the line number and content of mismatched lines.

    Parameters:
    file1 (str): Path to the first file.
    file2 (str): Path to the second file.

    Returns:
    list of tuples: Each tuple contains (line_number, file1_line, file2_line) for mismatched lines.
    """
    mismatched_lines = []

    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            line_number = 1
            while True:
                line1 = f1.readline()
                line2 = f2.readline()

                # If both lines are empty, end of file reached for both
                if not line1 and not line2:
                    break

                if not line2:
                    # print the next 5 lines of file1
                    print("File2 is shorter than File1")
                    for i in range(5):
                        line1 = f1.readline()
                        print(line1)

                # Compare lines
                if line1 != line2:
                    # if '>' in line2 or '>' in line1:
                    print(f"Line {line_number} mismatch:\n  File1: {line1.strip()}\n  File2: {line2.strip()}")
                    # breakpoint()
                    mismatched_lines.append((line_number, line1.strip(), line2.strip()))

                line_number += 1

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return mismatched_lines

# # Example usage
# file1_path = '/scratch/gpfs/zw1300/misc/COS551/hyena-dna/data/hg38/hg38.ml.fa'
# file2_path = '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38.ml.fa'

# mismatches = compare_files(file1_path, file2_path)
# if mismatches:
#     for line_num, f1_line, f2_line in mismatches:
#         print(f"Line {line_num} mismatch:\n  File1: {f1_line}\n  File2: {f2_line}")
# else:
#     print("The files match perfectly.")

# # Example usage
# input_file = '/scratch/gpfs/zw1300/misc/COS551/hyena-dna/data/hg38/hg38.ml.fa'
# output_file = '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38_hyena.ml.fa'
# process_fna(input_file, output_file, num_lines=None)
# input_file = '/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_2/ncbi_dataset/data/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna'
# output_file = '/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_1/ncbi_dataset/data/GCF_000001405.40/processed_human_2.fna'
# process_fna(input_file, output_file, num_lines=None)

# # Example usage
# print("Reading line {} to {} from the file".format(0, 10))
# file_path = '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38.ml.fa'
# examine_top_lines(file_path, 0, 10)
# print("Reading line {} to {} from the file".format(200, 205))
# examine_top_lines(file_path, 1000000, 1000010)

# file1 = '/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_1/ncbi_dataset/data/GCF_000001405.40/processed_human_1.fna'
file1 = '/Users/abhishek/Documents/classes/cos551/final_project/ncbi_data/ncbi_dataset_human_2/ncbi_dataset/data/GCF_009914755.1/processed_human_2.fna'
file2 = '/Users/abhishek/Documents/classes/cos551/temp/data/human/hg38.ml.fa'
file3 = 
compare_files(file1=file1, file2=file2)

