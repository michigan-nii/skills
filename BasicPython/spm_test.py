# Script to test that Matlab/SPM is callable from Python
import subprocess
import os
import gzip

my_home = os.path.expanduser('~')
data_dir = os.path.join(my_home, 'nipype_tutorial', 'data')
os.chdir(data_dir)

id = 1

subject = 'sub' + str(id).zfill(3)
top_dir = os.getcwd()
os.chdir(subject)
# SPM can't use .gz files
subprocess.check_output(['gunzip', '-k', 'run001.nii.gz'])
###  Smooth an image to test SPM functionality from raw python
###  Note, the SPM command is broken into two parts just for
###    legibility in the script.
spm_command = "try, spm_smooth('run001.nii', 'srun001.nii', [8,8,8]), catch, "
spm_command = spm_command + "'Error running smooth',end; exit"
spm_smooth_output = subprocess.check_output(
    ['matlab', '-nodesktop', '-r', spm_command])
print(spm_smooth_output)
subprocess.check_output(['gzip', 'srun001.nii'])
os.remove('run001.nii')
os.chdir(top_dir)

# You may get this message if you run this more than once.  How do you
#   want to handle it?
# gzip: srun001.nii.gz already exists; do you wish to overwrite (y or n)? y
