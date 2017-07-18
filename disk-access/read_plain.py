import time

import numpy

CHUNK = 8192
out = 0.0

startTime = time.time()
f = open("/mnt/sdb-instancestore/big-file.raw", "rb")

for i in xrange(40L*1024L*1024L*1024L/8L/CHUNK):
    a = numpy.frombuffer(f.read(8*CHUNK)).view(numpy.float64)
    out += a.sum()

f.close()
print "out:", out, "time:", time.time() - startTime
