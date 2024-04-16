git submodule update --init --recursive
# # if ! command -v mamba &> /dev/null
# # then
# #     echo "Mamba is not installed. Please install Mamba to continue."
# #     exit 1
# # fi


mamba create -y -n protein-design-env python=3.9
mamba env update -n protein-design-env --file environment3.yml

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate protein-design-env
pip install -e ./modules/openfold
pip install -e ./modules/ESM


#RF diffusion setup
chmod +x download_rf_diffusion.sh  
./download_rf_diffusion.sh
cd modules/RFdiffusion/env/SE3Transformer/ 
python setup.py install
cd ../..
pip install -e .
cd ../..

# bash scripts/download_alphafold_dbs.sh data/
bash scripts/download_openfold_params.sh openfold/resources
