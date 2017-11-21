#!/usr/bin/env python

from os.path import join as path_join
import numpy as np
import nibabel as nib

# Set path to subjects and image file
subjects = '/home/bennet/openfmri/ds101/subjects'
image_file = path_join(subjects, 'sub-01/anat/T1w.nii')
print("Image file:  {}\n".format(image_file))

# Load the image and extract the header
image = nib.load(image_file)
header = image.header

# Get the affine transform matrices
sform = header.get_sform()
qform = header.get_qform()

# Are the affines all the same or different?
sform_eq_qform = sform.all() == qform.all()
if sform_eq_qform == True:
    print("All affines are equal")
    print("Affine matrix")
    print(sform)
else:
    print("Affines are unequal")
    print("sform affine\n{}".format(sform))
    print("qform affine\n{}".format(qform))

# Get the image dimensions from the header
x_dim, y_dim, z_dim = header['dim'][1:4]
print("Image dimensions are: {}\n".format(str(header['dim'])))

# Calculate the coordinates for the center of the image
# 0-indexing and integer division, hence -1 and // instead of /
# (At least, I think that's right)
x_ctr = (x_dim-1)//2
y_ctr = (y_dim-1)//2
z_ctr = (z_dim-1)//2
print("x-center is: {}   y-center is: {}   z-center is: {}\n".format(
      x_ctr, y_ctr, z_ctr))

# Get the first three elements of the sform matrix diagonal and reverse sign
diag = sform.diagonal()[0:3] * -1

# Set the x-, y-, and z- centers to the correctly signed values for the center
[x_ctr, y_ctr, z_ctr] = diag * np.asarray([x_ctr, y_ctr, z_ctr])
print("New x center: {}   New y center: {}   New z center: {}\n".format(
           x_ctr, y_ctr, z_ctr))

print("Resetting the origin coordinates")
# Set the sform and qform entries we extracted to the new, corrected values
sform[0:3,3] = qform[0:3,3] = x_ctr, y_ctr, z_ctr

# Save them back to the image
image.set_sform(sform)
image.set_qform(qform)

# We have to create a new image file, and it's good not to overwrite original
# data anyway, isn't it?
new_image_file = image_file.replace('.nii', '_origin_reset.nii')
nib.save(image, new_image_file)

