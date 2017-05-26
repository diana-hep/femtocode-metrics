def runme(xdata, xsize, ydata, ysize, numEntries, outdata, outsize):
    xsizeindex = 0
    ysizeindex = 0
    xdataindex = 0
    ydataindex = 0
    dataLength = 0
    sizeLength = 0

    out = 0.0

    for entry in range(numEntries):
    # entry = 0
    # while entry < numEntries:
        nest0size = xsize[xsizeindex]
        xsizeindex += 1

        # outsize[sizeLength] = nest0size
        sizeLength += 1

        if nest0size == 0:
            # advance y because nest0 is x and there's a y loop above this level
            nest1size = ysize[ysizeindex]
            ysizeindex += 1
            for nest1 in range(nest1size):   # go all levels deep (only one here)
            # nest1 = 0
            # while nest1 < nest1size:
                ydataindex += 1
                # nest1 += 1

        ysizeunwind0 = ysizeindex
        ydataunwind0 = ydataindex
        for nest0 in range(nest0size):
        # nest0 = 0
        # while nest0 < nest0size:
            ysizeindex = ysizeunwind0
            ydataindex = ydataunwind0

            nest1size = ysize[ysizeindex]
            ysizeindex += 1

            # outsize[sizeLength] = nest1size
            sizeLength += 1

            if nest1size == 0:
                # advance x because nest1 is y and there's an x loop above this level
                nest2size = xsize[xsizeindex]
                xsizeindex += 1
                for nest2 in range(nest2size):
                # nest2 = 0
                # while nest2 < nest2size:
                    xdataindex += 1
                    # nest2 += 1

            xsizeunwind1 = xsizeindex
            xdataunwind1 = xdataindex
            for nest1 in range(nest1size):
            # nest1 = 0
            # while nest1 < nest1size:
                xsizeindex = xsizeunwind1
                xdataindex = xdataunwind1

                nest2size = xsize[xsizeindex]
                xsizeindex += 1

                # outsize[sizeLength] = nest2size
                sizeLength += 1

                for nest2 in range(nest2size):
                # nest2 = 0
                # while nest2 < nest2size:
                    # outdata[dataLength] = xdata[xdataindex] * 100 + ydata[ydataindex]
                    out += xdata[xdataindex] * 100 + ydata[ydataindex]
                    dataLength += 1

                    xdataindex += 1   # at the end of the nest2size loop because it's an xsize

                    # nest2 += 1

                ydataindex += 1       # at the end of the nest1size loop because it's a ysize

                # nest1 += 1

            # nest0 += 1

        # entry += 1

    # assert xsizeindex == len(xsize)
    # assert xdataindex == len(xdata)
    # assert ysizeindex == len(ysize)
    # assert ydataindex == len(ydata)
    return out
