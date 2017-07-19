import glob

import numpy

hold = {}
values = {}
fd = None

for fileName in sorted(glob.glob("/home/pivarski/storage/test/test_*.npy")):
    print fileName
    fd = numpy.memmap(fileName, dtype="float64", mode="r", shape=(100,))
    values[fileName] = fd[0]

# limit is just above 2043

# no limit if you let them go out of scope
