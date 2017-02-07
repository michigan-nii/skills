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

We can define a variable

We can get fancier with our functions by making them able to read values
when we use them.  Consider this definition,

```
def my_something(thing):
    print("My {} is mine, not yours!").format(thing)
```

That will be very useful.

glob
what's a dictionary
  keys :  values
get header information from .nii files in several folders
