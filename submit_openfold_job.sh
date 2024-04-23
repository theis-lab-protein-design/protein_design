#!/bin/bash

#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu_all
#SBATCH -t 0-05:00
#SBATCH --mem=32000
#SBATCH --qos=students
#SBATCH --cpus-per-task=2
#SBATCH -o "./outputs/openfold_slurm-%j.out"

# cd ${SLURM_SUBMIT_DIR}
# echo "Starting job ${SLURM_JOBID}"
# echo "Date: $(date)"
# echo "SLURM assigned me these nodes:"
# squeue -j ${SLURM_JOBID} -O nodelist | tail -n +2

# CONDA_BASE=$(conda info --base)
# source $CONDA_BASE/etc/profile.d/conda.sh
# conda activate protein-design-env
AF_DATABASE=/ceph/hdd/shared/hetzel_alphafold_database

BASE_PATH=/nfs/homedirs/hetzell/code/protein_design
FASTA_DIR=$BASE_PATH/example_outputs/proteinmpnn/seqs_best/trimer_linker
OUTPUT_DIR=$BASE_PATH/example_outputs/openfold_output_trimer_linker

python $BASE_PATH/create_empty_msas.py --fasta_dir $FASTA_DIR --output_dir $OUTPUT_DIR/alignments

python $BASE_PATH/modules/openfold/run_pretrained_openfold.py \
    $FASTA_DIR \
    $AF_DATABASE/pdb_mmcif/mmcif_files/ \
    --use_precomputed_alignments $OUTPUT_DIR/alignments\
    --uniref90_database_path $AF_DATABASE/uniref90/uniref90.fasta \
    --mgnify_database_path $AF_DATABASE/mgnify/mgy_clusters_2022_05.fa \
    --pdb70_database_path $AF_DATABASE/pdb70/pdb70 \
    --uniclust30_database_path $AF_DATABASE/uniclust30/uniclust30_2018_08/uniclust30_2018_08 \
    --bfd_database_path $AF_DATABASE/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
    --jackhmmer_binary_path /nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/jackhmmer \
    --hhblits_binary_path /nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/hhblits \
    --hhsearch_binary_path /nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/hhsearch \
    --kalign_binary_path /nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/kalign \
    --config_preset "model_1" \
    --model_device "cuda:0" \
    --output_dir $OUTPUT_DIR \
    # --config_preset "model_1_multimer_v3" \
    # --jax_param_path $BASE_PATH/modules/openfold/openfold/resources/params \
    # --openfold_checkpoint_path $BASE_PATH/modules/openfold/openfold/resources/openfold_params/finetuning_ptm_2.pt

