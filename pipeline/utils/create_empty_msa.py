import os
from pathlib import Path
import argparse


def read_fasta(fasta_file):
    """Parses a FASTA file and returns a list of tuples with sequence identifiers and sequences"""
    with open(fasta_file, "r") as file:
        fasta_entries = []
        identifier = ""
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if identifier:
                    fasta_entries.append((identifier, sequence, comment))
                identifier = line[1:].split("|")[0].strip()
                comment = line[1:].split("|")[1].strip()
                sequence = ""
            else:
                sequence += line
        if identifier:
            fasta_entries.append((identifier, sequence, comment))
    return fasta_entries


def create_directory_structure(base_dir, seq_name, sequence_entries):
    """Creates directories for each sequence in the list"""
    path = os.path.join(base_dir, seq_name, "msa")
    for identifier, _, _ in sequence_entries:
        sub_dir = os.path.join(path, identifier.split("-")[-1])
        os.makedirs(sub_dir, exist_ok=True)
        yield sub_dir, identifier


def write_a3m_file(directory, identifier, sequence, comment):
    file_path = os.path.join(directory, "bfd_uniref_hits.a3m")
    with open(file_path, "w") as file:
        file.write(f">{identifier} | {comment}\n{sequence}\n")


def write_sto_file(directory, identifier, sequence, comment, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as file:
        file.write("# STOCKHOLM 1.0\n\n")
        file.write(f"#=GS {identifier:<28} DE | {comment}\n\n")
        file.write(f"GS {identifier:<30} {sequence}\n")
        file.write(f"#= {'GC RF':<30} {'x'.join(['' for _ in sequence])}\n")
        file.write("//\n")


def main(fasta_dir, output_dir):
    fasta_dir = Path(fasta_dir)
    assert fasta_dir.is_dir(), f"Directory {fasta_dir} does not exist"
    for fasta_file in fasta_dir.glob("*.fasta"):
        seq_name = fasta_file.stem
        fasta_entries = read_fasta(fasta_file)
        for directory, identifier in create_directory_structure(output_dir, seq_name, fasta_entries):
            sequence, comment = next((seq, com) for id_seq, seq, com in fasta_entries if id_seq == identifier)
            write_a3m_file(directory, identifier, sequence, comment)
            write_sto_file(directory, identifier, sequence, comment, "mgnify_hits.sto")
            write_sto_file(directory, identifier, sequence, comment, "uniref90_hits.sto")


# Example usage
# main('path/to/your/seq_name.fasta', 'path/to/output/directory')
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fasta_dir",
        type=str,
        help="Path to directory containing FASTA files, one sequence per file",
        default="/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs_best/homomer",
    )
    parser.add_argument("--output_dir", type=str, default=".")
    # FASTA_DIR = "/nfs/homedirs/hetzell/code/protein_design/example_outputs/proteinmpnn/seqs_best/homomer/best_homomer_C8_oligo_0_0.fasta"
    args = parser.parse_args()
    main(args.fasta_dir, args.output_dir)