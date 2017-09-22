# The file system

Files are stored in what's called a _filesystem_, which is typically on a disk
drive somewhere, possibly installed in the computer, but possibly attached via
the network.

In Linux, filesystems are organized hierarchically, with the _top_ being called
`/`, the _root_ directory or 'slash'.  We now use directory and folder as
synonyms, and all other folders are considered to be in, inside, or under the
root directory.  This is reflected in their names.
```
/data
/data/home
/data/projects/BigStudy
```
Folder names that begin with the `/` are called _fully qualified names_, and
they refer to an absolute location; no ambiguity.

When you're logged in, you are always in some folder.  By default, when you
first log in, you are in your _home directory_.  Where that is can vary from
system to system depending on the whims of your system administrator and the
disk arrangement.  You can always find out what your current folder is by
using
```
$ pwd
/home/grundoon
```
Your home directory is sometimes referred to as `~` (which is pronounced
'tilde' or 'twiddle').  It will most often work, but sometimes not. The
fully qualified name printed by `pwd` from your home directory will _always_
work.

## Aside:  The filesystem is a database

The filesystem is a database.  It contains files, folders, and information
about those files and folders.  You can ask the filesystem for details about
files or for the contents of files.

In Linux, _everything_ is a file.  Folders are just a special type of file that
contain the locations of, and information about, other files.  To Linux, even
your terminal window is a file (two files, at once, actually).

# Creating and removing directories

You create directories with `mkdir` followed by the names of one or more
directories.  The first example below creates a folder called `working`
and the second one called `openfmri` and one called `src`.
```
$ mkdir working
$ mkdir openfmri src
```
If we decide we don't need `src` after all, we remove it (provided it's
empty) with
```
$ rmdir src
```
You change into the `working` directory, create another one called
`sub001`, and then change to that with
```
$ cd working
$ mkdir sub001
$ cd sub001
```
To make sure you know where you are, you can use `pwd`.  There is a
special directory name, `..` (yup, two dots, pronounced dot-dot), which
means "one directory above where I am".  So, you should be in the
`sub001` folder.  What's one above that?
```
$ cd ..
$ pwd
```
Change back to `sub001`, then try this trick.
```
$ cd sub001
$ cd ../..
$ pwd
```
Just `cd` with no name will take you back to your home directory, also
called `~` (tilde, or twiddle).  Do that.

