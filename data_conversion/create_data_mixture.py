import os
from tqdm import tqdm

mixtures = {
    # 'baseline': [
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38.ml.fa',
    # ],

    # 'diverse_human': [
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_009914755.1_T2T-CHM13v2.0_genomic.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCA_022833125.2_ASM2283312v2_genomic.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCA_018873775.2_hg01243.v3.0_genomic.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCA_011064465.2_Ash1_v2.2_genomic.ml.fa',
    # ],

    # 'diverse_species': [
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_000001635.27_GRCm39_genomic.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_000003025.6_Sscrofa11.1_genomic.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_002263795.3_ARS-UCD2.0_genomic.ml.fa',
    #     '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.ml.fa',
    # ],

    'diverse_species_and_human': [
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/hg38.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_000001635.27_GRCm39_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_000003025.6_Sscrofa11.1_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_002263795.3_ARS-UCD2.0_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCF_009914755.1_T2T-CHM13v2.0_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCA_022833125.2_ASM2283312v2_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCA_018873775.2_hg01243.v3.0_genomic.ml.fa',
        '/scratch/gpfs/zw1300/misc/COS551/data/processed_individual/GCA_011064465.2_Ash1_v2.2_genomic.ml.fa',
    ],
}

save_dir = '/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/'
for name, mix in mixtures.items():
    save_path = os.path.join(save_dir, f"{name}.ml.fa")
    with open(save_path, 'w') as f:
        for fp in mix:
            with open(fp) as tmp_f:
                for line in tqdm(tmp_f):
                    # check if it's not empty
                    if line.strip():
                        f.write(line)
    print(f"Saved mixture to {save_path}")
