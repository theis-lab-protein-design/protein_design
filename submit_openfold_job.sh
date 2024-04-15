#!/bin/bash

#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu_all
#SBATCH -t 0-05:00
#SBATCH --mem=32000
#SBATCH --qos=students
#SBATCH --cpus-per-task=2
#SBATCH -o "./outputs/openfold_slurm-%j.out"

cd ${SLURM_SUBMIT_DIR}
echo "Starting job ${SLURM_JOBID}"
echo "Date: $(date)"
echo "SLURM assigned me these nodes:"
squeue -j ${SLURM_JOBID} -O nodelist | tail -n +2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate leon_test 

python modules/openfold/run_pretrained_openfold.py \
    ./openfold_run/fasta_dir \
    /ceph/hdd/shared/hetzel_alphafold_database/pdb_mmcif/mmcif_files/ \
    --use_precomputed_alignments ./openfold_run/msa_dir \
    --uniref90_database_path /ceph/hdd/shared/hetzel_alphafold_database/uniref90/uniref.fasta \
    --mgnify_database_path /ceph/hdd/shared/hetzel_alphafold_database/mgnify/mgy_clusters_2018_12.fa \
    --pdb70_database_path /ceph/hdd/shared/hetzel_alphafold_database/pdb70/pdb70 \
    --uniclust30_database_path /ceph/hdd/shared/hetzel_alphafold_database/uniclust30/uniclust30_2018_08/uniclust30_2018_08 \
    --bfd_database_path /ceph/hdd/shared/hetzel_alphafold_database/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
    --jackhmmer_binary_path lib/conda/envs/leonoviny_env/bin/jackhmmer \
    --hhblits_binary_path lib/conda/envs/leonoviny_env/bin/hhblits \
    --hhsearch_binary_path lib/conda/envs/leonoviny_env/bin/hhsearch \
    --kalign_binary_path lib/conda/envs/leonoviny_env/bin/kalign \
    --config_preset "model_1_ptm" \
    --model_device "cuda:0" \
    --output_dir ./openfold_output \
    --openfold_checkpoint_path modules/openfold/openfold/resources/openfold_params/finetuning_ptm_2.pt

