import nipype.interfaces.spm as spm
import subprocess
import os
import gzip

my_home = os.path.expanduser('~')
data_dir = os.path.join(my_home, 'nipype_tutorial', 'data')
os.chdir(data_dir)
input_file = 'run002.nii'

for id in range(1,11):
    subject = 'sub' + str(id).zfill(3)
    top_dir = os.getcwd()
    os.chdir(subject)
    subprocess.check_output(['gunzip', '-k', input_file + '.gz'])
    smooth = spm.Smooth()
    smooth.inputs.in_files = input_file
    smooth.inputs.fwhm = [8, 8, 8]
    smooth.run()
    subprocess.check_output(['gzip', 's' + input_file])
    os.remove(input_file)
    os.chdir(top_dir)
