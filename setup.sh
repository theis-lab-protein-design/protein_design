git submodule update --init --recursive
if ! command -v conda &> /dev/null
then
    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh
    ~/miniconda3/bin/conda init bash

    # Source the shell initialization script to apply Conda changes immediately
    # Adjust the path to the initialization script if necessary
    source ~/.bashrc
fi

if ! command -v mamba &> /dev/null
then
    conda install -y -n base --override-channels -c conda-forge mamba 'python_abi=*=*cp*'
fi


# Now that Conda is initialized in the current session, you can proceed with the rest
mamba env create -y environment.yml
mamba activate leonoviny_env
# pip install -e ./modules/ESM
# pip install -e ./modules/openfold
