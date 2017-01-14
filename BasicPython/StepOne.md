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
a prompt, `>>>` to indicate a Python prompt, and other text will be output.
When we want to indicate something that is some kind of code, we'll make it
grey in the text, as we did with the `$` prompt above.)

The word `filename` is the name of the variable, and `'subj001` is the value.
Because there are quotes around `subj001`, it is a _string_ variable; that is,
one that contains characters.  Without the quotes, Python would think that is
a variable name because it begins with a non-numeric character.

Variable can be of many types, but the most important _single element_ types
are string, integer, and float (numeric with decimals).  You can ask Python
what a variable is, as shown below, along with creating and querying the two
numeric types.

```
>>> type(filename)
<type 'str'>
>>> i = 0
>>> type(i)
<type 'int'>
f = 0.0
>>> type(f)
<type 'float'>
```

Python reuses symbols in what tries to be sensible ways depending on context.
For example,

```
first = 'Evil'
last = 'Twin'
phrase = 'My' + ' ' + first + " " + last
```

You can `print` most variables

```
>>> print phrase
My Evil Twin
>>> print f
0.0
```

Sometimes you will have a number and wish it were a string, and vice-versa.
You can convert among them like this.

```
print 'subj' + str(i)
not_an_integer = '25'
type(not_an_integer)
i = 5
i + not_an_integer
i + int(not_an_integer)
```

If you're typing along, you will have got _Traceback_, which is Python-speak
for an error.  It shows you the steps it was taking when it got to the error
and it tries to give you helpful information.  As you get more experience, the
information will become more helpful (really).  This is what it looked like
when I did it.

```
>>> i + not_an_integer
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

The `File "<stdin>", line 1, in <module>` means it was doing something typed
at a Python prompt.  This bit, `TypeError: unsupported operand type(s) for +:
'int' and 'str'`, means that there were two different types of variables,
and you can only use one type with a `+` sign.  We converted the string to
the integer in the second attempt above.


