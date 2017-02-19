#!/usr/bin/env python

import subprocess
import os

my_home = os.path.expanduser('~')
data_dir = os.path.join(my_home, 'nipype_tutorial', 'data')
os.chdir(data_dir)
id = 1

subject = 'sub' + str(id).zfill(3)
top_dir = os.getcwd()
os.chdir(subject)
if not os.path.isfile('struct_bet.nii.gz') \
   or os.path.getmtime('struct.nii.gz') > os.path.getmtime('struct_bet.nii.gz'):
    # stripped file does not exist or it is older than structural
    bet_output = subprocess.check_output(['bet', 'struct.nii.gz', 'struct_bet.nii.gz', '-v'])
    print(bet_output)
else:
    print("Nothing to be done: struct_bet.nii.gz up to date")
os.chdir(top_dir)
