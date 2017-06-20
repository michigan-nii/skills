# Setting permissions recursively

It comes up sometimes that you want to set permissions recursively; that is,
on every file in a directory tree, or on some specifiable subset of files
within a directory tree.  We will look at a couple of ways that can be done.

First, lets review permissions and how to set them in Linux.

## Linux file permissions

When you look at the long listing for a file in Linux, you will see something
like this.
```bash
-rw-rw-r-- 1 grundoon nii-skills 3637299 Nov  2  2011 sub001/anatomy/highres001.nii.gz
```
The permissions are indicated by the characters furthest to the left.  The first
character indicates what kind of file; in this case it is a `-` and indicates a
regular file.  Other common possibilities are `d` for directory and `l` for symbolic
link.

Following that are three groups of three permissions.  The first permission in the group
indicates whether the file is readable if there is an `r`; the second indicates whether
is writable if there is a `w`; the third indicates whether it is executable if there is
an `x`.  The first group of three permissions are applied to the owner of the file, in
this case the user `grundoon`.  The second group is applied to the owning group, in this
case `nii-skills`; the third group is applied to everyone not in one of the first two
groups.  So, the file above is readable and writable by `grundoon`, readable and writable
by all the users in the `nii-skills` group, and readable but not writable by everyone else.

The permissions are referred to as the files _mode_ in Linux-speak, and they have a
numeric and symbolic representation.  If you set permissions numerically, you must
specify the _entire_ permission set explicitly, whereas if you set permissions symbolically
you can add and subtract permissions selectively.  For that reason, we recommend that you
use symbolic permissions wherever possible.

The owner is signified by a `u`; the group by a `g`; others by an `o`; and all the groups
by an `a`.  You indicate whether you want to add a permission with a `+` and to subtract
with a `-`.  If you want to operate on more than one of the permission groups, you separate
them by a comma.  Permissions are changed with the `chmod` command.  Here are a couple of 
examples.

Changing the permissions on the file listed above so that the group and the owner no longer
have write access could be done two ways.

```bash
$ chmod u-w,g-w sub001/anatomy/highres001.nii.gz
$ chmod a-w sub001/anatomy/highres001.nii.gz
```
The first explicitly names which groups write access should be subtraced from, whereas
the second removes it for everyone.

To make a script executable (provided that it really is) for everyone, you could

```bash
$ chmod a+x my_script
```

What would you use if you wanted to make it executable only by its owner and not
by others?  What is the effect of the following `chmod`?

``bash
$ chmod u+rwx,g+x-rw,o+x-rw secret_program
```

There are a couple of permissions that will come in handy when applied to directories.
The first is called the 'set GID bit'.  All files (and a directory is really just a
special type of file) are owned by a user and a group.  Every user has a primary group
to which they can belong.  When a user creates a new file, its owning group


## Setting permissions in a folder tree: Take one

Suppose you have a collection of subject folders `sub001`, `sub002`, etc.
This came from the OpenfMRI.org web site, collection DS008.  For each subject
there is an anatomy folder, and within the anatomy folder are
```
highres001_brain_mask.nii.gz  highres001.nii.gz     inplane.nii.gz
highres001_brain.nii.gz       inplane_brain.nii.gz
`` `
You want to try to reproduce the analysis, and some of those files will be
recreated, so you wish to move them aside and set their permissions to
read-only.

