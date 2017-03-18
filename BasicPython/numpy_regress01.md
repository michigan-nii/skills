As you know, the regression model can be written and implemented
using matrices.  The basic form of the model is

***Y*** = ***X&beta;*** + ***&epsilon;***

This example will show matrix functions that will let you take
that and convert to NumPy code.  I hope.

# Some useful NumPy functions

```
>>> import numpy as np
>>> Y = [1, 2, 3]
>>> Y = np.array(Y)
>>> Y.shape
(3,)
>>> Y
array([1, 2, 3])
```

So, Y is a row vector.  We need a column vector.

```
Y = Y[:,np.newaxis]
Y.shape
Y
array([[1],
       [2],
       [3]])
```

Data comes in files, typically, like this one, called `data.csv`.

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

To read a `.csv` file,

```python
data = np.loadtxt('data.csv', delimiter=',', skiprows='1')
```

(I put an error in that.  What is it?)

Our data came in as a column of X values followed by a
column of Y values.  So, we need to be able to separate
those.  We do that with a _slice_.

```
Y = data[:,1]
```

The colon indicates "all values".  You can put the start index to
its left and the end value to its right, we would have these
examples,

```
>>> data
array([[  4. ,  33. ],
       [  4.5,  42. ],
       [  5. ,  45. ],
       [  5.5,  51. ],
       [  6. ,  53. ],
       [  6.5,  61. ],
       [  7. ,  62. ]])
>>> data[:5,1]
array([ 33.,  42.,  45.,  51.,  53.])
>>> data[3:,1]
array([ 51.,  53.,  61.,  62.])
```

If you don't specify an index on one side, it's 'the beginning'
on the left and 'the end' on the right.  There are two functions
that come in handy for creating vectors of a particular length
of zeros or ones.

```
>>> np.zeros(3)
array([ 0.,  0.,  0.])
>>> np.ones(3)
array([ 1.,  1.,  1.])
```

If you want to create a vector of the same length as an existing
vector, you can use the appropriate dimension from the 'shape'
method

```
>>> np.ones(X.shape[0])
array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.])
```

You can glue two vectors together with

```
>>> Y = np.array([1,2,3])
>>> Y
array([1, 2, 3])
>>> Y = np.array( [ np.ones(Y.shape[0]), Y] )
>>> Y
array([[ 1.,  1.,  1.],
       [ 1.,  2.,  3.]])
```

X' is the transpose of a X, so

```
>>> Y.T
array([[ 1.,  1.],
       [ 1.,  2.],
       [ 1.,  3.]])

```

X'X means 'multiply' X' and X together.  There are several 'multiplies'
in matrix terminology, and the * operator in NumPy is elementwise
multiplication, that is, each element of the matrix on the left is
multiplied by the corresponding element of the matrix on the right.

```
>>> Y
array([[ 1.,  1.],
       [ 1.,  2.],
       [ 1.,  3.]])
>>> Y * Y
array([[ 1.,  1.],
       [ 1.,  4.],
       [ 1.,  9.]])
```

That is not what we want.  We want, instead what's called the dot
product,

```
[ 1.,  1.]   [ 1.,  1.,  1.]   [  2.,   3.,   4.]
[ 1.,  2.] * [ 1.,  2.,  3.] = [  3.,   5.,   7.]
[ 1.,  3.]                     [  4.,   7.,  10.]
```

and that is obtained by using

```
>>> Y
array([[ 1.,  1.],
       [ 1.,  2.],
       [ 1.,  3.]])
>>> Y.T
array([[ 1.,  1.,  1.],
       [ 1.,  2.,  3.]])
>>> np.dot(Y, Y.T)
array([[  2.,   3.,   4.],
       [  3.,   5.,   7.],
       [  4.,   7.,  10.]])
```

We also have X<sup>-1</sup>, which is the inverse of X.  Why
this is fancier than X', I don't know, but it's not just `np.inv()`
it's

```
>>> Y=data[:2,:2]
>>> Y
array([[  4. ,  33. ],
       [  4.5,  42. ]])
>>> np.linalg.inv(Y)
array([[ 2.15384615, -1.69230769],
       [-0.23076923,  0.20512821]])
```

And that is quite enough.  Those are the tools I think you will need
to write a program to calculate the following from the data in the
last example.

_b_ = _(X'X)<sup>-1</sup>X'Y_

_Y_est_ = _Xb_ which is the same as _X(X'X)<sup>-1</sup>X'Y_

_resid_ = _Y - Xb_

and finally, create a column vector of zeros, then check that

_Y - Xb - resid_ = 0
