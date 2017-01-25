# String things

If you look at the filenames for the images that come from the fMRI
lab, you'll see that the name change from one preprocessing step to
the next is by addition of a letter to the front of the name.  The
names are
```
    run.nii
    prun.nii
    tprun.nii
    rtprun.nii
```

```
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
