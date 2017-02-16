# Script to test that Matlab/SPM is callable from Python
import subprocess
import os
import gzip

my_home = os.path.expanduser('~')
data_dir = os.path.join(my_home, 'nipype_tutorial', 'data')
os.chdir(data_dir)

for id in range(1,11):
    subject = 'sub' + str(id).zfill(3)
    top_dir = os.getcwd()
    os.chdir(subject)
    subprocess.check_output(['gunzip', '-k', 'run001.nii.gz'])
    ###  Smooth an image to test SPM functionality from raw python
    spm_command = "try, spm_smooth('run001.nii', 'srun001.nii', [8,8,8]), catch, "
    spm_command = spm_command + "'Error running smooth',end; exit"
    spm_smooth_output = subprocess.check_output(
        ['matlab', '-nodesktop', '-r', spm_command])
    subprocess.check_output(['gzip', 'srun001.nii'])
    os.remove('run001.nii')
    os.chdir(top_dir)
