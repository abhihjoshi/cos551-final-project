# Authors: Abhishek Joshi
# inspired by Colin's bash scripts
# sets up no-pretraining HyendaDNA experiment
source $CONDA_INIT
conda activate hyena-dna

genomic_benchmarks=(
    dummy_mouse_enhancers_ensembl
    demo_coding_vs_intergenomic_seqs
    demo_human_or_worm
    human_enhancers_cohn
    human_enhancers_ensembl
    human_ensembl_regulatory
    human_nontata_promoters
    human_ocr_ensembl
)

for benchmark in ${genomic_benchmarks[@]}; do
    echo "Current Benchmark: $benchmark"
    python /scratch/gpfs/aj9792/hyena-dna/train.py wandb=null \
        experiment=hg38/genomic_benchmark \
        dataset.dataset_name=$benchmark \
        dataset.max_length=$1 \
        model.layer.l_max=1026 \
        +model.checkpoint_mixer=True \
        +model.checkpoint_mlp=True \
        +train.precision=bf16 \
        train.pretrained_model_path=null\
        model.d_model=128 \
        model.n_layer=8 \
        model.fused_dropout_add_ln=False 
done
