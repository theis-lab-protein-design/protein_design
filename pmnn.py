import os
import subprocess

folder_with_pdbs = "../inputs/PDB_monomers/pdbs/"

output_dir = "../outputs/example_1_outputs"
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

path_for_parsed_chains = os.path.join(output_dir, "parsed_pdbs.jsonl")

subprocess.run(["python", "./ProteinMPNN/helper_scripts/parse_multiple_chains.py", "--input_path", folder_with_pdbs, "--output_path", path_for_parsed_chains])

subprocess.run(["python", "./ProteinMPNN/protein_mpnn_run.py",
                "--jsonl_path", path_for_parsed_chains,
                "--out_folder", output_dir,
                "--num_seq_per_target", "2",
                "--sampling_temp", "0.1",
                "--seed", "37",
                "--batch_size", "1"])

import argparse

def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("folder", type=str, help="The folder to process")
    
    args = parser.parse_args()
    print(f"Processing folder: {args.folder}")

if __name__ == "__main__":
    main()
