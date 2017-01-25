# String things

If you look at the filenames for the images that come from the fMRI
lab, you'll see that the name change from one preprocessing step to
the next is by addition of a letter to the front of the name.  The
names are
```python
    run.nii
    prun.nii
    tprun.nii
    rtprun.nii
```

```python
for i in range(1,5):
    subjID = ???  # fill this in
    input_file = 'run.nii'
    output_file = ??? + input_file  # fill this in
    folder = './func/task/run_01/' + subjID
    # construct a print statement that will print the full path
    # with folder stating that it is converting the input to
    # the output
    print(" ??? ").format( ??? )
```

Start `ipython`, and when you get a prompt, create a string variable,

```python
subjID = 'subj001'
```

now, use the Tab feature to look at the list of _methods_ that it has.
Methods are the actions that an object (here, the object is a string with
the name`subjID`) can perform on itself because it's a particular kind of
thing -- a string.  In some places you'll see them called functions.  Get
used to the jargon being kind of loose, except when it's to the writer's
advantage to be precise and officious.

You should see some of these

```python
subjID.count   subjID.find   subjID.format   subjID.split   subjID.strip
```

If you search the web for `python string methods`, you'll find a reference to

https://docs.python.org/2/library/stdtypes.html

Search on that page for `str.split`, for example, to see what it does.

Strings, like our `subjID` are a collection of things, and they have a
length

```python
len(subjID)
```

The characters can be referred to by position, so `subjID[0]` is `s`.
Try this
```python
for position in range(len(subjID)):
    print "Letter number {} is:  {}".format(position, subjID[position])
```
and see what you get.  Remember that.  Lots of things in Python are
going to be _indexed_ like that.

So, you went and read up on `str.split()`, right?  So, you should
have seen something like

str.split([sep[, maxsplit]])
  Return a list of the words in the string, using sep as the delimiter string.

Let's 'xperiment.

```python
In [16]: subjID.split(0)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-16-784c12e44b3b> in <module>()
----> 1 subjID.split(0)

TypeError: expected a string or other character buffer object

In [17]: subjID.split('0')
Out[17]: ['subj', '', '1']
```

So, that first error is because we used the number 0, and the
second is when we used the string '0'.  You got that, right?  What
did the `split()` do?  It made a list of the things on either side
of the _sep_, which was a '0' here.

What's that thing we got back from `subjID.split('0')`?  That's like
what we got back from `range(5)`

```python
In [18]: range(5)
Out[18]: [0, 1, 2, 3, 4]
```

The square brackets indicate that it's a _list_ of things, and the
things are strings because they have `''` around them.  We can put
that into a variable and see how big it is like this

```python
In [19]: split_string = subjID.split('0')

In [20]: len(split_string)
Out[20]: 3
```
and, even more neater, we can look at the elements with

```python
In [23]: for thing in range(len(split_string)):
    ...:     print "split_string[{}] is:  {}".format(thing, split_string[thing])
    ...:  
split_string[0] is:  subj
split_string[1] is:  
split_string[2] is:  1
```

So, the point of all that was to show that you can look at parts of
strings and lists by using an _index_.
