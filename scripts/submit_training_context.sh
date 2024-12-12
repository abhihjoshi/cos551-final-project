# Authors: Abhishek Joshi
# inspired by Colin's bash scripts
# sets up no-pretraining HyendaDNA experiment
context_len=(100 200 400 800)

index=0
num_gpus=1
for i in "${!context_len[@]}"; do
context_len=${context_len[$i]}
index=$((index+1))
log_file="hyena-dna-finetune-"$index
echo "Queuing context length of" $context_len
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=aj9792@princeton.edu --time 23:59:00 --job-name $log_file --signal USR1@180 <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash training_scratch.sh $context_len
EOF
done