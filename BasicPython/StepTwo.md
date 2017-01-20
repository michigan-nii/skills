# Getting started with libraries and file and folder information

## Libraries

Python has a lot of built-in functionality, but it tends to be at a fairly
low-level.  That is, all the tools you need to get work done are there,
but they aren't alway packaged conveniently.  Python uses _libraries_
(sometimes referred to as _modules_) to create additional commands (or
functions) that make life easier for you.

We will introduce libraries and their use with a library that makes
interacting with operating system functions easier, including moving
around in folders, getting information about files, etc.

## Using a library

To use a library, you _import_ it.  The library we will start with is
the `os` library.

```python
import os
```

That gives us access to the functions included in `os` by referring to them
by name.  So, for example, to find out what directory your program is
running in, use

```python
>>> os.getcwd()
'/Users/grundoon'
```

Here, the result of asking for the name of the current directory is just
printed, but we can save it in a variable, too.

```python
>>> current_folder = os.getcwd()
>>> type(current_folder)
<type 'str'>
>>> print current_folder
'/Users/grundoon'
```

The library is called `os`, and `getcwd()` is a function in the library,
and `getcwd` is a name in the library.  Each library creates its own
_namespace_, which makes it possible to have two functions with the same
name that do different things without confusing Python about which to use.
Names can also be defined further along, as in `os.path.join()`.

## Making a folder hierarchy

One thing you might want to do is to create the folder hierarchy for
a subject ahead of time so you can be sure that all the folders exist
before you try to use them.  This could be called _intializing_ a
subject's folder structure.  To keep things simple, we'll use a fake
directory structure that looks a bit like that from the fMRI Lab.

For each subject, let's say the folder structure look like this

```
[subjectID]/
    anatomy/
        t1overlay_43sl/
        t1spgr_156sl/
    func/
        task1/
        task2/
    raw/
        pfiles/
        physio/
```

and we want to create this structure for three subjects, `subj001`,
`subj002`, `subj003`.

## Creating programs

When writing a program, I find it useful to first write a template
that just prints out what will happen.  That way I can get something
that runs, make sure that it will do things in the right order, etc.
Once that is done, the print statements can be replaced by functions
that do the work instead of just talking about it.  During the course
of writing a program, I will almost always go back and forth between
those, as doing a step may sometimes reveal other steps that weren't
thought of until I started.  So, let's outline what we want to do.

First, we need to make a list of our `subjectID`s because we're going
to make a folder structure for each of them.  (We did this at the end
of the previous step).  We need to create a folder for each subject.
We need to make a list of the folders that go into each subject, and
for each of those, another list of its folders.  So we have 5 lists,
right?  One of subjects, one of the folders that go into the subject
folder, and for each of those, a list of its subfolders.

### Lists

In StepOne, we used a list, but we didn't really talk about it.
Remember, we used the `range()` function?

```python
 >>> type(range(5))
list
```

The list produced by `range()` is a list of integers.  Lists can
hold other things, and they don't even have to be the same type
of thing.  For the moment, though, the important thing is that a
list contains one or more things, and we have a way to say "do
something to everything in this list."  Let's make the lists of
folders that we want to create.  From StepOne, we printed some
subject IDs.  Let's modify that so it creates a list of them,
instead.

```python
subjIDs = []
for id in range(3):
    subjID = 'subj{:03d}'.format(id)
    subjIDs.append(subjID)
```

What does that do?  Well, it would be nice if it actually told us, so
let's introduce comments.  Comments in Python scripts/programs begin with
a `#` character.  Anything after the `#` to the end of the line is
a comment and is not processed by Python.  Comments are used to explain
what your code does.  Most often, you're explaining it to yourself after
you've not looked at it for a while, so it's good to think of comments
as a form of self-help as well as being a help to whoever else uses your
program

```python
# Create an empty list for subject IDs
subjIDs = []

# Make a list of subject IDs from 1 to 3
for id in range(3):
    # Format the subjID so it has leading zeros
    subjID = 'subj{:03d}'.format(id)
    # Add this subject ID to the end of the list
    subjIDs.append(subjID)
print subjIDs
```

If you run that, you'll see that something's wrong.  Yeah, yeah.  So,
Python starts things at 0 not 1, so to get what we want, we have to
adjust that.  We can do it in at least two ways.  We can add 1 to
all the numbers produced by `range()`.

```python
for id in range(3):
    subjID = 'subj{:03d}'.format(id + 1)
    subjIDs.append(subjID)
```

or we can tell range to start and end somewhere else.  If we want
`range()` to start at 1, we need to adjust the stopping point by
1 also.

```python
for id in range(1,4):
    subjID = 'subj{:03d}'.format(id)
    subjIDs.append(subjID)
```

Those should both produce a list of subjects from `001` to `003`.

That's one way to make a list.  Another is just to..., well, list
the elements.

```python
raw_dirs = [ 'pfiles', 'physio' ]
```

The square brackets tell Python that the thing being created is
a list.  So, let's just move on and create the rest

```python
anat_dirs = [ 't1overlay_43sl', 't1spgr_156sl' ]
func_dirs = [ 'task1', 'task2' ]
```

We're making some progress.  We have several lists, so now let's
glue our lists together.  To do something once for each element of
a list, we have the `for` command.  Remember, _indentation matters_!
We can put one `for` inside another, inside another.  Let's just do
the first two.

```python
for subject in subjIDs:
    print "Working on subject", subject
    for subdir in [ 'anat', 'func' ]:
        print "Working on", subdir
```

and running that will give us

```
Working on subject subj001
Working on anat
Working on func
Working on subject subj002
Working on anat
Working on func
Working on subject subj003
Working on anat
Working on func
```

