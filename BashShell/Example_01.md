# Example of using a shell script for a pipeline

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

```
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

```
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

```
MY_TMP=$(mktemp -d)
cd $MY_TMP
# copy the data
eddy_correct NNN.edited.nii NNN.edited_eddy.nii 0
```

We ran the `eddy_correct` program once from the command line, so we now know
that it will create two files:  the one named on the command line,
`NNN.edited_eddy.nii` and `NNN.edited_eddy.ecclog`.  We can use our nice
wildcards to help with the copying of output, as in

```
NNN.edited_eddy.*
```

But, hmmm, I think I have a problem, Houston.  From where am I copying the
data and to where am I copying the output?  We have the data on a network
drive, and all the subjects will be under one folder, so this is good
place to use a variable because we have an unchanging part of a name.

```
DATA_DIR='/path/to/the/network/folder'
```

and we would refer to that as `$DATA_DIR` now.  That's also less to type if
the path is long, so reducing the chance of random typos.  Each subject will
have a folder under that, so something like

```
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

