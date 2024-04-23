import argparse
import logging
import os

import torch

from create_empty_msas import main as create_empty_msas
from modules.openfold.run_pretrained_openfold import add_data_args
from modules.openfold.run_pretrained_openfold import main as run_pretrained_openfold


def run_prediction(
    fasta_dir,
    use_precomputed_alignments=None,
    use_single_seq_mode=False,
    output_dir=os.getcwd(),
    model_device="cpu",
    config_preset="model_1",
    jax_param_path=None,
    openfold_checkpoint_path=None,
    save_outputs=False,
    cpus=4,
    preset="full_dbs",
    output_postfix=None,
    data_random_seed=None,
    skip_relaxation=False,
    multimer_ri_gap=200,
    trace_model=False,
    subtract_plddt=False,
    long_sequence_inference=False,
    cif_output=False,
):
    af_database = "/ceph/hdd/shared/hetzel_alphafold_database"
    args = dict(
        fasta_dir=fasta_dir,
        template_mmcif_dir=os.path.join(af_database, "pdb_mmcif/mmcif_files"),
        use_precomputed_alignments=use_precomputed_alignments,
        use_single_seq_mode=use_single_seq_mode,
        output_dir=output_dir,
        model_device=model_device,
        config_preset=config_preset,
        jax_param_path=jax_param_path,
        openfold_checkpoint_path=openfold_checkpoint_path,
        save_outputs=save_outputs,
        cpus=cpus,
        preset=preset,
        output_postfix=output_postfix,
        data_random_seed=data_random_seed,
        skip_relaxation=skip_relaxation,
        multimer_ri_gap=multimer_ri_gap,
        trace_model=trace_model,
        subtract_plddt=subtract_plddt,
        long_sequence_inference=long_sequence_inference,
        cif_output=cif_output,
        uniref90_database_path=os.path.join(af_database, "uniref90/uniref90.fasta"),
        mgnify_database_path=os.path.join(af_database, "mgnify/mgy_clusters_2022_05.fa"),
        pdb70_database_path=os.path.join(af_database, "pdb70/pdb70"),
        uniclust30_database_path=os.path.join(af_database, "uniclust30/uniclust30_2018_08/uniclust30_2018_08"),
        bfd_database_path=os.path.join(af_database, "bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt"),
        jackhmmer_binary_path="/nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/jackhmmer",
        hhblits_binary_path="/nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/hhblits",
        hhsearch_binary_path="/nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/hhsearch",
        kalign_binary_path="/nfs/staff-hdd/hetzell/miniconda3/envs/protein-design-env/bin/kalign",
    )

    # Set the JAX parameter path if not specified and no checkpoint path is given
    if jax_param_path is None and openfold_checkpoint_path is None:
        jax_param_path = os.path.join(
            "modules", "openfold", "openfold", "resources", "params", f"params_{config_preset}.npz"
        )
    args["jax_param_path"] = jax_param_path
    # Warning if running on CPU while CUDA is available
    if model_device == "cpu" and torch.cuda.is_available():
        logging.warning("The model is being run on CPU. Consider specifying --model_device for better performance.")
    parser = argparse.ArgumentParser()
    add_data_args(parser)
    _args = parser.parse_args()
    # combine args and _args namespaces
    _args = vars(_args)

    # Update dict1 with dict2, overriding values from ns1 with ns2 where applicable
    args.update(_args)
    args = argparse.Namespace(**args)
    # Example of what main might do:
    run_pretrained_openfold(args)


# Setup environment variables and paths

base_path = "/nfs/homedirs/hetzell/code/protein_design"
# fasta_dir = os.path.join(base_path, "example_outputs/proteinmpnn/seqs_best/trimer_linker")
# output_dir = os.path.join(base_path, "example_outputs/openfold_output_trimer_linker")
fasta_dir = os.path.join(base_path, "example_outputs/linker_test/seq")
output_dir = os.path.join(base_path, "example_outputs/openfold_output_trimer_linker")
alignments_dir = os.path.join(output_dir, "alignments")

# Assuming create_empty_msas.py has been adjusted to provide a callable function
create_empty_msas(fasta_dir=fasta_dir, output_dir=alignments_dir)

# Assuming run_pretrained_openfold.py has been adapted to include callable functions
args = dict(
    fasta_dir=fasta_dir,
    use_precomputed_alignments=alignments_dir,
    config_preset="model_1",
    model_device="cuda:0",
    output_dir=output_dir,
)


# Example of calling the function
run_prediction(**args)
