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

Suppose you were creating a pipeline that ran the programs to process
images from one step.  You can take the input file name and add a
letter to it to construct the output filename.

Assume that you have 4 subjects, the code below simulates what you
might need to do to run the first three preprocessing steps.  Fill
in the `???` with appropriate values, and finish the program so
that, when run, it produces output that looks like this.

## Output

```bash
$ python preprocessing.py
Running physio correction on ./func/task/run_01/subj001run.nii to create ./func/task/run_01/subj001prun.nii 
Running slice timing on ./func/task/run_01/subj001prun.nii to create ./func/task/run_01/subj001pprun.nii 
Running realignment on ./func/task/run_01/subj001pprun.nii to create ./func/task/run_01/subj001ppprun.nii

Running physio correction on ./func/task/run_01/subj002run.nii to create ./func/task/run_01/subj002prun.nii 
Running slice timing on ./func/task/run_01/subj002prun.nii to create ./func/task/run_01/subj002pprun.nii 
Running realignment on ./func/task/run_01/subj002pprun.nii to create ./func/task/run_01/subj002ppprun.nii

Running physio correction on ./func/task/run_01/subj003run.nii to create ./func/task/run_01/subj003prun.nii 
Running slice timing on ./func/task/run_01/subj003prun.nii to create ./func/task/run_01/subj003pprun.nii 
Running realignment on ./func/task/run_01/subj003pprun.nii to create ./func/task/run_01/subj003ppprun.nii

Running physio correction on ./func/task/run_01/subj004run.nii to create ./func/task/run_01/subj004prun.nii 
Running slice timing on ./func/task/run_01/subj004prun.nii to create ./func/task/run_01/subj004pprun.nii 
Running realignment on ./func/task/run_01/subj004pprun.nii to create ./func/task/run_01/subj004ppprun.nii
```

## Program skeleton

Copy this text to a file called `preprocessing.py`, make the changes,
and run it to verify the output you get matches the output above.

```python
for i in range(???, ???):
    subjID = ??? + ???
    input_file = 'run.nii'
    step = 'physio correction'
    output_file = ??? + ???
    folder = './func/task/run_01/' + subjID
    print("Running {} on {} to create {} ").format(???, ???, ???)
    ???
    ???
    . . .
```

Just a note, to add a blank line to the end of something printed, use

```python
print("Some text followed by a blank line.\n")
```

## Identifying repetition

There will be several lines of repeated code in the final result.  Suppose
there was a function called `nii_preprocess(step, input_file, prefix)`
that you would use like this

```python
    nii_preprocess('physio correction', 'run.nii', 'p')
```

that could be used.  What do you think the inside of that function
would look like?
