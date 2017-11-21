# Adventures in public data

Trying to prepare examples to show people, I started getting a lot of errors
when running the CAT12 toolbox to do segmentation.  The errors were not
all the same,

```
------------------------------------------------------------------------
CAT Preprocessing error: CAT:cat_main:badTissueContrast: ./bennet/openfmri/MC2/derivatives/sub-01/func/coReg/T1w.nii 
------------------------------------------------------------------------
Bad tissue contrast (C=127.24, G=136.76, W=37.40)
```
and
```
------------------------------------------------------------------------
AMAP estimated untypical tissue peaks that point to an 
error in the preprocessing bevor the AMAP segmentation.
```
are a couple of examples.

Consulting with local experts (always handy to have around), we concluded this
might be an issue with where the origin of the images was set.  This led to
two questions.

1.  How do we quickly get the origin and other useful information from a set
    of images?

1.  What might be analogous to printing variable definitions and summaries for
    a 'regular' dataset?

## Shell based

Since I eventually want to be able to _easily_ run this over a whole set of
images, I want something that I can run from the command line in a loop.  That
leads me to a non-SPM tool, since SPM locks you into the Matlab framework
pretty hard and starting Matlab from the command line for a simple task
like this takes too much time&ndash;much more time than getting the information!

That leads me to FSL, possibly to AFNI, and definitely to Python.  I pick...FSL.

Turns out there are several ways to get the origin, and there are also several
origins that one could get.

> To go from voxel coordinates to more anatomically meaningful coordinates is
> the job of the qform and sform matrices that are stored in the NIfTI file.
> Note that these matrices only provide useful information if they have a
> non-zero code, since a zero code indicates that the matrix is "Unknown" and
> hence cannot be used. Having two matrices here is a common source of
> confusion. They were originally proposed so that two different coordinates
> could be kept track of - one representing the scanner coordinate system (the
> real space inside the scanner bore) and the other one relating to standard
> space coordinates (e.g. MNI152). However, in practice, it is rare that both
> contain different information as they are often set to be the same, or one
> of them is "Unknown" in which case the other contains all the useful
> information.
`https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Orientation Explained`

While this might not be totally important if you are collecting and processing
your own data, it might be important if you get someone else's.

So, first job is to figure out how to get them both.  FSL has the `fslorient`
command, which has options to get and set both the sform and qform
orientations.

```
$ pwd
/home/bennet/openfmri/MC2/subjects

$ image=sub-21/func/run_02/run_02.nii

$ fslorient -getsform
3 0 0 -94.5 0 3 0 -101.006 0 0 4 -99.6867 0 0 0 1

$ fslorient -getqform
3 0 0 -94.5 0 3 0 -101.006 0 0 4 -99.6867 0 0 0 1
```
They both print the affine transformation matrix as a vector, so those are
equivalent to

```
 3  0  0  -94.5
 0  3  0  -101.006
 0  0  4  -99.6867
 0  0  0  1
```
If we want to verify that the `sform` and `qform` are equal, we could put the
output of `-fslorient` for each type into strings and compare the strings.

```
sform=$(fslorient -getsform $image)
qform=$(fslorient -getqform $image)

if [ "$sform" == "$qform" ] ; then
    echo sform and qform equal
else
    echo sform and qform not equal
    echo sform:  $sform
    echo qform:  $qform
fi
```

Finally, let's go ahead and put that into a loop to check all the subjects.

```
for image in sub-??/func/run_0[12]/run_0[12].nii ; do
    echo $image
    sform=$(fslorient -getsform $image)
    qform=$(fslorient -getqform $image)

    if [ "$sform" == "$qform" ] ; then
        echo sform and qform equal
    else
        echo sform and qform not equal
        echo sform:  $sform
        echo qform:  $qform
    fi
done
```
Sometimes you will get a bunch of output that says they are equal.  If you get
something like

```
sform and qform not equal
sform: 3 -0.00107336 0.00305605 -96.6988 0.00107038 3 0.00526595 -106.932 -0.00229347 -0.00394857 4 -81.7054 0 0 0 1
qform: 3 0 0 -96.6687 0 3 0 -106.789 0 0 4 -81.6145 0 0 0 1
```
you might want to stop and figure out why!  (If you look closely at the one
above, you'll see that the differences are very small, so this may be some
form of round-off error.  Does that matter?)

Now let's try it with an anatomical image.

```
$ anatomical=sub-01/anat/T1w.nii

$ fslorient -getsform $anatomical
-1 -0 -0 0 -0 1 -0 -127.5 0 0 1 -127.5 0 0 0 1

$ fslorient -getqform $anatomical
-1 -0 -0 0 -0 1 -0 -127.5 0 0 1 -127.5 0 0 0 1
```

As you can see, fMRI software is strange and interesting....  What is -0?  But,
we don't care about all the fields, just every fourth one, and those are equal.
But, are they sensible?  Why is the _x_-coordinate origin at 0 (fourth element)?

Again after consulting with the local expert, we should try resetting the
origin(s) to the center of the image, and wherever that is, none of its
coordinates should be 0 (with or without the sign).

We can get the _x_, _y_, and _z_ coordinates from

```
$ fslhd -x $anatomical | egrep 'nx|ny|nz'
  nx = '176'
  ny = '256'
  nz = '256'
```
and if we do some arithmetic, we will find that halving each of those will
give us 88, 128, and 128, but the origin starts at `(0, 0, 0)`, so subtract
one, and the center should be at `(87, 127, 127)`.

Or should it?

Don't forget the sign.  We actually want those to match.  We think.

The `fslorient` command also has the `-setsform` and `-setqform` options, and
we want the `sform` and `qform` data to match.  So, we have to set the sign.
How do we do that?

Using the example above,

```
-1 -0 -0 0    -0 1 -0 -127.5     0 0 1 -127.5     0 0 0 1
```

we want to change the fourth element, so that should look like

```
-1 -0 -0 87   -0 1 -0 -127       0 0 1 -127       0 0 0 1
```

and we would use that with

```
$ fslorient -setsform -1 -0 -0 87 -0 1 -0 -127 0 0 1 -127 0 0 0 1
$ fslorient -setqform -1 -0 -0 87 -0 1 -0 -127 0 0 1 -127 0 0 0 1
```

Now, take my word for it, getting all those values out of the output using
just a shell script will be ugly and take much consultation with the Goog.
If you are inclined not to believe me, we can show you an example, but you can
also try it.

So, instead, let's turn now to Python.

## Python based

The main Python library for manipulating the data in NIfTI images is Nibabel.
Scripts that will use Nibabel need to import it, and since NumPy is used to
manipulate the data in images, it's usually wise to import it also.  As we
saw above, the information we need is in the NIfTI header, so let's start
there.  Let's also start by kind of replicating what we have already done.

```
#!/usr/bin/env python

from os.path import join as path_join
import numpy as np
import nibabel as nib

# Set path to subjects and image file
subjects = '/home/bennet/openfmri/MC2/subjects'
image_file = path_join(subjects, 'sub-01/anat/T1w.nii')

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
```

We can get the affine matrix, and we can compare that with what we got
before, namely, the _x_-axis has origin at 0, which is almost certainly
Not Right[TM].

If in doubt about where the exact origin is, it is often safe to use the
center of the image, which might be off, but maybe not by a whole lot, so
it should be a reasonably good place for most coregistration, algorithms
to start matching images.

What do we need to find the center of the 'image'?  We need the dimensions of
the volumes, because the 'image' here will be a volume, not a slice.  Once
we know what the image dimensions are, then if we move in halfway, we'll be
about at the center of the image.

```
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
```

Oh, hang on, mate!  Look at the values we had:  0, -127.5, -127.5.  There's a
sign there!  Where does that come from?  Well, we heard a rumor that, if
we take the diagonal of the affine matrix, multiply it by -1, that will
give us the right sign for the sform matrix entries.  So, if we have this
sform matrix

```
  -1.    -0.    -0.     0. 
  -0.     1.    -0.  -127.5
   0.     0.     1.  -127.5
   0.     0.     0.     1. 
```

the diagonal will be `[-1, 1, 1]`, so the signs for the origin column will
be `[+, -, -]` after we reverse them.

Now we have the pieces:  We have a sign vector of `[+, -, -]` and we have
the centers (in absolute value) at `[x_ctr, y_ctr, z_ctr]`, and we can
calculate that by using

```
# Get the first three elements of the sform matrix diagonal and reverse sign
diag = sform.diagonal()[0:3] * -1

# Set the x-, y-, and z- centers to the correctly signed values for the center
[x_ctr, y_ctr, z_ctr] = diag * np.asarray([x_ctr, y_ctr, z_ctr])
print("New x center: {}   New y center: {}   New z center: {}\n".format(
           x_ctr, y_ctr, z_ctr))
```

Now we need to put those into the sform matrix and save it.

```
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
```

If it is safe to assume that the origin is within some distance of the center
of the image, which it should be somehow.  Then we could come up with something
fancier that would detect whether an image has an origin that is, say, _D_
units from the center.

```
# Allowed offset:  How many voxels away from center will we let the
# origin get before we reset to center?  This is the Euclidean distance
# so setting this to 10 implies that, if 100 >= x^2 + y^2 + z^2, the
# origin should be reset.
origin_offset = 10

# Get the current sform origin
sform_x, sform_y, sform_z = sform[0:3,3]

# Calculate the Euclidean distance from the center of the image
# of the current origin
origin_distance = sqrt((sform_x - x_ctr)**2 +
                       (sform_y - y_ctr)**2 +
                       (sform_z - z_ctr)**2)

# Calculate the distance from the center of each current origin
x_diff = abs(sform_x - x_ctr)
y_diff = abs(sform_y - y_ctr)
z_diff = abs(sform_z - z_ctr)

# If we are outside of the offset limits, print the current distances along the axes
if origin_distance > origin_offset:
    print("The x origin coordinate {:8.2f} is {:8.2f} voxels from center.".format(
          sform_x, x_diff))
    print("The y origin coordinate {:8.2f} is {:8.2f} voxels from center.".format(
          sform_y, y_diff))
    print("The z origin coordinate {:8.2f} is {:8.2f} voxels from center.".format(
          sform_z, z_diff))
```

Finally, we can check our work with

```
$ fslorient -getsform T1w_origin_reset.nii 
-1 -0 -0 87 -0 1 -0 -127 0 0 1 -127 0 0 0 1 

$ fslorient -getqform T1w_origin_reset.nii 
-1 0 -0 87 0 1 -0 -127 0 0 1 -127 0 0 0 1
```
