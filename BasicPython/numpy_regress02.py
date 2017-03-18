#!/usr/bin/env python

import numpy as np

data = np.loadtxt('data.csv', delimiter=',', skiprows=1)
print(data)
# print the first column using slice notation
print(data[:,0])
# print the first row using slice notation
print(data[0,:])
# print its dimensions
data.shape
# what kind of data prints with enclosing parentheses?
# so we can do this, right?
print(data.shape[0])
print(data.shape[1])
# create variable called num_rows and num_cols with correct data
# what gives with this?
print(data[:,0])
print(data[:,0].T)
# print a vector of ones
print(np.ones(data.shape[0]))
# create the ones vector
ones = np.ones(data.shape[0])
x = data[:,0]
# The following gives an error.  why?  Fix it
X = np.array([ones, x])
# Whazza matta wid dis?
print(X)
# How do you get it into the right shape?
# Compare the output of
# X.reshape(7,2)
# and
# X.T
# Is this the right one?
X = X.T
# Create the vector of dependent measures
Y = data[:,1]
print(Y)
# Oh, that thing again...  Not a column
# Much googling...
Y = Y[:, np.newaxis]
print(Y)
# Further googling reveals
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.expand_dims.html
# Y = np.expand_dims(Y, axis=1)
X_prime_X = np.dot(X.T, X)
print(X_prime_X)
X_prime_X_inverse = np.linalg.inv(X_prime_X)
# Need the X'Y matrix for intermediate calculations
X_prime_Y = np.dot(X.T, Y)
# the vector of coefficients is (X'X)^{-1}X^{-1}Y
b = np.dot(X_prime_X_inverse, X_prime_Y)
# calculate the predicted values
Y_hat = np.dot(X,b)
print(Y_hat)
# calculate the residuals, error vector
residuals = Y - np.dot(X,b)
print(residuals)
# check our work
zeros = np.zeros(data.shape[0])
# need this trick again
zeros = np.expand_dims(zeros, axis=1)
# do we get our data back?
data_check = Y_hat + residuals
print(data_check - Y == zeros)



