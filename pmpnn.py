import argparse
import os
import subprocess


def run_processes(input_path, output_dir, symmetry=True):
    """
    Run subprocesses to process PDB files and run a prediction model.

    Args:
    input_path (str): Path to the input directory containing PDB files.
    output_dir (str): Path where the outputs will be saved.
    """
    # Ensure the output directory exists
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Set up the path for the output JSONL file
    path_for_parsed_chains = os.path.join(output_dir, "parsed_pdbs.jsonl")
    path_for_tied_positions = os.path.join(output_dir, "tied_pdbs.jsonl")

    # Run the parsing script
    subprocess.run(
        [
            "python",
            "./modules/ProteinMPNN/helper_scripts/parse_multiple_chains.py",
            "--input_path",
            input_path,
            "--output_path",
            path_for_parsed_chains,
        ]
    )
    if symmetry:
        subprocess.run(
            [
                "python",
                "./modules/ProteinMPNN/helper_scripts/make_tied_positions_dict.py",
                "--input_path",
                path_for_parsed_chains,
                "--output_path",
                path_for_tied_positions,
                "--homooligomer",
                "1",
            ]
        )

        # Run the prediction model script
        subprocess.run(
            [
                "python",
                "./modules/ProteinMPNN/protein_mpnn_run.py",
                "--jsonl_path",
                path_for_parsed_chains,
                "--tied_positions_jsonl",
                path_for_tied_positions,
                "--out_folder",
                output_dir,
                "--num_seq_per_target",
                "10",
                "--sampling_temp",
                "0.2",
                "--seed",
                "37",
                "--batch_size",
                "10",
            ]
        )
    else:
        # Run the prediction model script
        subprocess.run(
            [
                "python",
                "./modules/ProteinMPNN/protein_mpnn_run.py",
                "--jsonl_path",
                path_for_parsed_chains,
                "--out_folder",
                output_dir,
                "--num_seq_per_target",
                "400",
                "--sampling_temp",
                "0.2",
                "--seed",
                "37",
                "--batch_size",
                "10",
            ]
        )


def main(input_path, output_path, symmetry=True):
    """
    Main function to process PDB files and predict using a machine learning model.

    Args:
    input_path (str): Directory containing the input PDB files.
    output_path (str): Directory where the outputs will be saved.
    """
    run_processes(input_path, output_path, symmetry=symmetry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDB files and predict outcomes.")
    parser.add_argument("input_path", type=str, help="Directory containing the input PDB files.")
    parser.add_argument("output_path", type=str, help="Directory where the outputs will be saved.")
    parser.add_argument("symmetry", type=bool, help="Directory where the outputs will be saved.", default=True)

    args = parser.parse_args()

    # Call main function using arguments from the command line
    main(args.input_path, args.output_path)
