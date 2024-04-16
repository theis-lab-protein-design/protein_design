import os
import shutil

# Specify the directory to scan and the suffix to look for
directory_path = '/nfs/homedirs/hetzell/code/protein_design/example_outputs/C8'
suffix = '.pdb'
subfolder_name = 'pdbs'

# Create the subfolder path
subfolder_path = os.path.join(directory_path, subfolder_name)

# Create the subfolder if it doesn't already exist
if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

# Loop through all the files in the directory
for filename in os.listdir(directory_path):
    # Check if the file has the specified suffix
    if filename.endswith(suffix):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        
        # Construct the destination path in the subfolder
        destination_path = os.path.join(subfolder_path, filename)
        
        # Move the file to the subfolder
        shutil.move(file_path, destination_path)

print("Files with suffix '{}' have been moved to the subfolder '{}'.".format(suffix, subfolder_name))