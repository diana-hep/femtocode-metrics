import time

import numpy
import numba

fp = numpy.memmap("/mnt/sdb-instancestore/big-file.raw", dtype="float64", mode="r", shape=(40L*1024L*1024L*1024L/8L,))

N = 40L*1024L*1024L*1024L/8L

@numba.njit
def doit():
    out = 0.0
    for i in range(N):
        out += fp[i]
    return out

startTime = time.time()
# out = fp.sum()
out = doit()
endTime = time.time()

print "out:", out, "time:", endTime - startTime

# 40 GB: 114.687829018
# 100 GB: 287.973561049 seconds
# factor of 2.51093392834041 (100/40)

# 356 MB/sec

# 25% slower than read-and-drop, but get the added benefit of keeping whole columns in RAM

# ulimits don't seem to affect it


