def runme(xdata, xsize, ydata, ysize, numEntries, outdata, outsize):
    xsizeindex = 0
    ysizeindex = 0
    xdataindex = 0
    ydataindex = 0
    dataLength = 0
    sizeLength = 0

    for entry in range(numEntries):
        nest0size = xsize[xsizeindex]
        xsizeindex += 1

        outsize[sizeLength] = nest0size
        sizeLength += 1

        if nest0size == 0:
            # advance y because nest0 is x and there's a y loop above this level
            nest1size = ysize[ysizeindex]
            ysizeindex += 1
            for nest1 in range(nest1size):   # go all levels deep (only one here)
                ydataindex += 1

        ysizeunwind0 = ysizeindex
        ydataunwind0 = ydataindex
        for nest0 in range(nest0size):
            ysizeindex = ysizeunwind0
            ydataindex = ydataunwind0

            nest1size = ysize[ysizeindex]
            ysizeindex += 1

            outsize[sizeLength] = nest1size
            sizeLength += 1

            if nest1size == 0:
                # advance x because nest1 is y and there's an x loop above this level
                nest2size = xsize[xsizeindex]
                xsizeindex += 1
                for nest2 in range(nest2size):
                    xdataindex += 1

            xsizeunwind1 = xsizeindex
            xdataunwind1 = xdataindex
            for nest1 in range(nest1size):
                xsizeindex = xsizeunwind1
                xdataindex = xdataunwind1

                nest2size = xsize[xsizeindex]
                xsizeindex += 1

                outsize[sizeLength] = nest2size
                sizeLength += 1

                for nest2 in range(nest2size):
                    outdata[dataLength] = xdata[xdataindex] * 100 + ydata[ydataindex]
                    dataLength += 1

                    xdataindex += 1   # at the end of the nest2size loop because it's an xsize

                ydataindex += 1       # at the end of the nest1size loop because it's a ysize
