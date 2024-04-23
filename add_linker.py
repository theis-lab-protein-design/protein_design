import argparse
import os
import sys
from pathlib import Path


def convert_fasta(input_file, output_file, spacer="G" * 25):
    # Read the sequences from the input file
    sequences = []
    current_seq = ""
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    header = lines[0]
    for line in lines:
        if line.startswith(">"):
            if current_seq:
                sequences.append(current_seq)
                current_seq = ""
        else:
            current_seq += line.strip()
    if current_seq:
        sequences.append(current_seq)

    # Combine the sequences with the spacer
    combined_sequence = spacer.join(sequences)

    # Write the combined sequence to the output file
    with open(output_file, "w") as f:
        f.write(f"{header}\n")
        f.write(combined_sequence + "\n")


if __name__ == "__main__":
    # use os to change the working directory to this files directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="Parse .fa file and make it a linked sequence.")
    parser.add_argument("-i", "--input", help="Path to the input .fa file or folder with .fa files", required=False)
    parser.add_argument("-o", "--output", help="Path to the output folder", default=None, required=False)

    # Add default values for input_file and output_file
    parser.set_defaults(
        input="/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs_best/trimer",
        output="/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs_best/trimer_linker",
    )

    args = parser.parse_args()
    # check if input is a folder
    _input = Path(args.input)
    if _input.is_dir():
        fasta_files = [f for f in _input.iterdir() if f.suffix in [".fasta", ".fa"]]
    else:
        # input is a single file
        fasta_files = [args.input]

    args.output = Path(args.output)
    args.output.mkdir(parents=True, exist_ok=True)

    for i, f in enumerate(fasta_files):
        o = args.output / f"{f.stem}.fasta"
        convert_fasta(f, o)
        sys.stdout.write(f"Sequences {i:5}/{len(fasta_files):5} done.\n")
        sys.stdout.flush()
