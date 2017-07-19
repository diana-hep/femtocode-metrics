import time
import gc

import numpy
import numba

N = 100L*1024L*1024L/8L
fp = None

for i in range(5):
    del fp
    gc.collect()
    print "new mmap"
    fp = numpy.memmap("/home/pivarski/storage/data/00000000-0000-0000-0000-000000000000.root", dtype="float64", mode="r", shape=(N,))

    @numba.njit
    def doit():
        out = 0.0
        for i in range(N):
            out += fp[i]
        return out

    for j in range(5):
        startTime = time.time()
        out = doit()
        endTime = time.time()

        print "time:", endTime - startTime

# new mmap
# time: 0.262980937958
# time: 0.0277998447418
# time: 0.0248579978943
# time: 0.0249099731445
# time: 0.0249691009521
# new mmap
# time: 0.155894994736
# time: 0.0281360149384
# time: 0.0248420238495
# time: 0.0249018669128
# time: 0.0251679420471
# new mmap
# time: 0.155912160873
# time: 0.0279729366302
# time: 0.0248610973358
# time: 0.0249500274658
# time: 0.0248959064484
# new mmap
# time: 0.155367851257
# time: 0.0282669067383
# time: 0.0260469913483
# time: 0.0253510475159
# time: 0.0247399806976
# new mmap
# time: 0.154551029205
# time: 0.0249660015106
# time: 0.0252799987793
# time: 0.0252161026001
# time: 0.0252120494843
