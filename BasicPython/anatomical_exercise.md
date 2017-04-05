# From the Skills meeting on Tue, 4 Apr, 2017

Not all the questions in the exercise are really clearly labeled, but this
is what I came up with after looking at several of our attempts.

```python
### https://bic-berkeley.github.io/psych-214-fall-2016/anatomical_exercise.html

# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Connect to Qt graphical display for plotting.  This is an
# IPython magick
%pylab

# Read data and convert to np.array
image_array = np.loadtxt('anatomical.txt')

# How many pixel values?
print(image_array.shape)

# There are 32 slices, so the size / 32 is the number of pixels per slice
# Doing that integer division thing to get the variable type right
P = int(image_array.shape[0]) // 32

#- Find the size of a slice over the third dimension
print(P)

# Candidates for I and J
# We've all seen images of brains, so one way to consider the range of
# possible values would be to find the middle value (the square root), then
# take about 70% of that as the lower value and 170% as the upper, yes?
# Both should be integers.

lower = int(np.sqrt(P) * .70)
upper = int(np.sqrt(P) * 1.70)

# There are several ways to do this.
##########
# Method 1  Create the Is and Js with standard Python and conditional

I = []
J = []

for i in range(lower,upper+1):
    if P % i == 0:
        I.append(i)
        J.append(P // i)
print(I)
print(J)
##########


##########
# Method 2  Use NumPy to do this

# Create an array with all the integers from upper to lower
cI = np.array(range(lower,upper+1))

# The following will run through the array and only keep values
# for which the same condition above is true.
cI = cI[P % cI == 0]

# Create the Js
cJ = P // cI

print(cI)
print(cJ)
##########

#  Use the fifth entry from I,J as an example
slice = image_array.reshape(I[5], J[5], 32)

#  Display the fifteenth slice from the reshaped data
plt.imshow(slice[:,:,15])

for i in range(len(I)):
    # Set the slice to the current shape values for I and J
    slice = image_array.reshape(I[i], J[i], 32)
    # Print the I, J values in the terminal
    print("Displaying image using I = {} and J = {}").format(I[i], J[i])
    # Show the corresponding image
    plt.imshow(slice[:,:,15])
    # Here are are getting some useless keyboard input as a way to pause
    # between displaying slices.  After messing with this, I decided to put
    # it in a try:...except: so that I don't get the ugly, distressing
    # traceback when I get to the one I want.  Now, Ctrl-C, Return prints
    # a civilized message.
    try:
        x = raw_input("Press Return to continue, Ctrl-C then Return to stop.")
    except KeyboardInterrupt:
        print("Stopping")
        break
    # By putting in the plt.close(), we reset the image window so that
    # the next image will appear.
    plt.close()
    ```
