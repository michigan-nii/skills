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

The filesystem is a database.
