#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>

struct XS {
  double *xdata;
  uint64_t *xsize;
  uint64_t xdataindex;
  uint64_t xsizeindex;
};

void XS_init(struct XS *xs, double *xdata, uint64_t *xsize, uint64_t xdataindex, uint64_t xsizeindex) {
  xs->xdata = xdata;
  xs->xsize = xsize;
  xs->xdataindex = xdataindex;
  xs->xsizeindex = xsizeindex;
}

uint64_t XS_size(struct XS *xs) {
  return xs->xsize[xs->xsizeindex];
}

double XS_get(struct XS *xs) {
  return xs->xdata[xs->xdataindex];
}

void XS_next(struct XS *xs) {
  xs->xdataindex++;
}

struct XSS {
  double *xdata;
  uint64_t *xsize;
  uint64_t xdataindex;
  uint64_t xsizeindex;
};

void XSS_init(struct XSS *xss, double *xdata, uint64_t *xsize, uint64_t xdataindex, uint64_t xsizeindex) {
  xss->xdata = xdata;
  xss->xsize = xsize;
  xss->xdataindex = xdataindex;
  xss->xsizeindex = xsizeindex + 1;
}

uint64_t XSS_size(struct XSS *xss) {
  return xss->xsize[xss->xsizeindex - 1];
}

void XSS_getXS(struct XSS *xss, struct XS *xs) {
  XS_init(xs, xss->xdata, xss->xsize, xss->xdataindex, xss->xsizeindex);
}

void XSS_next(struct XSS *xss) {
  struct XS xs;
  XSS_getXS(xss, &xs);
  uint64_t xsize0 = XS_size(&xs);
  for (uint64_t i = 0;  i < xsize0;  ++i) {
    XS_next(&xs);
  }
  xss->xdataindex = xs.xdataindex;
  xss->xsizeindex = xs.xsizeindex;
  xss->xsizeindex++;
}

struct YS {
  double *ydata;
  uint64_t *ysize;
  uint64_t ydataindex;
  uint64_t ysizeindex;
};

void YS_init(struct YS *ys, double *ydata, uint64_t *ysize, uint64_t ydataindex, uint64_t ysizeindex) {
  ys->ydata = ydata;
  ys->ysize = ysize;
  ys->ydataindex = ydataindex;
  ys->ysizeindex = ysizeindex;
}

uint64_t YS_size(struct YS *ys) {
  return ys->ysize[ys->ysizeindex];
}

double YS_get(struct YS *ys) {
  return ys->ydata[ys->ydataindex];
}

void YS_next(struct YS *ys) {
  ys->ydataindex++;
}

struct Entry {
  uint64_t entry;
  uint64_t numEntries;

  double *xdata;
  uint64_t *xsize;
  uint64_t xdataindex;
  uint64_t xsizeindex;

  double *ydata;
  uint64_t ydataindex;
  uint64_t *ysize;
  uint64_t ysizeindex;
};

void Entry_init(struct Entry *entry, uint64_t numEntries, double *xdata, uint64_t *xsize, double *ydata, uint64_t *ysize) {
  entry->entry = 0;
  entry->numEntries = numEntries;
  entry->xdata = xdata;
  entry->xsize = xsize;
  entry->xdataindex = 0;
  entry->xsizeindex = 0;
  entry->ydata = ydata;
  entry->ysize = ysize;
  entry->ydataindex = 0;
  entry->ysizeindex = 0;
}

void Entry_getXSS(struct Entry *entry, struct XSS *xss) {
  XSS_init(xss, entry->xdata, entry->xsize, entry->xdataindex, entry->xsizeindex);
}

void Entry_getYS(struct Entry *entry, struct YS *ys) {
  YS_init(ys, entry->ydata, entry->ysize, entry->ydataindex, entry->ysizeindex);
}

void Entry_next(struct Entry *entry) {
  struct XSS xss;
  Entry_getXSS(entry, &xss);
  uint64_t xsize0 = XSS_size(&xss);
  for (uint64_t i = 0;  i < xsize0;  ++i) {
    XSS_next(&xss);
  }
  entry->xdataindex = xss.xdataindex;
  entry->xsizeindex = xss.xsizeindex;

  struct YS ys;
  Entry_getYS(entry, &ys);
  uint64_t ysize0 = YS_size(&ys);
  for (uint64_t i = 0;  i < ysize0;  ++i) {
    YS_next(&ys);
  }
  entry->ydataindex = ys.ydataindex;
  entry->ysizeindex = ys.ysizeindex;

  entry->entry++;
}

bool Entry_notdone(struct Entry *entry) {
  return entry->entry < entry->numEntries;
}

double runnaive(double *xdata, uint64_t *xsize, double *ydata, uint64_t *ysize, uint64_t numEntries) {
  double out = 0.0;
  struct Entry entry;
  Entry_init(&entry, numEntries, xdata, xsize, ydata, ysize);
  while (Entry_notdone(&entry)) {
    struct XSS xss;
    Entry_getXSS(&entry, &xss);
    uint64_t xsize0 = XSS_size(&xss);
    printf("[ ");
    for (uint64_t i = 0;  i < xsize0;  ++i) {
      struct XS xs;
      XSS_getXS(&xss, &xs);
      uint64_t xsize1 = XS_size(&xs);
      printf("[ ");
      for (uint64_t j = 0;  j < xsize1;  ++j) {
        double x = XS_get(&xs);
        printf("%g ", x);
        XS_next(&xs);
      }
      printf("] ");
      XSS_next(&xss);
    }
    printf("]\n");

    struct YS ys;
    Entry_getYS(&entry, &ys);
    uint64_t ysize0 = YS_size(&ys);
    printf("[ ");
    for (uint64_t i = 0;  i < ysize0;  ++i) {
      double y = YS_get(&ys);
      out += y;
      printf("%g ", y);
      YS_next(&ys);
    }
    printf("]\n");
    Entry_next(&entry);
  }
  return out;
}
