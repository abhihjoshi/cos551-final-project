# Author: Colin Wang

max_idx=1
num_gpus=1
d_model=128
n_layer=8
log_file="hyena-dna-pretrain-"$idx"-"$d_model"-"$n_layer
for idx in $(seq 0 $max_idx); do
echo "bash misc/COS551/hyena-dna/pretrain.sh $idx"
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=zwc.compute@yahoo.com --time 23:59:00 --job-name $log_file --signal USR1@180 -p "pli-c" <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash pretrain.sh $idx $d_model $n_layer
EOF
done

d_model=256
n_layer=8
log_file="hyena-dna-pretrain-"$max_idx"-"$d_model"-"$n_layer
for idx in $(seq 0 $max_idx); do
echo "bash misc/COS551/hyena-dna/pretrain.sh $idx"
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=zwc.compute@yahoo.com --time 23:59:00 --job-name $log_file --signal USR1@180 -p "pli-c" <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash pretrain.sh $idx $d_model $n_layer
EOF
done

d_model=128
n_layer=16
log_file="hyena-dna-pretrain-"$max_idx"-"$d_model"-"$n_layer
for idx in $(seq 0 $max_idx); do
echo "bash misc/COS551/hyena-dna/pretrain.sh $idx"
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=zwc.compute@yahoo.com --time 23:59:00 --job-name $log_file --signal USR1@180 -p "pli-c" <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash pretrain.sh $idx $d_model $n_layer
EOF
done

d_model=256
n_layer=16
log_file="hyena-dna-pretrain-"$max_idx"-"$d_model"-"$n_layer
for idx in $(seq 0 $max_idx); do
echo "bash misc/COS551/hyena-dna/pretrain.sh $idx"
sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=zwc.compute@yahoo.com --time 23:59:00 --job-name $log_file --signal USR1@180 -p "pli-c" <<EOF
#!/bin/bash
PORT=$(expr $RANDOM + 1000) bash pretrain.sh $idx $d_model $n_layer
EOF
done

# d_model=128
# n_layer=4
# log_file="hyena-dna-pretrain-"$max_idx"-"$d_model"-"$n_layer
# for idx in $(seq 0 $max_idx); do
# echo "bash misc/COS551/hyena-dna/pretrain.sh $idx"
# sbatch --output=slurm/%A_%a-%x.out -N 1 --ntasks-per-node $num_gpus --mem=128G --cpus-per-task 12  --gres=gpu:$num_gpus --mail-type=BEGIN,END,FAIL,TIME_LIMIT --mail-user=zwc.compute@yahoo.com --time 23:59:00 --job-name $log_file --signal USR1@180 -p "pli-c" <<EOF
# #!/bin/bash
# PORT=$(expr $RANDOM + 1000) bash pretrain.sh $idx $d_model $n_layer
# EOF
# done
