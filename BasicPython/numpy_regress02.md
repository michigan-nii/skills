# Regression example

Here are the steps I used, in order.

Import NumPy, read the data from the `data.csv` file and print it (it's short).

```python
>>> import numpy as np
>>> data = np.loadtxt('data.csv', delimiter=',', skiprows=1)
>>> print(data)
[[  4.   33. ]
 [  4.5  42. ]
 [  5.   45. ]
 [  5.5  51. ]
 [  6.   53. ]
 [  6.5  61. ]
 [  7.   62. ]]
```

Create the Y and X vectors.  Y should be a column vector, so it needs
an extra dimension/axis, and X needs a column of 1s in addition to the
data column.

```python
>>> Y = data[:,1]
>>> Y
array([ 33.,  42.,  45.,  51.,  53.,  61.,  62.])
>>> Y = Y[:, np.newaxis]
>>> Y
array([[ 33.],
       [ 42.],
       [ 45.],
       [ 51.],
       [ 53.],
       [ 61.],
       [ 62.]])
>>> X = data[:,0]
>>> ones = np.ones(data.shape[0])
>>> ones
array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.])
>>> X = np.array([ones, X])
>>> X
array([[ 1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ],
       [ 4. ,  4.5,  5. ,  5.5,  6. ,  6.5,  7. ]])
```

I could stop with X here, but then I would have to transpose all the
Xs in (X'X)<sup>-1</sup> and everywhere else, and I _know_ I would lose
track, so

```python
>>> X = X.T
>>> X
array([[ 1. ,  4. ],
       [ 1. ,  4.5],
       [ 1. ,  5. ],
       [ 1. ,  5.5],
       [ 1. ,  6. ],
       [ 1. ,  6.5],
       [ 1. ,  7. ]])
```

I could code the whole equation directly with

```python
>>> np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), Y)
```

but do you really want to have to unpack that in a few months?
Maybe it's better to use some intermediary vegetables,

```python
>>> X_prime_X_inv = np.linalg.inv(np.dot(X.T, X))
>>> b = np.dot(
...     np.dot(X_prime_X_inv, X.T),
...     Y
... )
>>> b
array([[-2.67857143],
       [ 9.5       ]])
```

Usually when you do regression, you want to have the predicted values
and the residuals available, so lets make those.

```python
>>> Y_hat = np.dot(X, b)
>>> Y_hat
array([[ 35.32142857],
       [ 40.07142857],
       [ 44.82142857],
       [ 49.57142857],
       [ 54.32142857],
       [ 59.07142857],
       [ 63.82142857]])
>>> resid = Y - Y_hat
array([[-2.32142857],
       [ 1.92857143],
       [ 0.17857143],
       [ 1.42857143],
       [-1.32142857],
       [ 1.92857143],
       [-1.82142857]])
```

If we did all this correctly, then `Y - Y_hat - resid` should be a
column of zeros.

```python
>>> Y - Y_hat - resid
array([[ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.],
       [ 0.]])
```

and we can show off one last trick by creating a column vector of
zeros and using a test to see if it is equal to what we got just
now.

```python
>>> zero_vector = np.zeros(Y_hat.shape)
>>> zero_vector == Y - Y_hat - resid
array([[ True],
       [ True],
       [ True],
       [ True],
       [ True],
       [ True],
       [ True]], dtype=bool)
```

Let's print a table of coefficients.

```python
>>> print("b0:  %.6f\nb1:   %.6f" % (float(b[0]), float(b[1])))
b0:  -2.678571
b1:   9.500000
```

Finally, here's a gussied up version in a file ready to run.

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

OK, got it?  Good.  OK, you get to try this yourself.

Remember from your previous looks a regression output, there is
a table of sums of squares.  Typically, you'll see a total sums
of squares, sums of squares for regression, and sums of squares
for error.

If J is a square matrix all ones, that can be created by using

```python
>>> n = 3
>>> J = np.ones([n,n])
>>> J
array([[ 1.,  1.,  1.],
       [ 1.,  1.,  1.],
       [ 1.,  1.,  1.]])
```

the total sum of squares is shown in matrix notation as

Y'Y - 1/n * Y'JY

the sums of squares for regression (ssr) is given by

b'X'Y - 1/yY'JY

and the error sums of squares (sse) is given by

(Y - XB)'(Y - XB)

Our _n_ is `data.shape[0]`, and we are estimating only one parameter,
so the degrees of freedom for the residuals is `n - 2`.  An ANOVA
table for the regression would look like this.

```
Response: Y
              Df     Sum Sq  Mean Sq    F value
X             1      ssr     ssr/df     msr/mse
Residuals     n-2    sse     sse/df
```

and you should calculate the values for each of those.

