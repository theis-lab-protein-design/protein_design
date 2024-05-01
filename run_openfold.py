import argparse
from pathlib import Path

from create_empty_msas import main as create_empty_msas
from debug_openfold import run_prediction as run_openfold


def main(fasta_dir, output_dir, config_preset="model_1_multimer_v3"):
    FASTA_DIR = Path(fasta_dir)
    assert FASTA_DIR.is_dir(), f"Directory {FASTA_DIR} does not exist"

    setting = FASTA_DIR.stem
    OUTPUT_OPENFOLD = Path(output_dir) / f"openfold_{setting}"

    create_empty_msas(str(FASTA_DIR), str(OUTPUT_OPENFOLD / "alignments"))

    run_openfold(
        fasta_dir=str(FASTA_DIR),
        use_precomputed_alignments=str(OUTPUT_OPENFOLD / "alignments"),
        config_preset=config_preset,
        model_device="cuda:0",
        output_dir=str(OUTPUT_OPENFOLD),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fasta_dir",
        type=str,
        help="Path to directory containing FASTA files, one sequence per file",
        default="/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs_best/homomer",
    )
    parser.add_argument("--output_dir", type=str, default=".")
    parser.add_argument("--config_preset", type=str, default="model_1_multimer_v3")

    args = parser.parse_args()
    main(args.fasta_dir, args.output_dir, args.config_preset)
