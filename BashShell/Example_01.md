# Example of using a shell script for a repetitive task

This example will go over in a fair amount of detail how one Bash script to
complete one step in processing over many subjects was created.  This is an
example of how I (Bennet) tend to work, and you may find another way is more
suited to you.  I find the method valuable, and along the way, we'll look at
a bunch of shell commands, variables, etc. that you should find useful no
matter what method you use to create your scripts.

I like to start with a bunch of words, then try to make something that looks
more like a list, then transform the list into commands.

## State the problem in words

The problem we are working on is that we have data from an external source
for several hundred subjects.  We want to run a processing stream on all the
subjects, but we are going to start with only the first step for this example.

So, we have subjects, called `AA001`, `AA002`,. . . , `AANNN`, where `NNN` is
some number in the hundreds.  For each subject, we want to run the FSL program
`eddy_correct` like so:

```bash
$ eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0
```

The data are on a network drive, though, and testing shows that things will
go much faster if we copy the data to a local drive, process, then copy the
results back.

The revised plan is then to create a temporary, local folder, copy the data
into it, run the program, copy the results back to the network drive, remove
all traces of our data from the local drive.

## Make the words into a list

Let's figure this out for just one subject first.

1. Make a temporary local folder
1. Copy the data to it from the network drive
1. Process the data
1. Copy the results back to the network drive
1. Clean up after ourself

## Convert the list to commands

I tend to make a lot of typographical errors, so I prefer to start with the
command itself, then wrap around that all the other steps that are needed to
make the final thing work.

In this case, for one subject, we can start with the command, as shown above.

Looking at what surrounds that command, we must take the first couple of steps
in order.  We can't copy data to a nonexistent folder.  So, first pass looks
like

```bash
cd /tmp
mkdir work
cd work
# copy the data
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0
```

Now, it's possible that someone else already created `work`; I mean, that's
kind of an obvious choice.  There are also crazy security reasons why you
might want to use a different name.  Mainly, though, you don't want things
to fail because someone beat you to using a name.

The one, true, right-minded way to create a temporary folder is using the
`mktemp` command, with the `-d` option to indicate you want a folder, not a
file.  That also will, by default, put it in the right temporary folder.

When you give the command, it prints the name of the new folder, and you want
to save that in a variable for later use.  You can make the output of a command
available for saving in a variable by putting it inside `$(...)`.  So,
that would result in this chunk.

```bash
MY_TMP=$(mktemp -d)
cd $MY_TMP
# copy the data
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0
```

We ran the `eddy_correct` program once from the command line, so we now know
that it will create two files:  the one named on the command line,
`NNN.edited_eddy.nii` and `NNN.edited_eddy.ecclog`.  We can use our nice
wildcards to help with the copying of output, as in

```bash
NNN.edited_eddy.*
```

But, hmmm, I think I have a problem, Houston.  From where am I copying the
data and to where am I copying the output?  We have the data on a network
drive, and all the subjects will be under one folder, so this is good
place to use a variable because we have an unchanging part of a name.

```bash
DATA_DIR='/path/to/the/network/folder'
```

and we would refer to that as `$DATA_DIR` now.  That's also less to type if
the path is long, so reducing the chance of random typos.  Each subject will
have a folder under that, so something like

```bash
DATA_DIR='/path/to/the/network/folder'
MY_TMP=$(mktemp -d)
cd $MY_TMP
cp -r $DATA_DIR/AA001 ./
cd AA001
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0
```

If we're putting this into a file, say `do_eddy_correct.sh`, we might want
to make it a runnable program.  To do that we have to add the special line
at the top to tell it which program will know the commands in the file,
`#!/bin/bash` in this case, and we have to change its permissions to add
the runnable attribute.  So, now we have

```bash
$ cat do_eddy_correct.sh
#!/bin/bash
DATA_DIR='/path/to/the/network/folder'
MY_TMP=$(mktemp -d)
cd $MY_TMP
cp -r $DATA_DIR/AA001 ./
cd AA001
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0
```

To make it a program we can just run, we set permissions with `chmod`.

```bash
$ ls -l do_eddy_correct.sh
-rw-r--r-- 1 grundoon users   0 Mar  8 23:19 do_eddy_correct.sh

$ chmod a+x do_eddy_correct.sh
$ ls -l do_eddy_correct.sh
-rwxr-xr-x 1 grundoon users   0 Mar  8 23:19 do_eddy_correct.sh
```

where the `x`s indicate _executable_.  We can now run it with

```bash
$ ./do_eddy_correct.sh
```

Finally, we should probably put comments into the file so that the person
we will be three months from now can be reminded what today's self was doing.

```bash
#!/bin/bash

# Save the data folder name in a variable for convenience
DATA_DIR='/path/to/the/network/folder'

# Create a temporary folder and save the name
MY_TMP=$(mktemp -d)

cd $MY_TMP

# Copy the subject folder and all its files (-r:  recursive copy)
cp -r $DATA_DIR/AA001 ./

cd AA001

# Run the program
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0

# Copy the output back to the data folder
cp NNN.edited_eddy.* $DATA_DIR/AA001/

```

So, we're almost done with the first pass at this.  Now all we need to do
is remove the data we copied, which makes it look finally like this.

```bash
#!/bin/bash

# Save the data folder name in a variable for convenience
DATA_DIR='/path/to/the/network/folder'

# Create a temporary folder and save the name
MY_TMP=$(mktemp -d)

cd $MY_TMP

# Copy the subject folder and all its files (-r:  recursive copy)
cp -r $DATA_DIR/AA001 ./

cd AA001

# Run the program
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0

# Copy the output back to the data folder
cp NNN.edited_eddy.* $DATA_DIR/AA001/

# Go back to our home directory
cd

# Delete the temporary folder and everything in it
rm -r $MY_TMP
```

Whoops.  I ran that, and it didn't work because the data file isn't really
calle `NNN.edited.nii`.  Looking in the subject folder reveals that it's
called `001.edited.nii`.  That's a lot like, but not exactly, the same as
the folder name.  There's a handy little program that can help us here: `tr`.
To learn more about `tr`, read the man page (something you'll hear a lot if
you hang out with Linux nerds).  Here's the first bit of the man page....

```bash
$ man tr

TR(1)                            User Commands                           TR(1)

NAME
       tr - translate or delete characters

SYNOPSIS
       tr [OPTION]... SET1 [SET2]

DESCRIPTION
       Translate, squeeze, and/or delete characters from standard input, writ‐
       ing to standard output.

       -c, -C, --complement
              use the complement of SET1

       -d, --delete
              delete characters in SET1, do not translate

       -s, --squeeze-repeats
              replace each sequence of a repeated character that is listed  in
              the last specified SET, with a single occurrence of that charac‐
              ter
```

If you've not read one of these, the synopsis tries to tell you how to use it.
Options are the the things that start with a `-`, like `-d`.  Later on the page
it will tell you what `SETS` are.  For a program like this, I like to use
`echo` to test what it does.  For example,

```bash
$ echo "tthe stuff is good" | tr -s 't'
the stuff is good
$ echo "tthe stuff is good" | tr -s 'tf'
the stuf is good
$ echo "tthe stuff is good" | tr -d 't'
he suff is good
$ echo "tthe stuff is good" | tr -c 't' 'a'
ttaaaataaaaaaaaaaaa$
```

That last one is a little tricky.  It changed _everything but_ 't' into 'a',
including the end of line character, which is why the `$` prompt is on the
same line as the `tr` output.  Why this digression?

We can use `echo $subject | tr -d 'A'` to get `001` from `AA001`.  And we can
use that in the filename, like so.

```bash
id_num=$(echo 'AA001' | tr -d 'A')
. . . .
eddy_correct ${id_num}.edited.nii ${id_num}.edited_eddy.nii 0
```

The first of those lines takes the output of the commands inside the `$()`
and puts in into a variable called `id_num`.  When we want to use the
variable's value, we add the `$` prefix.  Bash (shell) variables can contain
letters (upper and lower), numbers, and underscores in their names.  We use
the `{}` around the variable name whenever there might be some question
about whether what follows it could be part of the name.  In this case,
we're cool, but what if we copy this file to use for something else, and
the file name is `001_edited.nii`?

```$bash
$ id_num='001'
$ echo The file is called $id_num_edited.nii
The file is called .nii

$ echo The file is called ${id_num}_edited.nii
The file is called 001_edited.nii
```

See what happened?  Bash interpreted everything from the `$` to the first
character that isn't allowed in a variable name as the name, that is
`id_num_edited`, which doesn't exist, so it doesn't have a value, and the
command echoed everything else.

Since we're using variables, let's also put the subject folder in a variable
so we can change it in one place instead of maybe forgetting one later.  That
gives us

```bash
#!/bin/bash

# Set the name of the subject folder
subject='AA001'

# Create the ID number from it
id_num=$(echo $subject | tr -d 'A')

# Save the data folder name in a variable for convenience
DATA_DIR='/path/to/the/network/folder'

# Create a temporary folder and save the name
MY_TMP=$(mktemp -d)

cd $MY_TMP

# Copy the subject folder and all its files (-r:  recursive copy)
cp -r $DATA_DIR/$subject ./

cd $subject

# Run the program
eddy_correct ${id_num}.edited.nii ${id_num}.edited_eddy.nii 0

# Copy the output back to the data folder
cp ${id_num}.edited_eddy.* $DATA_DIR/$subject/

# Go back to our home directory
cd

# Delete the temporary folder and everything in it
rm -r $MY_TMP
```

If we are going to use this to process a bunch of different subjects, we
don't want to have to edit the file and change the subject name each time
-- we might as well just run the command.  To do this, we need to be able
to supply an _argument_ to the shell script that is the name of the subject
folder.  Then we could run it with something like

```bash
$ do_eddy_correct.sh AA0001
```

There are some variables that are automatically set when you run a shell
script (or other command), and those are the variables that correspond to
the _positional arguments_.  In the command above, there are two of these.
The first refers to the name of the program, i.e., `do_eddy_correct.sh`, and
it is called `$0`.  This exists even for your login shell.

```bash
$ echo $0
-bash
```

All the rest are `$1`, `$2`, etc.  There are lots of good things that can be
done using these, but here, we only care about `$1`.  We want to set `$subject`
to be whatever we provide as `$1`, in this case `AA001`.  Here's the short,
unsafe way to do that.

```bash
subject=$1
```

Why unsafe?  Well, we saw what happens when a variable doesn't exist, so we
want to make sure that _something_ is in `$1`.  It will be safer to use

```bash
if [ -z $1 ] ; then
    echo "No subject folder name given.  Bye, bye."
    exit 1
fi
subject=$1
echo "Subject is $subject"
```

So the `-z` thing means "is the following thing empty?", so that `if` will be
true if we don't include a folder name.  If we don't, then `do_eddy_correct.sh`
will print a message and exit and indicate it did so because of an error
(that's what the 1 means).  If there is a folder name -- no guarantee it's a
valid folder, but it's something -- then the `if` doesn't do anything, and the
subject gets set and printed.

Put just those into a file called `test.sh`, and try it.

```bash
$ bash test.sh
No subject folder name given.  Bye, bye.
$ bash test.sh AA001
Subject is AA001
```

So, replace these lines

```bash
```bash
#!/bin/bash

# Set the name of the subject folder
subject='AA001'
```

from your saved `do_eddy_correct.sh` with these lines

```bash
if [ -z $1 ] ; then
    echo "No subject folder name given.  Bye, bye."
    exit 1
fi
subject=$1
```

and it should all be good to go as

```bash
$ do_eddy_correct.sh AA001
```

## Processing multiple subjects

Because we made `do_eddy_correct.sh` take an argument, all we have to do
is find a way to run it a bunch of times, each time with a new subject.
To do this, we will use a `for` loop, thusly.

```bash
#!/bin/bash

for sub in AA001 AA002 AA003 ; do
    echo "running $sub"
done
```

Here, again, I'm creating a 'fake' script to make sure I get the `for` part
right before I go and try to run a program that might spit many nasty errors
at me.  You can create a file and put these lines in it, then change its
permissions to make it runnable, then run it.

Or, you should be able to just copy and paste the three lines of the loop
into a terminal and see it work.  

```bash
$ for sub in AA001 AA002 AA003 ; do
>     echo "running $sub"
> done
running AA001
running AA002
running AA003
```

So, to run the `do_eddy_correct.sh` script, we change that the file to contain

```bash
#!/bin/bash

for sub in AA001 AA002 AA003 ; do
    ./do_eddy_correct.sh $sub
done
```

and it's done.

Well, if you have only those three subjects.  Suppose you have

```bash
$ ls 
AA001  AA003  AA005  AA007  AA010  AA012  AA014  AA017  AA019
AA002  AA004  AA006  AA008  AA011  AA013  AA016  AA018  AA020
```

We can use a cute trick here.  Suppose I have those in a folder called
`data`.  I can generate that list by using this.

```bash
$ ls data
AA001  AA003  AA005  AA007  AA010  AA012  AA014  AA017  AA019
AA002  AA004  AA006  AA008  AA011  AA013  AA016  AA018  AA020
```

*and* I can even do this (watch, now; nothing up my sleeve)

```bash
for sub in $(ls data) ; do
   echo Subject is $sub
done
```

It's always good to think a bit ahead.  Suppose I had, instead

```bash
$ ls data
00READ_ME_FOR_INFORMATION  AA003  AA006  AA010  AA013  AA017  AA020
AA001                      AA004  AA007  AA011  AA014  AA018
AA002                      AA005  AA008  AA012  AA016  AA019
```

Then that command would give me

```bash
$ for sub in $(ls data) ; do
>     echo Subject is $sub
> done
Subject is 00READ_ME_FOR_INFORMATION
Subject is AA001
. . . .
```

and that would be bad.  But, things get complicated as we try to work around
that.  If I try `data/AA*` to get just what begins with `AA`, then I get

```bash
$ ls data/AA*
data/AA001:
001.nii

data/AA002:
002.nii
. . . .
```

I can use the `-d` and get partway there,

```bash
$ ls -d data/AA*
data/AA001  data/AA004  data/AA007  data/AA011  data/AA014  data/AA018
. . . .
```

What I really want is go into `data`, then do `ls -d AA*`.

Another digression:  When we put something inside `()`, we are running it
in a _subshell_, which is another copy of bash that runs the stuff in the
`()` then quits.  We can separate commands inside the `()` with a semicolon.

```bash
$ (cd data ; ls -d AA*)
AA001  AA003  AA005  AA007  AA010  AA012  AA014  AA017  AA019
AA002  AA004  AA006  AA008  AA011  AA013  AA016  AA018  AA020
```

and to use all those names, we make it

```bash
for sub in $(cd data ; ls -d AA*) ; do
    ./do_eddy_correct.sh $sub
done
```

That's a lot of stuff all to get just one thing done..., well, actually,
if we had a couple hundred subjects, we've done one thing but a couple
of hundred times.  As you learn more of these commands, writing scripts like
these will get easier, and take less time, and it will All Be Worth It.
