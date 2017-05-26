from nested import runme

def testy(xdata, xsize, ydata, ysize, numEvents):
    outdata = [None] * 1000
    outsize = [None] * 1000
    runme(xdata, xsize, ydata, ysize, numEvents, outdata, outsize)
    outdata[outdata.index(None):] = []
    outsize[outsize.index(None):] = []
    return outdata, outsize

xdata = []
xsize = []
ydata = []
ysize = []

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 2)

xdata += [7, 8, 9, 10, 11, 12]
xsize += [3, 0, 0, 0, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 4)

xdata += [7, 8, 9, 10, 11, 12]
xsize += [0, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 6)

xdata += [1, 2, 3, 4, 5, 6]
xsize += [3, 2, 2, 2, 3, 0, 0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 8)

xdata += [1, 2, 3, 4, 5, 6]
xsize += [3, 2, 2, 2, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 10)

xdata += []
xsize += [3, 0, 0, 0, 3, 0, 0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 12)

xdata += []
xsize += [0, 3, 0, 0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 14)

xdata += []
xsize += [0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

testy(xdata, xsize, ydata, ysize, 16)

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

testy(xdata, xsize, ydata, ysize, 18)

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [1, 2, 3, 4]
ysize += [4, 0]

testy(xdata, xsize, ydata, ysize, 20)

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += []
ysize += [0, 0]

testy(xdata, xsize, ydata, ysize, 22)

xdata += [7, 8, 9, 10, 11, 12]
xsize += [3, 0, 0, 0, 3, 2, 2, 2]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

testy(xdata, xsize, ydata, ysize, 24)

xdata += [7, 8, 9, 10, 11, 12]
xsize += [0, 3, 2, 2, 2]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

testy(xdata, xsize, ydata, ysize, 26)

xdata += []
xsize += [0, 3, 0, 0, 0]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

testy(xdata, xsize, ydata, ysize, 28)

xdata += []
xsize += [0, 0]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

outdata, outsize = testy(xdata, xsize, ydata, ysize, 30)

import numpy
import numba
import time

multiplier = 10000

bigxdata = numpy.empty(len(xdata) * multiplier, dtype=numpy.float64)
bigxsize = numpy.empty(len(xsize) * multiplier, dtype=numpy.uint64)
bigydata = numpy.empty(len(ydata) * multiplier, dtype=numpy.float64)
bigysize = numpy.empty(len(ysize) * multiplier, dtype=numpy.uint64)
bigoutdata = numpy.empty(len(outdata) * multiplier, dtype=numpy.float64)
bigoutsize = numpy.empty(len(outsize) * multiplier, dtype=numpy.uint64)

for i in range(multiplier):
    bigxdata[i * len(xdata) : (i + 1) * len(xdata)] = xdata
    bigxsize[i * len(xsize) : (i + 1) * len(xsize)] = xsize
    bigydata[i * len(ydata) : (i + 1) * len(ydata)] = ydata
    bigysize[i * len(ysize) : (i + 1) * len(ysize)] = ysize

compiled = numba.jit(nopython=True)(runme)

compiled(bigxdata, bigxsize, bigydata, bigysize, 30 * multiplier, bigoutdata, bigoutsize)

for i in range(100):
    startTime = time.time()
    compiled(bigxdata, bigxsize, bigydata, bigysize, 30 * multiplier, bigoutdata, bigoutsize)
    endTime = time.time()
    print endTime - startTime, 1e-6 * 2400000 / (endTime - startTime), "MHz"

