# Adventures in public data

Trying to prepare examples to show people, I started getting a lot of errors
when running the CAT12 toolbox to do segmentation.  The errors were not
all the same,

```
------------------------------------------------------------------------
CAT Preprocessing error: CAT:cat_main:badTissueContrast: ./bennet/openfmri/MC2/derivatives/sub-01/func/coReg/T1w.nii 
------------------------------------------------------------------------
Bad tissue contrast (C=127.24, G=136.76, W=37.40)
```
and
```
------------------------------------------------------------------------
AMAP estimated untypical tissue peaks that point to an 
error in the preprocessing bevor the AMAP segmentation.
```
are a couple of examples.

Consulting with local experts (always handy to have around), we concluded this
might be an issue with where the origin of the images was set.  This led to
two questions.

1.  How do we quickly get the origin and other useful information from a set
    of images?

1.  What might be analogous to printing variable definitions and summaries for
    a 'regular' dataset?


