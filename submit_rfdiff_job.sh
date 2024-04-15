#!/bin/bash

#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu_all
#SBATCH -t 1-00:00
#SBATCH --mem=32000
#SBATCH --qos=students
#SBATCH --cpus-per-task=2
#SBATCH -o "./outputs/slurm-%j.out"

cd ${SLURM_SUBMIT_DIR}
echo "Starting job ${SLURM_JOBID}"
echo "Date: $(date)"
echo "SLURM assigned me these nodes:"
squeue -j ${SLURM_JOBID} -O nodelist | tail -n +2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate leon_test 

python ./modules/RFdiffusion/scripts/run_inference.py --config-name symmetry  inference.symmetry=tetrahedral 'contigmap.contigs=[360-360]' inference.output_prefix=test_sample/tetrahedral inference.num_designs=1
