# Finishing the module

So, we now have a _module_, `my`, and it defines one function.  As the
error messages and experiments might suggest, the way to add more functions
to the module is to define them.  Let's go ahead and create a new function
to print the regression results.  In `my.py`, we had put the printing
into a conditional so we could suppress it if we were testing, now let's
move it into its own function.

```python
def print_results():
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

I run this, and I get,

```python
Traceback (most recent call last):
  File "my_project.py", line 7, in <module>
    my.regress(Y, X)
  File "/Users/bennet/github/skills/BasicPython/my.py", line 40, in regress
    print_results()
  File "/Users/bennet/github/skills/BasicPython/my.py", line 47, in print_results
    print("b0:  %.6f\nb1:   %.6f" % (float(b[0]), float(b[1])))
NameError: global name 'b' is not defined
```

What does that mean?  Oh, right, this is that _scope_ thing again.  We
created a function, so all the names in the function are _local_ to that
function, so the `b` in the main program is invisible.  How do we fix that?
We pass in the data needed, so that means the `def` line becomes

```python
def print_results(b, Y_hat, resid):
```

While we're here, let's clean up a bit.  We are printing some kind of a
heading, then a separator line, then some data three times.  That part
repeats.  Can we put that into a function?

```python
def print_head(heading):
    print("\n{}").format(heading)
    print("{}").format('-'*60)
heading = "Regression Coefficients"
>>> print_head(heading)

Regression Coefficients
------------------------------------------------------------
```

Now I have this in my `my.py` module file.

```python
import numpy as np
def print_results(b, Y_hat, resid):
    print_heading("Regression coefficients")
    print("b0:  %.6f\nb1:   %.6f" % (float(b[0]), float(b[1])))
    print_heading("Predicted values")
    print(Y_hat)
    print_heading("Residuals")
    print_heading(resid)
def print_heading(heading):
    print("\n{}").format(heading)
    print("{}").format('-'*60)

def regress(Y, X):
    '''This is a naive implementation of regression to illustrate some NumPy
    operations.  It also tries to implement some rudimentary error checking.
    It takes as input two NumPy arrays.  These should be of dimension (n,)
    '''
    # Try to perform a NumPy operation on Y, if it fails,
    # print message and return NaN
    try:
        Y = Y[:, np.newaxis]
    except TypeError:
        print "Y is not a NumPy array, perhaps?"
        return float('NaN')
    # Try to perform a NumPy operation on X, if it fails,
    # print message and return NaN
    try:
        ones = np.ones(X.shape[0])
    except AttributeError:
        print "X is not a NumPy array, perhaps?"
        return float('NaN')
    # Both inputs are now confirmed NumPy objects
    if X.shape[0] != Y.shape[0]:
        print "Y and X are not the same length.  Bye."
        return float('NaN')
    if not X.shape == (len(X),) or not Y.shape == (len(Y),1):
        print "X", X.shape, "Y", Y.shape
        print "One of X and Y are not unidimensional"
        return float('NaN')
    X = np.array([ones, X]).T
    X_prime_X_inv = np.linalg.inv(np.dot(X.T, X))
    b = np.dot(
           np.dot(X_prime_X_inv, X.T),
           Y
        )
    Y_hat = np.dot(X, b)
    resid = Y - Y_hat
    if __name__ != '__main__':
        print_results(b, Y_hat, resid)
    else:
        print "Succeeded"

if __name__ == "__main__":
    print "I should run some tests here, shouldn't I?"

    print "\nTrying with good data"
    Xgood = np.array([ 4. ,  4.5,  5. ,  5.5,  6. ,  6.5,  7. ])
    Ygood = np.array([ 33.,  42.,  45.,  51.,  53.,  61.,  62.])
    regress(Ygood, Xgood)

    print "\nTrying with bad X"
    X = [ 4. ,  4.5,  5. ,  5.5,  6. ,  6.5,  7. ]
    regress(Ygood, X)
    print "\nTrying with bad Y"
    Y = [ 33.,  42.,  45.,  51.,  53.,  61.,  62.]
    regress(Y, Xgood)
```

There's one last thing we should cover here, and that is getting values
back out of a function.  None of the data structures, `resid`, `Y_hat`,
etc., that are created inside the `regress()` function are visible to
the calling program.  You can verify by trying to `print resid` in 
`my_project.py`.  So, how do we get interesting and useful things back
out of a function?  We got a hint of this with our error checking, where
we used ` return float('NaN')`.  Now we want to `return` good values.

Let's put this right before we print the results table.

```python
return (b, Y_hat, resid)
```

That says that `regress()` should pass a _tuple` (like a list) back to
the calling program, and it should have the three calculated arrays
in it.  From the calling program, `my_project.py`, we change

```python
my.regress(Y, X)
```

to

```python
b, Y_hat, resid = my.regress(Y, X)
print b
print resid
```

to confirm that we actually got back something useful.
