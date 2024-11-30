file="/scratch/gpfs/zw1300/misc/COS551/data/suss11/ncbi_dataset/data/GCF_000003025.6/GCF_000003025.6_Sscrofa11.1_genomic.fna"

save_path="/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/"

python convert_to_standard.py \
    --file_path $file \
    --save_path $save_path \
    # --dry-run \
