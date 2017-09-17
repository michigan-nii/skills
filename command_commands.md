# Command Linux commands with example uses

## Creating, changing to, and removing directories (folders)
Create a directory called `work`.  To create more than one directory, list
more than one name.
```
$ mkdir work
$ mkdir tmp1 tmp2 tmp3
```
To see which directory you are in, use
```
$ pwd
/home/grundoon
```
To change into a directory, use `cd`.  The special directory `..` is one
above wherever you are.
```
$ cd work
$ pwd
/home/grundoon/work
$ cd ..
$ pwd
/home/grundoon
```
To remove a directory, and it must be empty, use `rmdir`.  To remove more
than one, list them.
```
$ rmdir work
$ rmdir tmp2 tmp3
```

## Copying, renaming, and moving files
To copy a file, use `cp`, followed by the name of the original, then the name
of the copy.
```
$ cp 
```
