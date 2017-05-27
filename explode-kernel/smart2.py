import time

import numba
import numpy

@numba.njit
def runsmart(xdata, xsize, ydata, ysize, numEntries):
    out = 0.0
    entry_xdataindex = 0
    entry_xsizeindex = 0
    entry_ydataindex = 0
    entry_ysizeindex = 0
    for n in range(numEntries):

        # print "[",
        xss_xdataindex = entry_xdataindex
        xss_xsizeindex = entry_xsizeindex + 1
        for i in range(xsize[xss_xsizeindex - 1]):

            # print "[",
            ys_ydataindex = entry_ydataindex
            ys_ysizeindex = entry_ysizeindex
            for j in range(ysize[entry_ysizeindex]):

                # print "[",
                xs_xdataindex = xss_xdataindex
                xs_xsizeindex = xss_xsizeindex
                for k in range(xsize[xs_xsizeindex]):

                    x = xdata[xs_xdataindex]
                    y = ydata[ys_ydataindex]
                    out += 100*x + y
                    # print 100*x + y,

                    xs_xdataindex += 1
                # print "]",

                ys_ydataindex += 1
            # print "]",

            xnest1 = xsize[xss_xsizeindex]
            xss_xsizeindex += 1
            for j in range(xnest1):
                xss_xdataindex += 1

        # print "]",

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

        # print

    return out

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
    runsmart(bigxdata, bigxsize, bigydata, bigysize, 30 * multiplier)
    endTime = time.time()
    print endTime - startTime, 1e-6 * 2400000 / (endTime - startTime), "MHz"
