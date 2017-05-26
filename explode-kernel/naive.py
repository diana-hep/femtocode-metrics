from collections import namedtuple
import time

import numpy
import numba

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

# @numba.jit(nopython=True)
# def dummy1(n):
#     out = 0
#     for j in range(n):
#         xss = []
#         for i in range(10000):
#             xss.append(i*i)
#         for xi in xss:
#             out += xi
#     return out

# @numba.jit(nopython=True)
# def dummy2(n):
#     out = 0
#     for j in range(n):
#         xss = [0] * 10000
#         for i in range(10000):
#             xss[i] = i*i
#         for xi in xss:
#             out += xi
#     return out

# def doit():
#     dummy1(1000)
#     dummy2(1000)
#     startTime = time.time()
#     dummy1(10000)
#     endTime = time.time()
#     print endTime - startTime
#     startTime = time.time()
#     dummy2(10000)
#     endTime = time.time()
#     print endTime - startTime

# doit()


@numba.jitclass([
    ("xdata", numba.float64[:]),
    ("xsize", numba.uint64[:]),
    ("xsizeindex", numba.uint64),
    ("xdataindex", numba.uint64)])
class XS(object):
    def __init__(self, xdata, xsize, xsizeindex, xdataindex):
        self.xdata = xdata
        self.xsize = xsize
        self.xsizeindex = xsizeindex
        self.xdataindex = xdataindex

    @property
    def size(self):
        return self.xsize[self.xsizeindex]

    @property
    def iterate(self):
        dataoffset = 0
        for i in range(self.xsize[self.xsizeindex]):
            yield self.xdata[self.xdataindex + dataoffset]
            dataoffset += 1

    def get(self, index):
        dataoffset = 0
        for i in range(self.xsize[self.xsizeindex]):
            if i == index:
                return self.xdata[self.xdataindex + dataoffset]
            dataoffset += 1
        raise IndexError("ouch")

@numba.jitclass([
    ("xdata", numba.float64[:]),
    ("xsize", numba.uint64[:]),
    ("xsizeindex", numba.uint64),
    ("xdataindex", numba.uint64)])
class XSS(object):
    def __init__(self, xdata, xsize, xsizeindex, xdataindex):
        self.xdata = xdata
        self.xsize = xsize
        self.xsizeindex = xsizeindex
        self.xdataindex = xdataindex

    @property
    def size(self):
        return self.xsize[self.xsizeindex]

    @property
    def iterate(self):
        sizeoffset = 0
        dataoffset = 0
        for i in range(self.xsize[self.xsizeindex + sizeoffset]):
            sizeoffset += 1
            yield XS(self.xdata, self.xsize, self.xsizeindex + sizeoffset, self.xdataindex + dataoffset)
            for j in range(self.xsize[self.xsizeindex + sizeoffset]):
                dataoffset += 1

    def get(self, index):
        sizeoffset = 0
        dataoffset = 0
        for i in range(self.xsize[self.xsizeindex + sizeoffset]):
            sizeoffset += 1
            if i == index:
                return XS(self.xdata, self.xsize, self.xsizeindex + sizeoffset, self.xdataindex + dataoffset)
            for j in range(self.xsize[self.xsizeindex + sizeoffset]):
                dataoffset += 1
        raise IndexError("ouch")

@numba.jitclass([
    ("ydata", numba.float64[:]),
    ("ysize", numba.uint64[:]),
    ("ysizeindex", numba.uint64),
    ("ydataindex", numba.uint64)])
class YS(object):
    def __init__(self, ydata, ysize, ysizeindex, ydataindex):
        self.ydata = ydata
        self.ysize = ysize
        self.ysizeindex = ysizeindex
        self.ydataindex = ydataindex

    @property
    def size(self):
        return self.ysize[self.ysizeindex]

    @property
    def iterate(self):
        dataoffset = 0
        for i in range(self.ysize[self.ysizeindex]):
            yield self.ydata[self.ydataindex + dataoffset]
            dataoffset += 1

    def get(self, index):
        dataoffset = 0
        for i in range(self.ysize[self.ysizeindex]):
            if i == index:
                return self.ydata[self.ydataindex + dataoffset]
            dataoffset += 1
        raise IndexError("ouch")

@numba.jitclass([
    ("xdata", numba.float64[:]),
    ("xsize", numba.uint64[:]),
    ("ydata", numba.float64[:]),
    ("ysize", numba.uint64[:]),
    ("xsizeindex", numba.uint64),
    ("xdataindex", numba.uint64),
    ("ysizeindex", numba.uint64),
    ("ydataindex", numba.uint64)])
class Entry(object):
    def __init__(self, xdata, xsize, ydata, ysize, xsizeindex, xdataindex, ysizeindex, ydataindex):
        self.xdata = xdata
        self.xsize = xsize
        self.ydata = ydata
        self.ysize = ysize
        self.xsizeindex = xsizeindex
        self.xdataindex = xdataindex
        self.ysizeindex = ysizeindex
        self.ydataindex = ydataindex

    @property
    def xss(self):
        return XSS(self.xdata, self.xsize, self.xsizeindex, self.xdataindex)

    @property
    def ys(self):
        return YS(self.ydata, self.ysize, self.ysizeindex, self.ydataindex)

@numba.jit(nopython=True)
def entries(xdata, xsize, ydata, ysize, numEntries):
    xsizeindex = 0
    xdataindex = 0
    ysizeindex = 0
    ydataindex = 0
    for entry in range(numEntries):
        yield Entry(xdata, xsize, ydata, ysize, xsizeindex, xdataindex, ysizeindex, ydataindex)

        xnest0 = xsize[xsizeindex]
        xsizeindex += 1
        for i in range(xnest0):
            xnest1 = xsize[xsizeindex]
            xsizeindex += 1
            for j in range(xnest1):
                xdataindex += 1

        ynest0 = ysize[ysizeindex]
        ysizeindex += 1
        for i in range(ynest0):
            ydataindex += 1

@numba.jit(nopython=True)
def runnaive(xdata, xsize, ydata, ysize, numEntries):
    out = 0.0
    for entry in entries(xdata, xsize, ydata, ysize, numEntries):
        # xss = entry.xss
        # ys = entry.ys
        # for i in range(xss.size):
        #     xs = xss.get(i)
        #     for j in range(ys.size):
        #         y = ys.get(j)
        #         for k in range(xs.size):
        #             x = xs.get(k)
        #             out += 100*x + y
        for xs in entry.xss.iterate:
            for y in entry.ys.iterate:
                for x in xs.iterate:
                    out += 100*x + y
    return out

for i in range(100):
    startTime = time.time()
    runnaive(bigxdata, bigxsize, bigydata, bigysize, 30 * multiplier)
    endTime = time.time()
    print endTime - startTime

# @numba.jit(nopython=True)
# def runnaive(xdata, xsize, ydata, ysize, numEntries):
#     xsizeindex = 0
#     ysizeindex = 0
#     xdataindex = 0
#     ydataindex = 0

#     out = 0

#     for entry in range(numEntries):
#         xsize0 = xsize[xsizeindex]
#         xsizeindex += 1
#         xss = [[0]] * xsize0
#         # for i in range(xsize0):
#         #     xsize1 = xsize[xsizeindex]
#         #     xsizeindex += 1
#         #     xs = [0] * xsize1
#         #     for j in range(xsize1):
#         #         xs[j] = xdata[xdataindex]
#         #         xdataindex += 1
#         #     xss[i] = xs

#         ysize0 = ysize[ysizeindex]
#         ysizeindex += 1
#         ys = [0] * ysize0
#         for i in range(ysize0):
#             ys[i] = ydata[ydataindex]
#             ydataindex += 1

#         # for xs in xss:
#         #     for y in ys:
#         #         for x in xs:
#         #             out += 100*x + y

#         for y in ys:
#             out += y

#     return out

# print runnaive(bigxdata, bigxsize, bigydata, bigysize, 30 * multiplier)

# for entry in entries(xdata, xsize, ydata, ysize, 2):
#     # print "[",
#     # for xs in entry.xss:
#     #     print "[",
#     #     for x in xs:
#     #         print x,
#     #     print "]",
#     # print "]"
#     # print "[",
#     # for y in entry.ys:
#     #     print y,
#     # print "]"

#     print "[",
#     xss = entry.xss
#     for i in range(len(xss)):
#         xs = xss[i]
#         print "[",
#         for j in range(len(xs)):
#             x = xs[j]
#             print x,
#         print "]",
#     print "]"
#     print "[",
#     ys = entry.ys
#     for i in range(len(ys)):
#         y = ys[i]
#         print y,
#     print "]"
