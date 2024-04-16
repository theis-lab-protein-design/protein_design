#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

import numpy as np


def check_path(path):
    path = Path(path)
    assert not path.exists(), f"Error: {path} already exists."


def write_fasta_file(seqs, output_file, meta_data: dict = None, stop_after=None):
    if meta_data is not None:
        assert "seq_name" in meta_data.keys(), "Error: meta_data must contain 'seq_name' key."
        assert "score" in meta_data.keys(), "Error: meta_data must contain 'score' key."

    if stop_after is None:
        stop_after = len(seqs)

    with open(output_file, "w") as f:
        for i, seq in enumerate(seqs):
            if i == stop_after:
                break
            # convert i to captial letter
            f.write(f"{meta_data['seq_name']}-{chr(i + 65)} | score={meta_data['score']}" + "\n")
            f.write(f"{seq}\n")


def parse_and_extract(input_file, output_folder=None, overwrite=False, add_monomer=True, add_trimer=True, n_seqs=1):
    try:
        with open(input_file, "r") as f:
            lines = f.readlines()

        input_file = Path(input_file)
        # get filename without extension
        input_file_name = input_file.stem
        if output_folder is None:
            # get folder of input_file
            output_folder = os.path.dirname(input_file)
        folder = Path(output_folder)
        # create folder if it does not exist
        output_file = folder / "homomer" / f"best_homomer_{input_file_name}.fasta"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not overwrite:
            check_path(output_file)

        # Remove "\n" from lines
        lines = [line.strip() for line in lines]
        header, seqs = lines[0], lines[2:]
        seq_name = header.split(",")[0]
        # Find the line with the best score
        # best_seq_desc = max([s for s in seqs if "score=" in s], key=lambda x: float(x.split("score=")[1].split(",")[0]))
        top_sequences_desc = sorted(
            [s for s in seqs if "score=" in s], key=lambda x: float(x.split("score=")[1].split(",")[0]), reverse=True
        )[:n_seqs]
        for i, seq_desc in enumerate(top_sequences_desc):
            score = seq_desc.split("score=")[1].split(",")[0]
            meta_data = {"seq_name": seq_name, "score": score}

            idx = (np.where(np.array(seqs) == np.array(seq_desc))[0] + 1)[0]
            best_seqs = seqs[idx].split("/")

            # Write the best sequence to the output file
            output_file = folder / "homomer" / f"best_homomer_{input_file_name}_{i}.fasta"
            write_fasta_file(best_seqs, output_file, meta_data=meta_data)
            if add_monomer:
                output_file = folder / "monomer" / f"best_monomer_{input_file_name}_{i}.fasta"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                if not overwrite:
                    check_path(output_file)
                write_fasta_file(best_seqs, output_file, meta_data=meta_data, stop_after=1)

            if add_trimer:
                output_file = folder / "trimer" / f"best_trimer_{input_file_name}_{i}.fasta"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                if not overwrite:
                    check_path(output_file)
                write_fasta_file(best_seqs, output_file, meta_data=meta_data, stop_after=3)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    # use os to change the working directory to this files directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="Parse .fa file for the best score and store the matching sequence.")
    parser.add_argument("-i", "--input", help="Path to the input .fa file or folder with .fa files", required=False)
    parser.add_argument("-o", "--output", help="Path to the output folder", default=None, required=False)

    # Add default values for input_file and output_file
    parser.set_defaults(
        input="/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs",
        output="/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs_best",
    )

    args = parser.parse_args()
    # check if input is a folder
    _input = Path(args.input)
    if _input.is_dir():
        fasta_files = [f for f in _input.iterdir() if f.suffix in [".fasta", ".fa"]]
    else:
        # input is a single file
        fasta_files = [args.input]
    for i, f in enumerate(fasta_files):
        parse_and_extract(f, args.output, overwrite=True, n_seqs=1)
        sys.stdout.write(f"Sequences {i:5}/{len(fasta_files):5} done.\n")
        sys.stdout.flush()
