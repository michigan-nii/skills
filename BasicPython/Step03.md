# Getting information out of a NIfTI file

In this step, our goal is to extract the information from the header of
at least one NIfTI (I'm just going to use nifti from now on) format file.
We have to learn some other things first, though.

## Creating new functions

In the last episode, we saw some ways to create folders and move around
in them from within our Python program.  The way we left things, we had
written Python in a `try...except` block that we could use to create
a new folder that would also do the right thing if one existed (or mostly
the right thing).  To use it more than once, we have to copy a bunch of
lines around.  If we do that, we are making it easy to introduce typos
and other kinds of error into our program, so we're going to turn that
into something we can reuse by typing `mk_my_dir()`.  Before we get to
that, we need to know how to write a new function.

### Writing functions, part 1

Simple functions just do something.  They don't take any input and they
don't produce any output.  One example of a function like that is the
`sys.exit` function that we imported in the last episode as `bail_out`
(mostly to show you how to import single functions from a library and
how to rename them).  We _define_ functions using the `def` statement,
and here's an example.

```python
def my_world():
    print("My world, and welcome to it.")
```

Just the `def` statement, the name of the new function (with parentheses),
and what it does.  If you do that from the Python prompt, you get

```python
>>> def my_world():
...     print("My world, and welcome to it.")
... 
>>> my_world()
My world, and welcome to it.
```

You might use something like that to print the name and version of your
program when it starts, for example, so that's not an entirely useless
example.  

We can define a function called, say `up_one()` that simply changes up
one directory level.  We can only do that because the name for "up one level"
is always defined and is always the same.

```
def up_one():
    parent = '..'
    os.chdir(parent)
```

What happens if `os` wasn't imported?  Try it.

This is where a try can come in handy.

```
try:
    os.chdir('..')
except NameError:
    import os
    os.chdir('..')
```
    
I cheated and tried it first.  That reported the following scary
message.

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'os' is not defined
```
We can get fancier with our functions by making them able to read values
when we use them.  Consider this definition,

```
def my_something(thing):
    print("My {} is mine, not yours!").format(thing)
```

That will be very useful.

Go to

http://nipy.org/nibabel/coordinate_systems.html

and download `someones_epi.nii.gz`

http://nipy.org/nibabel/_downloads/someones_epi.nii.gz

Here is an example of reading an `.nii` file (and some other
things).  For the moment, let's just go through the first block.

[  Install `nibabel`  ]

```
import nibabel as nib
epi_img = nib.load('Downloads/someones_epi.nii.gz')
epi_img_data = epi_img.get_data()
epi_img_data.shape
epi_img_header = epi_img.header
```

For this to work, you must use IPython, not just regular python.
That should Just Work if you are on the Skills machine and using
VNC.

```
import matplotlib.pyplot as plt

def show_slices(slices):
   """ Function to display row of image slices """
   fig, axes = plt.subplots(1, len(slices))
   for i, slice in enumerate(slices):
       axes[i].imshow(slice.T, cmap="gray", origin="lower")

slice_0 = epi_img_data[26, :, :]
slice_1 = epi_img_data[:, 30, :]
slice_2 = epi_img_data[:, :, 16]
show_slices([slice_0, slice_1, slice_2])
plt.suptitle("Center slices for EPI image")
```



Let's look at the header of an image

See http://nipy.org/nibabel/nibabel_images.html

```
import os
import numpy as np
from nibabel.testing import data_path
example_file = os.path.join(data_path, 'example4d.nii.gz')
import nibabel as nib
img = nib.load(example_file)
header = img.header
header['descrip']
print(header['descrip'])
```

what's a dictionary
  keys :  values

Project:  Get header information from `.nii` files in several folders with
one program.  Your program should change to at least one folder different
from where it started, read at least two `.nii` files, and print the `dim`
and `descrip` fields from the header.  Optionally, you can find the middle
slice in each dimension and print them.
