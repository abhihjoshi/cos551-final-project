# Authors: Supraj Gunda, Abhishek Joshi
# inspired by Colin's bash scripts
# submits no-pretraining HyendaDNA experiment

d_model=(128 128 128 128)
n_layer=(2 4 8 16)

index=0
num_gpus=1
for i in "${!n_layer[@]}"; do
d_model=${d_model[$i]}
n_layer=${n_layer[$i]}
index=$((index+1))
log_file="hyena-dna-finetune-"$index
echo $d_model $n_layer
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12 --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=sg0666@princeton.edu --time 23:59:00 --job-name $log_file --signal USR1@180 <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash training_scratch.sh $d_model $n_layer
EOF
done