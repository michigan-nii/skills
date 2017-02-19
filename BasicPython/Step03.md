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

```python
def up_one():
    parent = '..'
    os.chdir(parent)
```

What happens if `os` wasn't imported?  Try it.  I got

```python
>>> up_one()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in up_one
NameError: global name 'os' is not defined
```

This is where something called `try` can come in handy.  It's often
referred to as `try...except`, because not only do you tell it what
to try, you tell it what to do if it takes exception with you.  Notice
in the above, that the last line says: `NameError: global name 'os' not
defined`.  The _exception type_ is `NameError`, and the exception
message is the rest.  When we want Python to try something, we then
tell it what to do in the case of an exception, and we can do different
things depending on the type of exception.  

```python
try:
    os.chdir('..')
except NameError:
    import os
    os.chdir('..')
except:
    print("Something really bad happened, man!")
```
    
We can get fancier with our functions by making them able to read values
when we use them.  Consider this definition,

```python
def my_something(gizmo):
    print("My {} is mine, not yours!").format(gizmo)
```
```python
>>> my_something('heart')
My heart is mine, not yours!
```

Another place where `try...except` is useful is checking to make sure
that the right kind of value was given to a function.   For example,

```python
>>> def my_calc(x):
...      return x / 2.0
... 
>>> my_calc(2)
1.0
>>> my_calc('a')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in my_calc
TypeError: unsupported operand type(s) for /: 'str' and 'float'
```

So, we could make that function less _fragile_ if we put something
in to test for the type of variable.

```python
>>> def my_calc(x):
...     try:
...         return x/2.0
...     except TypeError:
...         print("Give me a number!")
...         return float('NaN')
... 
>>> my_calc('a')
Give me a number!
nan
>>> my_calc(4)
2.0
```

That `float('NaN')` should be recognizable to people who have used
Matlab.  It's Not A Number.  We return it so that, if we were saving
the result of `my_calc()`, it would cause the right kind of error if
it were used later.

Being able to give a function something to work on is very useful.
Boy, howdy, is it!

## Finally we get to an image

Go to

http://nipy.org/nibabel/coordinate_systems.html

and download `someones_epi.nii.gz`

http://nipy.org/nibabel/_downloads/someones_epi.nii.gz

We will assume that it will go into the `Downloads` folder and
be loadable from there.

Here is an example of reading an `.nii` file (and some other
things).  This presumes you're on a machine that has `nibabel`
installed.

```python
>>> import nibabel as nib
>>> epi_img = nib.load('Downloads/someones_epi.nii.gz')
>>> epi_img_data = epi_img.get_data()
>>> epi_img_data.shape
>>> epi_img_header = epi_img.header
>>> print(epi_img_header)
<class 'nibabel.nifti1.Nifti1Header'> object, endian='<'
sizeof_hdr      : 348
data_type       : 
db_name         : 
extents         : 0
session_error   : 0
regular         : 
dim_info        : 0
dim             : [ 3 53 61 33  1  1  1  1]
intent_p1       : 0.0
intent_p2       : 0.0
intent_p3       : 0.0
intent_code     : none
datatype        : uint8
bitpix          : 8
slice_start     : 0
pixdim          : [ 1.  3.  3.  3.  1.  1.  1.  1.]
vox_offset      : 0.0
scl_slope       : nan
scl_inter       : nan
slice_end       : 0
slice_code      : unknown
xyzt_units      : 2
cal_max         : 0.0
cal_min         : 0.0
slice_duration  : 0.0
toffset         : 0.0
glmax           : 0
glmin           : 0
descrip         : 
aux_file        : 
qform_code      : mni
sform_code      : mni
quatern_b       : 0.149438127875
quatern_c       : -0.0
quatern_d       : -0.0
qoffset_x       : -78.0
qoffset_y       : -76.0
qoffset_z       : -64.0
srow_x          : [  3.   0.   0. -78.]
srow_y          : [  0.           2.86600947  -0.88656062 -76.        ]
srow_z          : [  0.           0.88656062   2.86600947 -64.        ]
intent_name     : 
magic           : n+1
```

Is that science?!

So, quit your regular Python, and instead start your IPythons.
And, in addition, your IPython has to be able to open windows.
That should Just Work if you are on the Skills machine and using
VNC.

IPython uses a very different prompt.

```python
In [1]: 
```

IPython is also notorious for being badly behaved if you try to
copy and paste any indented Python commands into it.  If you want
to do that, you can use what is called a _magic_ (or maybe _magik_).

First, here is the code that we want to paste.  Copy just to the
blank line, then paste it.

```python
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
It will either double the size of the indents, or it will go
totally wacko with the indents.  To be safe, you use 

```python
In [1]: %cpaste
Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
:def show_slices(slices):
:   """ Function to display row of image slices """
:   fig, axes = plt.subplots(1, len(slices))
:   for i, slice in enumerate(slices):
:       axes[i].imshow(slice.T, cmap="gray", origin="lower")
:--
In [2]:
```

The `%` indicates it is magic.  Trust me, just do this.  Especially
if the chunk you're pasting has many indents.


We saw the full header of an image above, but it's much more likely
that you will only want some part of the header.  Here is some python
that will print just the description from the header of an
image that is included with `nibabel`.

```python
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

Note, that, in the example above, we're using that
`os.path.join()` function to create a path that will work whether
we're on Linux, Mac, or Windows.  We're also renaming the libraries
as we import them (or functions from them).  All of the muck at the
top is so we can do `img = nib.load(example_file)`, which is how
you read an image into Python.  The image has two parts, a header,
which we've seen, and data.  We extract the header from the `img` and
put it into its own variable.

See http://nipy.org/nibabel/nibabel_images.html



## Python dictionaries

We've seen that lists in Python can be used to collect multiple items into
one place and then use them, one after another.  An individual item can
only be referred to in a list by its position, commonly called its _index_.

Sometimes that's not such a hot idea.  One example where something else is
desirable is when the number of items is different depending on circumstances,
so the number of items changes, leaving gaps.  In one list, it might be
that the fourth item is the same as the sixth item in another list.  Python
uses _dicitionaries_ as the way to give each element a name -- the _key_ --
and that is used to access the _value_ associated with it.  They are sometimes
called _associative arrays_, and smattering your conversation with references
to _key-value pairs_ shows you're cool.

Just above, we saw how to get the values of items in a dictionary; like this

```python
print(header['descrip'])
```

In this case, the dictionary component is hidden behind something else, a
NiPy image object, but that's what it is.  In the case above, `header` would
be the name of the dictionary variable, and `descrip` is the name of the
entry.  These are very much like database fields.  OK, that's how we get
stuff out of one, how do we get stuff into one?  First, we need to tell
Python that we want a dictionary.

```python
header = {}
```
or
```python
header = dict()
```

Once it is created, you add things to it by specifying the key (name) in the
same way you would specify an index to a list -- in square brackets.  Suppose
we have the following information about a how images for a study were acquired.

> We obtained 146 contiguous echo planar imaging (EPI) whole-brain functional
volumes (TR=2000 ms; TE=30 ms; flip angle=80, 40 slices, matrix=64x64;
FOV=192 mm; acquisition voxel size=3x3x4mm) during each of the two flanker
task blocks.

> A high-resolution T1-weighted anatomical image was also acquired using a
magnetization prepared gradient echo sequence (MPRAGE, TR=2500 ms;
TE= 3.93 ms; TI=900 ms; flip angle=8; 176 slices, FOV=256 mm).

Now we want to put some of that into a dictionary so we can refer to it.

```python
>>> EPI_info = dict()
>>> EPI_info['TR'] = 2000
>>> EPI_info['TE'] = 30

>>> print(EPI_info['TE'])
30
>>> type(EPI_info['TE'])
int
```

That's all very well and good, so long as you have a record of what the
keys are somewhere, right?  You can get the keys present in a list with

```python
for key in EPI_info:
    print(key)
TE
TR
```

Note, though that the keys are not sorted, nor are they guaranteed to be
in any particular order.  If you want the keys to be sorted, you must
refer to them with `sorted(EPI_info.keys())`.

OK, your turn.  Write a little program that will created the `EPI_info`
dictionary above and print a list of the sorted keys and their values.

Project:  Get header information from `.nii` files in several folders with
one program.  Your program should change to at least one folder different
from where it started, read at least two `.nii` files, and print the `dim`
and `descrip` fields from the header.
