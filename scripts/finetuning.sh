source $CONDA_INIT
conda activate hyena-dna

model_path=$1
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
    python -m train wandb=null \
        experiment=hg38/genomic_benchmark \
        dataset.dataset_name=$benchmark \
        train.pretrained_model_path=$model_path \
        dataset.max_length=500 \
        model.layer.l_max=1026 \
        model.d_model=$2 \
        model.n_layer=$3 \
        model.fused_dropout_add_ln=False 
done
