# Reading data from a file

At some point or another, most projects you might create with Python will
involve reading and/or writing to files.  So, a good place to start your
excursion with Python is doing that.  Along the way, we need to learn some
other skills and techniques.

# Variables and variable types

When doing work with data, there will often be a list of files that need
to be worked with.  One of the most common ways of doing that is to assign
each filename to a variable, then do something with that file, then move on
to the next filename.  We can't, of course, do that, until we know how to
assign values to variables.  So, let's start there.

```
filename = 'subj001'

```

(Text in the grey boxes is literal program text, and Python should be able to
run it as typed.  If we want to indicate a command, we will use `$` to indicate
a prompt, `>>>` to indicate a Python prompt, and other text will be output.)

The word `filename` is the name of the variable, and `'subj001` is the value.
Because there are quotes around `subj001`, it is a _string_ variable; that is,
one that contains characters.  Without the quotes, Python would think that is
a variable name because it begins with a non-numeric character.

Variable can be of many types, but the most important _single element_ types
are string, integer, and float (numeric with decimals).  

