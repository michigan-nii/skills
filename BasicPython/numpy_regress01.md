# A simulated numerical project using NumPy

As you know, the regression model can be written and implemented
using matrices.  The basic form of the model is

***Y*** = ***X&beta;*** + ***&epsilon;***

That's all well and good, but it's not terribly helpful if
you want to compute those things, yet.  Typically, you would
get the _*Y*_ and the _*X*_ in a file, then you would compute
the _&beta;_ and the _&epsilon;_.

For example, you might get a file, let's call it `data.csv` that
is structured like this

```
x,y
4.0,33
4.5,42
5.0,45
5.5,51
6.0,53
6.5,61
7.0,62
```

So, for the remainder of this page, I'll write out in English
some plausible steps you might take to calculate the various parts
of the regression equation above.

What's the first thing you have to do to use NumPy?  Import it.
Import it the way it is used most commonly.

## Read the data

To do anything to data with NumPy, you have to get it (them?) into
a format that NumPy likes.  That form is a _NumPy array_.

For some information about NumPy arrays, see

http://www.scipy-lectures.org/intro/numpy/array_object.html

We will be creating some arrays, we'll do some operations on
them, we'll combine them, and finally we'll figure out how to
print them.

We have a file, and it contains the data, so we don't need to
spend a lot of time here creating NumPy arrays manually -- who
would consider typing in data for a slice by hand?  Instead, 
we'll cheat and ask the Goog how to read an array from a file.

I searched for "numpy read array from file" and got two promising
hits.

https://docs.scipy.org/doc/numpy/reference/generated/numpy.fromfile.html
-- and --
https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html

I looked at the top of the first page and saw

> A highly efficient way of reading binary data with a known data-type,...

and I figured this was not the droid I was looking for.  I have _text_ data.
Next.

> Load data from a text file.

Oh, yeah.  Much more promising!  It's good to read the descriptions of the
options, at least scan quickly, so you have a sense of what's possible even
if you don't use it right away.  Hmmm, fname, scan, delimiter, scan, skiprows,scan,
scan.

I think that's what is needed.  So, to read the file above, I would try

```
data = np.loadtxt('data.csv', delimiter=',', skiprows='1')
```

(I put an error in that.  Can you find it?)

Once you have data in `data` you can print it, find out its type, and 
find out the type of just the first element of the first row.

So, now we have

```
array([[  4. ,  33. ],
       [  4.5,  42. ],
       [  5. ,  45. ],
       [  5.5,  51. ],
       [  6. ,  53. ],
       [  6.5,  61. ],
       [  7. ,  62. ]])
```
That's not really what we need to do the matrix calculations.  We
need one column for `Y`, and we actually need one column for `X`,
but it also needs a column of 1s.

What does this give you?

```
data[:,0]
```

That's not quite right.  We are going to want a two-column array,
where the first column is all 1s and the second is the first column
from `data`.

Break that down into smaller tasks.  First, get just the first column
of `data` out.  You'll need to find the part about _slices_ in NumPy.

Next, you need to get a vector of 1s that is the same length as the
length of the first column of `data`.  For something short like this,
you can count.  But, if that were long you really wouldn't want to.
So, find a way to get the right length using a function.

Next, you need to create an array that combines the vector of 1s and
the data vector into a 2 x N matrix.


