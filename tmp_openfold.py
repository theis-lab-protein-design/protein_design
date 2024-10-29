from pathlib import Path

from debug_openfold import run_prediction as run_openfold

if __name__ == "__main__":
    STEM = Path("/nfs/homedirs/hetzell/code/protein_design/example_outputs")
    FOLDER = STEM / "19Sep24_frameflow_design_symmetry"
    FASTA_DIR = FOLDER / "protein_mpnn" / "seqs_best" / "homomer"
    OUTPUT_OPENFOLD = FOLDER / "openfold_homomer"
    assert FASTA_DIR.exists()
    assert OUTPUT_OPENFOLD.exists()
    # run_openfold(
    #     fasta_dir=str(FASTA_DIR),
    #     use_precomputed_alignments=str(OUTPUT_OPENFOLD / "alignments"),
    #     config_preset="model_1",
    #     model_device="cuda:0",
    #     output_dir=str(OUTPUT_OPENFOLD),
    # )
    run_openfold(
        fasta_dir=str(FASTA_DIR),
        use_precomputed_alignments=str(OUTPUT_OPENFOLD / "alignments"),
        config_preset="model_1_multimer_v3",
        model_device="cuda:0",
        output_dir=str(OUTPUT_OPENFOLD),
    )
