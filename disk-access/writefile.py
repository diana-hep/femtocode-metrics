import sys
import time

import numpy

single = numpy.array(xrange(-4096, 4096), dtype=numpy.float64)

startTime = time.time()
file = open(sys.argv[1], "wb")

# write it out 4*1024**2 times to make a 256 GB file
for i in xrange(4*1024**2):
    file.write(single.data)
    if i % 10000 == 0:
        print 1.0 * i / (4*1024**2)

file.close()
print "writing took", time.time() - startTime, "seconds"

# 573.141191006 seconds on i2.xlarge optimized SSD (450 MB/sec)
