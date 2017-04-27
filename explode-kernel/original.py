def runme(xdata, xsize, ydata, ysize, numEntries, outdata, outsize):
    countdown = [0, 0, 0]
    xdataindex = [0, 0, 0]
    xsizeindex = [0, 0, 0]
    ydataindex = [0, 0]
    ysizeindex = [0, 0]
    entry = 0
    dataLength = 0
    sizeLength = 0
    deepi = 0

    xskip = [False, False]     # a skip for each variable,
    yskip = [False]            # length == depth of the progression

    while entry < numEntries:
        if deepi != 0:
            countdown[deepi - 1] -= 1

        if deepi == 0:
            xsizeindex[1] = xsizeindex[0]
            xdataindex[1] = xdataindex[0]

            if True:           # check all the x skips below this point
                countdown[deepi] = xsize[xsizeindex[1]]
                xsizeindex[1] += 1
            if True:           # check anything below this point
                outsize[sizeLength] = countdown[deepi]
                sizeLength += 1

            if countdown[deepi] == 0:
                xskip[0] = True         # x and 0, like xsizeindex[0]
                countdown[deepi] = 1
            else:
                xskip[0] = False        # x and 0, like xsizeindex[0]

        elif deepi == 1:
            ysizeindex[1] = ysizeindex[0]
            ydataindex[1] = ydataindex[0]

            if True:           # check all the y skips below this point
                countdown[deepi] = ysize[ysizeindex[1]]
                ysizeindex[1] += 1
            if not xskip[0]:   # check anything below this point
                outsize[sizeLength] = countdown[deepi]
                sizeLength += 1

            if countdown[deepi] == 0:
                yskip[0] = True         # y and 0, like ysizeindex[0]
                countdown[deepi] = 1
            else:
                yskip[0] = False        # y and 0, like ysizeindex[0]

        elif deepi == 2:
            xsizeindex[2] = xsizeindex[1]
            xdataindex[2] = xdataindex[1]

            if not xskip[0]:   # check all the x skips below this point
                countdown[deepi] = xsize[xsizeindex[2]]
                xsizeindex[2] += 1
            if not xskip[0] and not yskip[0]:     # anything below this point
                outsize[sizeLength] = countdown[deepi]
                sizeLength += 1

            if countdown[deepi] == 0:
                xskip[1] = True         # x and 1, like xsizeindex[1]
                countdown[deepi] = 1
            else:
                xskip[1] = False        # x and 1, like xsizeindex[1]

        elif deepi == 3:
            deepi -= 1

            if not xskip[0] and not xskip[1] and not yskip[0]:
                               # check anything below this point
                outdata[dataLength] = xdata[xdataindex[2]] * 100 + ydata[ydataindex[1]]
                dataLength += 1

            if not xskip[0] and not xskip[1]:     # x skips below this point
                xdataindex[2] += 1

        deepi += 1

        while deepi != 0 and countdown[deepi - 1] == 0:
            deepi -= 1

            if deepi == 0:
                xsizeindex[0] = xsizeindex[1]
                xdataindex[0] = xdataindex[1]
                ysizeindex[0] = ysizeindex[1]
                ydataindex[0] = ydataindex[1]

            elif deepi == 1:
                xsizeindex[1] = xsizeindex[2]
                xdataindex[1] = xdataindex[2]

            elif deepi == 2:
                if not yskip[0]:                  # y skips below this point
                    ydataindex[1] += 1

        if deepi == 0:
            entry += 1
