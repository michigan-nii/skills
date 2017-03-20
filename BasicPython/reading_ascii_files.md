# Some notes on doing homeworks

I was working on an exercise from the Enthought training to grab data
from a file with 33,271 lines.  I scratched my head over it for a while
and came up with this

`read_ascii.py`

```python
# Create an empty dictionary
logs = dict()

with open('long_logs.crv') as log_file:
    # The first line is special then split to make a list
    header = log_file.readline().split()
    # Initialize an empty list for each column name so we can .append()
    for column in header:
        logs[column] = []
    # Now the rest of the data
    for line in log_file.readlines():
        line = line.split()
        for i in range(len(line)):
            logs[header[i]].append(line[i])
# Print the first few values from the first column
print header[0],": ", logs[header[0]][:10]
```

Here's their version.

`ascii_log_file_solution.py`

```python
log_file = open('long_logs.crv')

# The first line is a header that has all the log names:
header = log_file.readline()
log_names = header.split()
log_count = len(log_names)

# Read in each row of values, converting them to floats as
# they are read in.  Assign them to the log name for their
# particular column:
logs = {}

# Initialize the logs dictionary so that it contains the log names
# as keys, and an empty list for the values.
for name in log_names:
    logs[name] = []

for line in log_file:
    values = [float(val) for val in line.split()]
    for i, name in enumerate(log_names):
        logs[name].append(values[i])
log_file.close()

# output the first 10 values for the DEPTH log.
print 'DEPTH:', logs['DEPTH'][:10]
```

  Pretty similar, but I do have to remember that
`enumerate()` function, which prints out a list along with the index
of the element.  So, if a list has

```python
>>> x = ['a', 'b', 'c']
```

then `enumerate(x)` spits out

```python
(0, 'a')
(1, 'b')
(2, 'c')
```
and you can get both element index and its value with

```python
>>> j, name = enumerate(log_names)
```


Then, this is their fast one.

`ascii_log_file_solution2.py`


```python
"""
This version is about 35% faster than the original on largish files
because it reads in all the data at once and then uses array slicing
to assign the data elements to the correct column (or log).
"""
log_file = open('long_logs.crv')
# The first line is a header that has all the log names:
header = log_file.readline()
log_names = header.split()
log_count = len(log_names)

# Everything left is data.
# Now, read in all of the data in one fell swoop, translating
# it into floating point values as we go:
value_text = log_file.read()
values = [float(val) for val in value_text.split()]

# Once this is done, we can go back through and split the "columns" out
# of the values and associating them with their log names.  This can be
# done efficiently using strided slicing. The starting position for
# each log is just its column number, and, the "stride" for the slice
# is the number of logs in the file:
logs = {}
for offset, log_name in enumerate(log_names):
    logs[log_name] = values[offset::log_count]
print 'DEPTH:', logs['DEPTH'][:10]
```

The last one is kinda weird.  It's pretty much the same, except all the
data is read into one giant string(!), which it then splits with a "list
comprehension"

```python
>>> len(value_text)
>>> 8018070
>>> values = [float(val) for val in value_text.split()]
```

so it splits on whitespace boundaries into elements of a list, for each of which it
applies the `float()` function to convert to numbers, then all of those go into a giant
list called values.

```python
>>> len(values)
>>> 532320
```

This is the part I have a hard time thinking of ahead of time, and only get after staring at it for a minute or three.

```python
>>> values[offset::log_count]
```

Huh?  Oh, yeah.  `values[start:end:spacing]`

```python
   values[0::len(log_names)]
```

Remember, because there is nothing before the first and second colon, that
means "till the end", so that will grab every 15th element, starting from 0.
Next time it will be

```python
   values[1::len(log_names)]
   values[2::len(log_names)]
   etc.
```

Tricky buggers.

Anyway, there are a couple of ways to do the same thing.  In case you're curious,
here is the time it took them each.

```python
In [12]: run -t read_log.py
DEPTH:  ['182.500', '183.000', '183.500', '184.000', '184.500', '185.000', '185.500', '186.000', '186.500', '187.000']

IPython CPU timings (estimated):
  User   :       0.61 s.
  System :       0.02 s.
Wall time:       0.63 s.

In [13]: run -t ascii_log_file_solution.py
DEPTH: [182.5, 183.0, 183.5, 184.0, 184.5, 185.0, 185.5, 186.0, 186.5, 187.0]

IPython CPU timings (estimated):
  User   :       0.76 s.
  System :       0.02 s.
Wall time:       0.78 s.

In [14]: run -t ascii_log_file_solution2.py
DEPTH: [182.5, 183.0, 183.5, 184.0, 184.5, 185.0, 185.5, 186.0, 186.5, 187.0]

IPython CPU timings (estimated):
  User   :       0.36 s.
  System :       0.05 s.
Wall time:       0.42 s.

```

