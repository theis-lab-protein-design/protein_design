#!/bin/bash
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu_all
#SBATCH -t 0-05:00
#SBATCH --mem=32000
#SBATCH --qos=students
#SBATCH --cpus-per-task=2
#SBATCH -o "./outputs/openfold_slurm-%j.out"

folder_with_pdbs="./example_outputs/C8/pdbs"

output_dir="./example_outputs/proteinmpnn"
if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi


path_for_parsed_chains=$output_dir"/parsed_pdbs.jsonl"
path_for_tied_positions=$output_dir"/tied_pdbs.jsonl"
path_for_designed_sequences=$output_dir"/temp_0.1"

python ./modules/ProteinMPNN/helper_scripts/parse_multiple_chains.py --input_path=$folder_with_pdbs --output_path=$path_for_parsed_chains

python ./modules/ProteinMPNN/helper_scripts/make_tied_positions_dict.py --input_path=$path_for_parsed_chains --output_path=$path_for_tied_positions --homooligomer 1

python ./modules/ProteinMPNN/protein_mpnn_run.py \
        --jsonl_path $path_for_parsed_chains \
        --tied_positions_jsonl $path_for_tied_positions \
        --out_folder $output_dir \
        --num_seq_per_target 2 \
        --sampling_temp "0.2" \
        --seed 37 \
        --batch_size 1
