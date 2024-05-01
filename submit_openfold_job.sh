#!/bin/bash

#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu_large
#SBATCH -t 2-05:00
#SBATCH --mem=64000
#SBATCH --qos=phd
#SBATCH --cpus-per-task=8
#SBATCH -o "./outputs/openfold_slurm-%j.out"

cd ${SLURM_SUBMIT_DIR}
echo "Starting job ${SLURM_JOBID}"
echo "Date: $(date)"
echo "SLURM assigned me these nodes:"
squeue -j ${SLURM_JOBID} -O nodelist | tail -n +2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate protein-design-env

BASE_PATH=/nfs/homedirs/hetzell/code/protein_design
FASTA_DIR=$BASE_PATH/example_outputs/30Apr24_looping/protein_mpnn/seqs_best/homomer
# FASTA_DIR=$BASE_PATH/example_outputs/30Apr24_looping/protein_mpnn/seqs_best/trimer_linker
OUTPUT_DIR=$BASE_PATH/example_outputs/30Apr24_looping

python $BASE_PATH/run_openfold.py \
    --fasta_dir $FASTA_DIR \
    --output_dir $OUTPUT_DIR \
    # --config_preset "model_1" \
    --config_preset "model_3_multimer_v3" \
