import time

import numba
import numpy

# @numba.njit
# def iterator(numEntries):
#     for n in range(numEntries):
#         yield n

# @numba.njit
# def useiterator(numEntries):
#     out = 0
#     for n in iterator(numEntries):
#         out += n
#     return out

# @numba.njit
# def useloop(numEntries):
#     out = 0
#     for n in range(numEntries):
#         out += n
#     return out

# def test1(numEntries):
#     useiterator(10)
#     startTime = time.time()
#     useiterator(numEntries)
#     endTime = time.time()
#     print endTime - startTime

# def test2(numEntries):
#     useloop(10)
#     startTime = time.time()
#     useloop(numEntries)
#     endTime = time.time()
#     print endTime - startTime

# test1(1000000000)
# test2(1000000000)

@numba.njit
def getentries(xdata, xsize, ydata, ysize, numEntries):
    entry_xdataindex = 0
    entry_xsizeindex = 0
    entry_ydataindex = 0
    entry_ysizeindex = 0

    for n in range(numEntries):
        yield entry_xdataindex, entry_xsizeindex, entry_ydataindex, entry_ysizeindex

        xnest0 = xsize[entry_xsizeindex]
        entry_xsizeindex += 1
        for i in range(xnest0):
            xnest1 = xsize[entry_xsizeindex]
            entry_xsizeindex += 1
            for j in range(xnest1):
                entry_xdataindex += 1

        ynest0 = ysize[entry_ysizeindex]
        entry_ysizeindex += 1
        for i in range(ynest0):
            entry_ydataindex += 1

@numba.njit
def getxss(xdata, xsize, xss_xdataindex, xss_xsizeindex):
    xss_xsizeindex += 1
    for i in range(xsize[xss_xsizeindex - 1]):
        yield xss_xdataindex, xss_xsizeindex

        xnest1 = xsize[xss_xsizeindex]
        xss_xsizeindex += 1
        for j in range(xnest1):
            xss_xdataindex += 1

@numba.njit
def getxs(xdata, xsize, xs_xdataindex, xs_xsizeindex):
    for i in range(xsize[xs_xsizeindex]):
        yield xs_xdataindex, xs_xsizeindex
        xs_xdataindex += 1

@numba.njit
def getys(ydata, ysize, ys_ydataindex, ys_ysizeindex):
    for i in range(ysize[ys_ysizeindex]):
        yield ys_ydataindex, ys_ysizeindex
        ys_ydataindex += 1

@numba.njit
def runsmarter(xdata, xsize, ydata, ysize, numEntries):
    out = 0.0
    for entry in getentries(xdata, xsize, ydata, ysize, numEntries):
        xss_xdataindex, xss_xsizeindex, ys_ydataindex, ys_ysizeindex = entry

        # print "[",
        for xss in getxss(xdata, xsize, xss_xdataindex, xss_xsizeindex):
            xs_xdataindex, xs_xsizeindex = xss

            # print "[",
            for ys in getys(ydata, ysize, ys_ydataindex, ys_ysizeindex):
                y_ydataindex, y_ysizeindex = ys

                # print "[",
                for xs in getxs(xdata, xsize, xs_xdataindex, xs_xsizeindex):
                    x_xdataindex, x_xsizeindex = xs

                    x = xdata[x_xdataindex]
                    y = ydata[y_ydataindex]
                    # print 100*x + y,
                    out += 100*x + y

                # print "]",

            # print "]",

        # print "]"

xdata = []
xsize = []
ydata = []
ysize = []

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += [7, 8, 9, 10, 11, 12]
xsize += [3, 0, 0, 0, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += [7, 8, 9, 10, 11, 12]
xsize += [0, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += [1, 2, 3, 4, 5, 6]
xsize += [3, 2, 2, 2, 3, 0, 0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += [1, 2, 3, 4, 5, 6]
xsize += [3, 2, 2, 2, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += []
xsize += [3, 0, 0, 0, 3, 0, 0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += []
xsize += [0, 3, 0, 0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += []
xsize += [0, 0]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [1, 2, 3, 4]
ysize += [4, 0]

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += []
ysize += [0, 0]

xdata += [7, 8, 9, 10, 11, 12]
xsize += [3, 0, 0, 0, 3, 2, 2, 2]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

xdata += [7, 8, 9, 10, 11, 12]
xsize += [0, 3, 2, 2, 2]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

xdata += []
xsize += [0, 3, 0, 0, 0]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

xdata += []
xsize += [0, 0]
ydata += [5, 6, 7, 8]
ysize += [0, 4]

multiplier = 10000

bigxdata = numpy.empty(len(xdata) * multiplier, dtype=numpy.float64)
bigxsize = numpy.empty(len(xsize) * multiplier, dtype=numpy.uint64)
bigydata = numpy.empty(len(ydata) * multiplier, dtype=numpy.float64)
bigysize = numpy.empty(len(ysize) * multiplier, dtype=numpy.uint64)

for i in range(multiplier):
    bigxdata[i * len(xdata) : (i + 1) * len(xdata)] = xdata
    bigxsize[i * len(xsize) : (i + 1) * len(xsize)] = xsize
    bigydata[i * len(ydata) : (i + 1) * len(ydata)] = ydata
    bigysize[i * len(ysize) : (i + 1) * len(ysize)] = ysize

for i in range(100):
    startTime = time.time()
    runsmarter(bigxdata, bigxsize, bigydata, bigysize, 30 * multiplier)
    endTime = time.time()
    print endTime - startTime, 1e-6 * 2400000 / (endTime - startTime), "MHz"

