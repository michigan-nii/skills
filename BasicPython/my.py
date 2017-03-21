import numpy as np

def regress(Y, X):
    Y = Y[:, np.newaxis]
    ones = np.ones(X.shape[0])
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
