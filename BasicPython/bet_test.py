# Script to test that bet is callable from Python
import subprocess
import os

my_home = os.path.expanduser('~')
data_dir = os.path.join(my_home, 'nipype_tutorial', 'data')
os.chdir(data_dir)

# Set ID number
id = 1

# Format subject directory string
subject = 'sub' + str(id).zfill(3)

# Save where we are, then go to subject folder
top_dir = os.getcwd()
os.chdir(subject)
# Do work
bet_output = subprocess.check_output(['bet', 'struct.nii.gz', 'struct_bet.nii.gz', '-v'])
print(bet_output)

# Return to top
os.chdir(top_dir)
