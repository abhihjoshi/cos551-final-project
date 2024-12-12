# Author: Colin Wang

source $CONDA_INIT
conda activate hyena-dna

# bed_files=(
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/human-sequences.bed"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/baseline.bed"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_human.bed"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species.bed"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species_and_human.bed"
# )

# fasta_files=(
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/baseline.ml.fa"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/baseline.ml.fa"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_human.ml.fa"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species.ml.fa"
#     "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species_and_human.ml.fa"
# )

# epochs=(
#     100
#     100
#     20
#     20
#     10
# )

bed_files=(
    "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/baseline.bed"
    "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species.bed"
)

fasta_files=(
    "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/baseline.ml.fa"
    "/scratch/gpfs/zw1300/misc/COS551/data/processed_mix/diverse_species.ml.fa"
)

epochs=(
    100
    20
)

index=$1
bed_file=${bed_files[$index]}
fasta_file=${fasta_files[$index]}
epoch=${epochs[$index]}

python -m train wandb=null \
    experiment=hg38/hg38_hyena \
    model.d_model=$2 \
    model.n_layer=$3 \
    dataset.bed_file=$bed_file \
    dataset.fasta_file=$fasta_file \
    dataset.batch_size=256 \
    train.global_batch_size=256 \
    dataset.max_length=1024 \
    optimizer.lr=6e-4 \
    trainer.devices=1 \
    trainer.max_epochs=$epoch \
