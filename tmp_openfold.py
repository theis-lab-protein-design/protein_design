from pathlib import Path

from debug_openfold import run_prediction as run_openfold

if __name__ == "__main__":
    FASTA_DIR = Path(
        "/nfs/homedirs/hetzell/code/protein_design/example_outputs/25Jul24_dna_design_0.2/protein_mpnn/seqs_best/monomer"
    )
    OUTPUT_OPENFOLD = Path(
        "/nfs/homedirs/hetzell/code/protein_design/example_outputs/25Jul24_dna_design_0.2/openfold_monomer"
    )
    assert FASTA_DIR.exists()
    assert OUTPUT_OPENFOLD.exists()
    run_openfold(
        fasta_dir=str(FASTA_DIR),
        use_precomputed_alignments=str(OUTPUT_OPENFOLD / "alignments"),
        config_preset="model_1",
        model_device="cuda:0",
        output_dir=str(OUTPUT_OPENFOLD),
    )
