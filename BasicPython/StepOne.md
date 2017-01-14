# Getting started with variables and repeating things

## Variables and variable types

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

## The magically changing meaning of +

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

## Changing the type of a variable

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

## Scary error messages demystified

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

So, the `+` sign means two different things depending whether it has strings
on either side or integers.

## Generating a sequence of numbers

Numbers are nice because you can generate them.  To generate integers, Python
uses the `range()` function.  Here, `range` is the function name, we add the
`()` to indicate so, and we will often just say 'uses `range()`' and you'll
know we mean a function because of the parentheses.  The function will do
things with whatever is inside the parentheses.

In this case `range()` will generate a list of integers that start at 0 and
go to one less than whatever integer you put in the parentheses.  A list is
another variable type.  It holds multiple elements.

```
>>> range(5)
[0, 1, 2, 3, 4]
>>> type(range(5))
<type 'list'>
```
A list is a collection of other types of variables.  Lists have nice ways
to refer to individual elements and to go through each element in turn.  We'll
learn lots more about lists and other multi-element variable types later.

## Doing something to each element of a list

To do something to each element of a list (or other multi-element variables),
you can use `for`.

```
>>> for item in range(5):
...     print item
...
0
1
2
3
4
```

So, Python took each element out of the list, and for each one, it printed it.
A couple of things to note about this.  First, the colon at the end of the
`for` line indicates that more is to come and should be done for each item.
Second, the lines that are part of the `for` loop (what we call this type
of action) are all indented _exactly the same way_.  Here, we used four
spaces.  You should, too.  If you use four spaces on one line, and three on
the next, you will get an indentation error, and you won't like it.  Be
careful with Tab characters!

## Formatting string for printing and other things

We have almost all the pieces we want.  It's usually a good idea to _pad_
names so that all the names of similar things have the same number of
characters.  For subjects, you'll often see (and almost certainly want)
_left padding with zeros_ in your subject IDs.  That `for` loop above left
the variable `item` with the value `4`, so to pad that to three characters
we use this

```
print('{:03d}').format(item)
```

We know what `print` does, but we're adding new stuff to it; `print` is really
a function, and we can use it without parentheses if we only want a simple
print.  Here we are adding a string inside the parentheses (we know it's a
string because it's quoted).  The braces are used as a _placeholder_ for
things inside the `.format()`.  The `03d` is the format we want the string to
have (the leading 0 is how you indicate 0-padding, the 3 is the width, and
the `d` indicates integer (I don't know how they came up with that).  The
`:` is there to separate the placeholder name (which we're not using here)
from the format.

Here are two examples, one where the braces are filled by the things in the
`format()` in order as listed, and one where they are named and can be in
a different order.

```
print('{subjID:04d} and {int}').format(int=i, subjID=item)
print('{:03d} and {}').format(item, i)
```

## Remind me why we did this...

So, combining all this together, we can make the skeleton of a program that
will do something useful for each subject from 0 to 4.

```
for id in range(5):
    subjID = 'subj{:03d}'.format(id)
    print "I did something useful to subject: {}".format(subjID)
```

which results in

```
I did something useful to subject: subj000
I did something useful to subject: subj001
I did something useful to subject: subj002
I did something useful to subject: subj003
I did something useful to subject: subj004
```
