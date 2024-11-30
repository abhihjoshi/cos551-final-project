fp = "/scratch/gpfs/zw1300/misc/COS551/data/bost9/ncbi_dataset/data/GCF_002263795.3/GCF_002263795.3_ARS-UCD2.0_genomic.fna"

# read 50 lines
with open(fp) as f:
    for i, line in enumerate(f):
        if i == 1000:
            break
        print(line.strip())