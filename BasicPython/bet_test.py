# Script to test that bet is callable from Python
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
    subprocess.check_output(['bet', 'struct.nii.gz', 'struct_bet.nii.gz'])
    os.chdir(top_dir)
