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


