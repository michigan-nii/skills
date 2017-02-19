import subprocess
import nipype.interfaces.fsl as fsl
import os

my_home = os.path.expanduser('~')
data_dir = os.path.join(my_home, 'nipype_tutorial', 'data')
os.chdir(data_dir)

id = 1

subject = 'sub' + str(id).zfill(3)
top_dir = os.getcwd()
os.chdir(subject)
mybet = fsl.BET(in_file='struct.nii.gz',
                out_file='struct_bet.nii.gz')
mybet.run()
os.chdir(top_dir)

###  Note, there are other ways to fill in the needed information,
###  some of which you might find more readable
###  Examples from
#    http://miykael.github.io/nipype-beginner-s-guide/firstSteps.html

# Method 2: specify parameters after node creation
# mybet = fsl.BET()
# mybet.inputs.in_file = 'struct.nii.gz'
# mybet.inputs.out_file = 'struct_bet.nii.gz'
# mybet.run()

# Method 3: specify parameters when the node is executed
# mybet = fsl.BET()
# mybet.run(in_file='struct.nii.gz',
#          out_file='struct_bet.nii.gz')
