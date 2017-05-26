from collections import namedtuple
import time

import numba
import numpy

Column = namedtuple("Column", ["data", "size", "dataindex", "sizeindex"])
Entry = namedtuple("Entry", ["x", "y"])

@numba.njit
def Column_update(copyto, copyfrom):
    copyto.dataindex = copyfrom.dataindex
    copyto.sizeindex = copyfrom.sizeindex

@numba.njit
def XS_init(data, size, dataindex, sizeindex):
    return Column(data, size, dataindex, sizeindex)

@numba.njit
def XS_size(xs):
    return xs.size[xs.sizeindex]

@numba.njit
def XS_get(xs):
    return xs.data[xs.dataindex]

@numba.njit
def XS_next(xs):
    xs.dataindex += 1

@numba.njit
def XSS_init(data, size, dataindex, sizeindex):
    return Column(data, size, dataindex, sizeindex + 1)

@numba.njit
def XSS_size(xss):
    return xss.size[xss.sizeindex - 1]

@numba.njit
def XSS_getXS(xss):
    return Column(xss.data, xss.size, xss.dataindex, xss.sizeindex)

@numba.njit
def XSS_next(xss):
    xs = XSS_getXS(xss)
    for i in range(XS_size(xs)):
        XS_next(xs)
    Column_update(xss, xs)
    xss.sizeindex += 1

@numba.njit
def YS_init(data, size, dataindex, sizeindex):
    return Column(data, size, dataindex, sizeindex)

@numba.njit
def YS_size(ys):
    return ys.size[ys.sizeindex]

@numba.njit
def YS_get(ys):
    return ys.data[ys.dataindex]

@numba.njit
def YS_next(ys):
    ys.dataindex += 1

@numba.njit
def Entry_init(xdata, xsize, ydata, ysize):
    return Entry(Column(xdata, xsize, 0, 0), Column(ydata, ysize, 0, 0))

@numba.njit
def Entry_getXSS(entry):
    return XSS_init(entry.x.data, entry.x.size, entry.x.dataindex, entry.x.sizeindex)

@numba.njit
def Entry_getYS(entry):
    return YS_init(entry.y.data, entry.y.size, entry.y.dataindex, entry.y.sizeindex)

@numba.njit
def Entry_next(entry):
    xss = Entry_getXSS(entry)
    for i in range(XSS_size(xss)):
        XSS_next(xss)
    Column_update(entry.x, xss)

    ys = Entry_getYS(entry)
    for i in range(YS_size(ys)):
        YS_next(ys)
    Column_update(entry.y, ys)

@numba.njit
def runsmart(xdata, xsize, ydata, ysize, numEntries):
    out = 0.0
    entry = Entry_init(xdata, xsize, ydata, ysize)
    for n in range(numEntries):

        xss = Entry_getXSS(entry)
        for i in range(XSS_size(xss)):

            ys = Entry_getYS(entry)
            for j in range(YS_size(ys)):

                xs = XSS_getXS(xss)
                for k in range(XS_size(xs)):

                    x = XS_get(xs)
                    y = YS_get(ys)
                    out += 100*x + y

                    XS_next(xs)

                YS_next(ys)

            XSS_next(xss)

        Entry_next(entry)

    return out

xdata = []
xsize = []
ydata = []
ysize = []

xdata += [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
xsize += [3, 2, 2, 2, 3, 2, 2, 2]
ydata += [1, 2, 3, 4, 5, 6, 7, 8]
ysize += [4, 4]

print runsmart(xdata, xsize, ydata, ysize, 2)
