# Author: Colin Wang

fp = "/scratch/gpfs/zw1300/misc/COS551/data/mm39/ncbi_dataset/data/GCF_000001635.27/GCF_000001635.27_GRCm39_genomic.fna"

f = open(fp, 'r')
for i, line in enumerate(f):
    line = line.strip()
    if line.startswith('>'):
        print(line)
    # if line.startswith('>NC_000'):
    #     print(line)
    #     chr_num = line.split(' ')[6].replace(',', '')
    #     print(f"chr{chr_num}")
