# Making functions and pipelineable programs

We have a fine and wonderful program now that will regress one variable
on another.  If this were some other special calculation, and it needed
to fit into a pipeline somewhere, what would we have to do to make it
generally useful?

What does it do right now?

1. It imports NumPy
1. It reads a specific data file
1. It creates two new variables, Y and X of the right shape
1. It calculates the regression equation
1. It spits out some output

What would we need to do to make this more generally useful?

1. We could pass it the name of the `.csv` file as a parameter
1. We could change it so it we could specify which two columns
   to use as Y and X from a file with more than two columns.
1. We could pass data back as return values:  Like, a matrix
   with the residuals and predicted values.  Maybe even pass
   the beta vector back; or both.
1. We could have it calculate a bunch more stuff

We could do all of that.

So, why don't we start by creating a function that takes as
input the two vectors, Y and X, and just calculates the regression
and prints the output?

Right, I hear only Stanley Clarke and no objections, so, here
goes.

We already saw how to create a new function in Step03, but here's
the quick recap.

```python
>>> def my_world():
...     print("My world, and welcome to it.")
... 
>>> my_world()
My world, and welcome to it.
```

and the rest is details.  What we have, though, is

```python
import numpy as np
data = np.loadtxt('data.csv', delimiter=',', skiprows=1)
Y = data[:,1]
Y = Y[:, np.newaxis]
X = data[:,0]
ones = np.ones(data.shape[0])
X = np.array([ones, X]).T
X_prime_X_inv = np.linalg.inv(np.dot(X.T, X))
b = np.dot(
       np.dot(X_prime_X_inv, X.T),
       Y
    )
Y_hat = np.dot(X, b)
resid = Y - Y_hat
print("\nRegression coefficients")
print("----------------")
print("b0:  %.6f\nb1:   %.6f" % (float(b[0]), float(b[1])))
print("----------------")
print("\nPredicted values")
print("----------------")
print(Y_hat)
print("----------------")
print("\nResiduals")
print("----------------")
print(resid)
print("----------------")
```

So, let's take a stab at it....  As a place to start, let's say we
will pass in two separate vectors, Y and X, and we only need to
keep what's important for them.  Let's start by keeping everything
in one file.

```python
import numpy as np

def my_regress(Y, X):
    Y = Y[:, np.newaxis]
    ones = np.ones(data.shape[0])
    X = np.array([ones, X]).T
    X_prime_X_inv = np.linalg.inv(np.dot(X.T, X))
    b = np.dot(
           np.dot(X_prime_X_inv, X.T),
           Y
        )
    Y_hat = np.dot(X, b)
    resid = Y - Y_hat
    print("\nRegression coefficients")
    print("----------------")
    print("b0:  %.6f\nb1:   %.6f" % (float(b[0]), float(b[1])))
    print("----------------")
    print("\nPredicted values")
    print("----------------")
    print(Y_hat)
    print("----------------")
    print("\nResiduals")
    print("----------------")
    print(resid)
    print("----------------")

# Do the real work here
data = np.loadtxt('data.csv', delimiter=',', skiprows=1)
Y = data[:,1]
X = data[:,0]

my_regress(Y, X)
```

Did that work?  Mine did!  Wicked.

Wouldn't it be cool, though, if we could put the function in
a separate file, then we would only need four easy lines to
do this.  OK, let's try it.  Put all the 'real work' lines into
a separate file and call it `my_project.py`.  Now, remove those
from the file where you had the function definition, and rename
it `my_regress.py`.

Maybe we'll get lucky!

```bash
$ python my_project.py 
Traceback (most recent call last):
  File "my_project.py", line 7, in <module>
    my_regress(Y, X)
NameError: name 'my_regress' is not defined
```

Fooey.  So, what's happened here?  Python is not Matlab, so the
files that end with `.py` are not automatically on your path if
they are in the same folder.  Instead, we have to use an `import`.

So, right after I `import numpy`, lets import `my_regress` (someone
on the internet said so).

```python
import numpy as np
import my_regress
. . . .
```

Now I run it, and I get

```python
Traceback (most recent call last):
  File "my_project.py", line 8, in <module>
    my_regress(Y, X)
TypeError: 'module' object is not callable
```

Progress?  Yes, we got one error to go away.  'Module object is
not callable'?  Module?  Oh, right.  We use `import` to load
modules, so this is saying that `my_regress` is the name of the
module, not the name of the function.  We have another module
loaded, `numpy`, and we assigned it to an alias, `np`.  So, let's
try a wild and crazy experiment and try

```python
import my_regress as my
```

and then change `my_project.py` to say

```python
my.my_regress(Y, X)
```
More progress!  Now I get,

```python
  File "my_project.py", line 8, in <module>
    my.my_regress(Y, X)
  File "my_regress.py", line 4, in my_regress
    Y = Y[:, np.newaxis]
NameError: global name 'np' is not defined
```

What the...?!  I have an `import numpy` in....  Oh.  In `my_project.py`.
I guess the import there isn't visible to `my_regress.py`.  Let's add an
`import numpy` there, too.

Now I get,

```python
[bennet@perspicacity:BasicPython]$ python my_project.py 
Traceback (most recent call last):
  File "my_project.py", line 8, in <module>
    my.my_regress(Y, X)
  File "my_regress.py", line 5, in my_regress
    ones = np.ones(data.shape[0])
NameError: global name 'data' is not defined
```

Oh, right, I am using the original `data` matrix to set the size
of the ones.  I should be using something _local_ to `my_regress`,
so let's change it to

```python
ones = np.ones(X.shape[0])
```
I'm using `X` because that's what I'm going to join it to.

And..., Joy!  That seems to have made it work.  There is one
more suggestion that occurred to me late, and that is, since
we have to use the module name to use the function, let's change
the function to `regress()` and rename the module file to `my.py`,
so we can call it with `my.regress(Y, X)`.

The two files are now

The script that reads data and runs `regress()` [my_project.py](my_project.py)
The file that contains the `regress()` function [my.py](my.py)
