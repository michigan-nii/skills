# Error checking and testing

In the last session, we split off the regress function from the code
that uses it.  And, in the end, we ended up with two files:

* `my_project.py` which reads the data and then passes it to the
`regress()` function
* `my.py` which got renamed so that we can call `my.regress()` rather
  than `my_regress.my_regress()` or having to create an alias to avoid
  doing that.

That's all good, but when the function gets moved off into a module, it
gets much easier to lose track of what kind of data it should be given,
and that suggests that the function should do some checking.

At the meeting, we discussed some things that you might want your regress
function to check before it went on to the hard stuff.  Here's a partial
list.

1.  We thought maybe it should check that it got both an `X` and a `Y`.
    That's a good idea, but Python will take care of that, in its current
    incarnation because we used `def regress(Y, X)`, so if one is missing,
    Python will flag it for us.
1.  We can't do regression if the two vectors are of different length.
1.  Since we are manipulating the data into the right shape inside the
    function, we should check that we are getting unidimensional arrays.
1.  We are going to depend on NumPy to do the work, so we should check
    that they are valid NumPy thingies.

There's probably more, but that's enough to get us started on error checking.
One thing that goes with error checking is testing that the error checking
works.  We can do that by setting up little scenarios with data known to be
bad in a particular way, then feed that to the function, which should do the
Right Thing.  There are many fancy frameworks to do this Unit Testing, and
if you continue writing Python, it might be worth looking at a couple.  Here
we will just look at simple tests.

## Running as a module versus running as a program

We put the regress function into a file.  That file is now imported rather
than being used directly.  We can use that with a neat addition to the bottom
of the file.  After the function is defined, add these lines.

```python
if __name__ == "__main__":
    print "I should run some tests here, shouldn't I?"
```

Then, try it out.

```bash
$ python my.py
I should run some tests here, shouldn't I?
```

but if you run `$ python my_project.py` it doesn't print that output.  Why
not?  The file that you run directly with the `python` command will always
be called `__main__`, and everything that it uses will have some other name.
We don't need to know why, just that it is, and that lets us put code in
that conditional at the bottom that only gets run when we run `my.py` directly.
Testing it is one of the main reasons why one might want to run it directly,
so let's add an error check and a test to see if it works.

## Check for data type

There are two ways that we could check the type of incoming data.  We can
explicitly check type with something like `isinstance(Y, np.ndarray)`.
That's fine and good, but we could also use the `try...except` structure
we saw a while back, and if the data is good, we make progress, and if it
is not, we exit with an error.

We could use

```python
if not isinstance(Y, np.ndarray) or not isinstance(X, np.ndarray):
    print("Either X or Y is not a NumPy array.  Bye")
    return float("NaN")
```

You could split that up and test separately for `X` and `Y`.  That
might be better.  Or we could use something like this.

```python
try:
    Y = Y[:, np.newaxis]
except TypeError:
    print "Y is not a NumPy array, perhaps?"
    return float('NaN')
```

That's kind of nice because we have to do `Y = Y[:, np.newaxis]` anyway
and if `Y` is the right stuff, we did it, and if not, we can bail out.
Similarly, we could do

```python
try:
    ones = np.ones(X.shape[0])
except TypeError:
    print "X is not a NumPy array, perhaps?"
    return float('NaN')
```
for `X`.  I kind of like this approach over the checking type, so let's
put that into our `my.py` file.  Mine now looks like

```python
import numpy as np
def regress(Y, X):
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
    . . . .
```

Put that in your version, make sure that it still runs properly with
the data we have.

OK, so now we need to put in the test at the bottom to make sure that
our test fails when it should.

The part that comes after we test what the `__name__` is is just a regular
Python script, so anything you can do in one, you can do here.  This is what
I put in first.

```python
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
