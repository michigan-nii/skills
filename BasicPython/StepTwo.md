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

At this point, we have to decide, do we add the final loop that we need
&ndash; the one that creates the folder inside each `anat` and `func` folder
&ndash; or do we first create the `anat` and `func` folders?  In future,
this will be a matter for personal preference, but to move things along,
let's create the `anat` and `func` folders now.

## Creating folders and changing to them

We found the `getcwd()` function in the `os` module, so that's a good place
to look for functions to make directories and change to them.  If you go to
the Python documentation web site for the `os` library,
https://docs.python.org/2/library/os.html
you can search for 'directory' and eventually find it.  If you know the
command to create directories in Linux or at the Windows command prompt,
you might search for 'mkdir' and find it right away.  Similarly, hunt
around until you find `chdir()`

Let's try `os.mkdir()` and `os.chdir()` see what happens.

```python
>>> os.getcwd()
'/Users/grundoon'
>>> os.mkdir('Example')
>>> os.chdir('Example')
>>> os.getcwd()
'/Users/grundoon/Example'
```

That seems to have worked!  There are two ways you might return to the
folder you came from.  What are they? [Answer at the bottom.]

OK.  We have a couple more tools we need.  Let's go ahead and make the
first two levels of directories.  We'll take our script that just printed
and add some work to it.  (This isn't going to work if you haven't been
typing along.  Make sure you have the `subjIDs` list created and that it
has at least one entry.)

```python
for subject in subjIDs:
    print "Working on subject", subject
    # We need to create these
    os.mkdir(subject)
    # We need to create the next folders inside the subject folder
    os.chdir(subject)
    for subdir in [ 'anat', 'func' ]:
        print "  Working on", subdir, "in", os.getcwd()
        os.mkdir(subdir)
    # When we are done with work in a subject folder, we need to
    # go back.  Note the indentation change.  If this is indented
    # to the same level as making subdir, it will go bad for you.
    os.chdir('..')
```
OK, so that works.  Once.  If you try to run that again, you will get
errors because you are trying to create folders that already exist.
Wouldn't it be nice if that didn't happen?

## Try it, you'll like it

We're going to take a little time with this because it will be important
later on.  You can ask Python to _try_ something, and if it doesn't
work, Python will _raise an exception_, as in "I take exception to that,
you cad!"  You can then provide an alternate something to do in that
(or those) cases.  Let's use some of what we've learned to figure out
an exception and what do to when we get one.

We just created some subject folders.  What happens if we try to create
the same folder again?

```python
>>> os.mkdir('subj001')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 17] File exists: 'subj001'
```

Well, there's that traceback stuff again, but we can ignore that for
now and concentrate on the `OSError: [Errno 17] File exists: 'subj001'`.
The first thing there, is the _exception type_: `OSError`.  The second
bit is the error number, and final bit is the error message.

You need to know the error conditions to figure out what to do about them,
and one way to do that is to induce them, as we have here.  There are two
parts to this method, the first is what you want to try, and the second
is what to do when trying fails.  Here's a first pass.

```python
try:
    os.mkdir('subj001')
except OSError:
    print("subj001 exists")
```
If you type that at a Python prompt, it should look like this:

```python
>>> try:
...     os.mkdir('subj001')
... except OSError:
...     print("subj001 exists")
... 
subj001 exists
```

Let's get a little fancier and also learn another really useful
thingy, the conditional.  Sometimes you want to do one thing _if_
some condition pertains and another if not.  We do this with `if`,
`elif`, and `else`.  Let's see how this works.

```python
>>> if os.path.isdir('subj001'):
...     print "It's a dir!"
... elif os.path.isfile('subj001'):
...     print "It's a file!"
... else:
...     print "Call superman, it's something weird!"
... 
It's a dir!
```

Notice, I snuck in a couple of new functions.  There are many
functions under `os.path` that can help with file and folder
names and such.  But, to return to the main story, that little
chunk first inquires whether `subj001` is a directory; if it is
it says so.  If it's not a directory, it goes to the next 
enumerated condition and checks whether it is a file; if it is
it says so.  If none of the preceding enumerated conditions are true,
then the `else` is invoked.

We care about this because there are two ways that creating a
directory could fail, and the error message doesn't distinguish
among them.  We get the same error message whether `subj001` is
a file or a folder.  If it's a folder, we can probably go on to
do with it what we want.  If it's a file, though, we don't want
to try to change directory to it.  So, let's dress up our trying.

```python
try:
    os.mkdir('subj001')
except OSError:
    if os.path.isdir('subj001'):
        print "OK then.  Continue."
    elif os.path.isfile('subj001'):
        print "It's a file!  Stop what you're doing"
    else:
        print "Call superman, it's something weird!"
```

Finally, let's pull all this together into one big jumble, and try
to write a program that will create the first two levels of the tree.
That is, it will create three sets of folders that look like

```
[subjectID]/
    anatomy/
    func/
    raw/
```

We have this bit from a while back that creates the folders if they
aren't there.

```python
for subject in subjIDs:
    print "Working on subject", subject
    # We need to create these
    os.mkdir(subject)
    # We need to create the next folders inside the subject folder
    os.chdir(subject)
    for subdir in [ 'anat', 'func' ]:
        print "  Working on", subdir, "in", os.getcwd()
        os.mkdir(subdir)
    # When we are done with work in a subject folder, we need to
    # go back.  Note the indentation change.  If this is indented
    # to the same level as making subdir, it will go bad for you.
    os.chdir('..')
```

and into that we want to put our groovy new error checking thing.

So, we want to find all the uses of `os.mkdir()` and replace them with
our `try...except`.  When doing something like this, it's a good idea
to just comment the thing you're replacing and put the replacement
below it.  Don't forget to adjust the indents.  Also, when copying
and pasting, don't do what I did and leave the `'subj001'` as the
thing being checked everywhere &ndash; use the variable name
for the folder you're trying to check on.

```python
for subject in subjIDs:
    print "Working on subject", subject
    # We need to create these
    # os.mkdir(subject)
    try:
        os.mkdir(subject)
    except OSError:
        if os.path.isdir(subject):
            print "OK then.  Continue."
        elif os.path.isfile(subject):
            print "It's a file!  Stop what you're doing"
        else:
            print "Call superman, it's something weird!"
    # We need to create the next folders inside the subject folder
    os.chdir(subject)
    for subdir in [ 'anat', 'func' ]:
        print "  Working on", subdir, "in", os.getcwd()
        # os.mkdir(subdir)
        try:
            os.mkdir(subdir)
        except OSError:
            if os.path.isdir(subdir):
                print "OK then.  Continue."
            elif os.path.isfile(subdir):
                print "It's a file!  Stop what you're doing"
            else:
                print "Call superman, it's something weird!"
    # When we are done with work in a subject folder, we need to
    # go back.  Note the indentation change.  If this is indented
    # to the same level as making subdir, it will go bad for you.
    os.chdir('..')
```

Finally, we're going to introduce one last thing.  We can import specific
things from a library.  In that program above, we actually want to stop
the program in some places.  There is a library called `sys` that has such
a function, `sys.exit`, and we're going to import just that function but
call it `bail_out`.

```python
from sys import exit as bail_out
```

Now, we're going to have one last version of this where we quit the
program if something goes wrong.

```python
for subject in subjIDs:
    print "Working on subject", subject
    # We need to create these
    # os.mkdir(subject)
    try:
        os.mkdir(subject)
    except OSError:
        if os.path.isdir(subject):
            print "OK then.  Continue."
        elif os.path.isfile(subject):
            print "It's a file!  Stop what you're doing"
            bail_out()
        else:
            print "Call superman, it's something weird!"
            bail_out()
    # We need to create the next folders inside the subject folder
    os.chdir(subject)
    for subdir in [ 'anat', 'func' ]:
        print "  Working on", subdir, "in", os.getcwd()
        # os.mkdir(subdir)
        try:
            os.mkdir(subdir)
        except OSError:
            if os.path.isdir(subdir):
                print "OK then.  Continue."
            elif os.path.isfile(subdir):
                print "It's a file!  Stop what you're doing"
                bail_out()
            else:
                print "Call superman, it's something weird!"
                bail_out()
    # When we are done with work in a subject folder, we need to
    # go back.  Note the indentation change.  If this is indented
    # to the same level as making subdir, it will go bad for you.
    os.chdir('..')
```

## What's ahead?

In the next episode, we'll look at how to make functions of our own, so we
don't have to copy large blocks of text around.  Like that `try...except` that
we have in two places (and will have in a third).

-----

### About what you read on the internet

Step into a new window in your browser, and search the web for the text "python
make directory".  One of the top items returned (if you use the Evil Google)
is to the web page
http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
where you can see that there are lots of ways to do this, and many opinions
about the One True Best Way.  You want to learn enough, and experiment enough,
to be able to look at the sage and not-so-sage advice you find and
tell whether it is good or bad, worth trying or not, and whether it is
complete enough for what you need or needs to be given more thought.

Remember, on the internet, you never know whether they're a dog.

https://en.wikipedia.org/wiki/On_the_Internet,_nobody_knows_you're_a_dog

### Returning to the folder whence you came

You can save the folder you are in
prior to using `os.chdir()`, then `os.chdir()` explicitly to it.

```python
old_dir = getcwd()
os.chdir('Example')
# Do something fabulous here
os.chdir(old_dir)
os.getcwd()
```

Or, you can also use the 'name' of the directory above the current one

```python
os.chdir('Example')
# Do something fabulous here
os.chdir('..')
os.getcwd()
```
This could be made easier by assigning `'..'` to a variable, then using
the variable, which would be easier to type.  Sometimes making things
easier to type is reason enough.
