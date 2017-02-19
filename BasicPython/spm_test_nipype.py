import nipype.interfaces.spm as spm
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
input_file = 'run001.nii'
subprocess.check_output(['gunzip', '-k', input_file + '.gz'])
smooth = spm.Smooth()
smooth.inputs.in_files = input_file
smooth.inputs.fwhm = [8, 8, 8]
smooth.run()
subprocess.check_output(['gzip', 's' + input_file])
os.remove(input_file)
os.chdir(top_dir)

# You may get this message if you run this more than once.  How do you
#   want to handle it?
# gzip: srun001.nii.gz already exists; do you wish to overwrite (y or n)? y
