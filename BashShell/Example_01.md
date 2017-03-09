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

So, we have subjects, called AA0001, AA0002,. . . , AA0NNN, where NNN is
some number in the hundreds.  For each subject, we want to run

```
$ eddy_correct 0001.edited.nii 0001.edited_eddy.nii 0
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

