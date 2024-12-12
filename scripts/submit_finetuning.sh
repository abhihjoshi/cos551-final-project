# Author: Colin Wang

model_ckpts=(
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-51-58-125330/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-51-58-126147/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-51-58-126880/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-52-27-052366/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-52-43-997551/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-52-44-000626/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-52-59-538789/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-52-59-540445/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-52-59-580287/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-53-29-089532/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-53-29-182792/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-53-36-301792/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-54-02-154636/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-54-02-155340/checkpoints/test/loss.ckpt"
    "/scratch/gpfs/zw1300/misc/COS551/hyena-dna/outputs/2024-11-29/19-54-02-156514/checkpoints/test/loss.ckpt"
)

d_model=(
    128
    128
    128
    128
    256
    128
    256
    256
    256
    128
    256
    128
    128
    128
    128
)

n_layer=(
    2
    2
    2
    2
    2
    2
    2
    2
    2
    4
    2
    4
    4
    4
    4
)

index=0
num_gpus=1
for i in "${!model_ckpts[@]}"; do
model_ckpt=${model_ckpts[$i]}
d_model=${d_model[$i]}
n_layer=${n_layer[$i]}
index=$((index+1))
log_file="hyena-dna-finetune-"$index
echo $model_ckpt $d_model $n_layer
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=zwc.compute@yahoo.com --time 23:59:00 --job-name $log_file --signal USR1@180 -p "pli-c" <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash finetuning.sh $model_ckpt $d_model $n_layer
EOF
done
