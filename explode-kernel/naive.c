#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>

struct XS {
  double *xdata;
  uint64_t *xsize;
  uint64_t xdataindex;
  uint64_t xsizeindex;
};

inline void XS_init(struct XS *xs, double *xdata, uint64_t *xsize, uint64_t xdataindex, uint64_t xsizeindex) {
  xs->xdata = xdata;
  xs->xsize = xsize;
  xs->xdataindex = xdataindex;
  xs->xsizeindex = xsizeindex;
}

inline uint64_t XS_size(struct XS *xs) {
  return xs->xsize[xs->xsizeindex];
}

inline double XS_get(struct XS *xs) {
  return xs->xdata[xs->xdataindex];
}

inline void XS_next(struct XS *xs) {
  xs->xdataindex++;
}

struct XSS {
  double *xdata;
  uint64_t *xsize;
  uint64_t xdataindex;
  uint64_t xsizeindex;
};

inline void XSS_init(struct XSS *xss, double *xdata, uint64_t *xsize, uint64_t xdataindex, uint64_t xsizeindex) {
  xss->xdata = xdata;
  xss->xsize = xsize;
  xss->xdataindex = xdataindex;
  xss->xsizeindex = xsizeindex + 1;
}

inline uint64_t XSS_size(struct XSS *xss) {
  return xss->xsize[xss->xsizeindex - 1];
}

inline void XSS_getXS(struct XSS *xss, struct XS *xs) {
  XS_init(xs, xss->xdata, xss->xsize, xss->xdataindex, xss->xsizeindex);
}

inline void XSS_next(struct XSS *xss) {
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

inline void YS_init(struct YS *ys, double *ydata, uint64_t *ysize, uint64_t ydataindex, uint64_t ysizeindex) {
  ys->ydata = ydata;
  ys->ysize = ysize;
  ys->ydataindex = ydataindex;
  ys->ysizeindex = ysizeindex;
}

inline uint64_t YS_size(struct YS *ys) {
  return ys->ysize[ys->ysizeindex];
}

inline double YS_get(struct YS *ys) {
  return ys->ydata[ys->ydataindex];
}

inline void YS_next(struct YS *ys) {
  ys->ydataindex++;
}

struct Entry {
  double *xdata;
  uint64_t *xsize;
  uint64_t xdataindex;
  uint64_t xsizeindex;

  double *ydata;
  uint64_t ydataindex;
  uint64_t *ysize;
  uint64_t ysizeindex;
};

inline void Entry_init(struct Entry *entry, double *xdata, uint64_t *xsize, double *ydata, uint64_t *ysize) {
  entry->xdata = xdata;
  entry->xsize = xsize;
  entry->xdataindex = 0;
  entry->xsizeindex = 0;
  entry->ydata = ydata;
  entry->ysize = ysize;
  entry->ydataindex = 0;
  entry->ysizeindex = 0;
}

inline void Entry_getXSS(struct Entry *entry, struct XSS *xss) {
  XSS_init(xss, entry->xdata, entry->xsize, entry->xdataindex, entry->xsizeindex);
}

inline void Entry_getYS(struct Entry *entry, struct YS *ys) {
  YS_init(ys, entry->ydata, entry->ysize, entry->ydataindex, entry->ysizeindex);
}

inline void Entry_next(struct Entry *entry) {
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
}

double runnaive(double *xdata, uint64_t *xsize, double *ydata, uint64_t *ysize, uint64_t numEntries) {
  // struct Entry entry;
  // Entry_init(&entry, xdata, xsize, ydata, ysize);
  // for (uint64_t n = 0;  n < numEntries;  ++n) {
  //   struct XSS xss;
  //   Entry_getXSS(&entry, &xss);
  //   uint64_t xsize0 = XSS_size(&xss);
  //   printf("[ ");
  //   for (uint64_t i = 0;  i < xsize0;  ++i) {
  //     struct XS xs;
  //     XSS_getXS(&xss, &xs);
  //     uint64_t xsize1 = XS_size(&xs);
  //     printf("[ ");
  //     for (uint64_t j = 0;  j < xsize1;  ++j) {
  //       double x = XS_get(&xs);
  //       printf("%g ", x);
  //       XS_next(&xs);
  //     }
  //     printf("] ");
  //     XSS_next(&xss);
  //   }
  //   printf("]\n");

  //   struct YS ys;
  //   Entry_getYS(&entry, &ys);
  //   uint64_t ysize0 = YS_size(&ys);
  //   printf("[ ");
  //   for (uint64_t i = 0;  i < ysize0;  ++i) {
  //     double y = YS_get(&ys);
  //     printf("%g ", y);
  //     YS_next(&ys);
  //   }
  //   printf("]\n");
  //   Entry_next(&entry);
  // }

  double out = 0.0;
  struct Entry entry;
  Entry_init(&entry, xdata, xsize, ydata, ysize);
  for (uint64_t n = 0;  n < numEntries;  ++n) {

    // printf("[ ");
    struct XSS xss;
    Entry_getXSS(&entry, &xss);
    uint64_t xss_size = XSS_size(&xss);
    for (uint64_t i = 0;  i < xss_size;  ++i) {

      // printf("[ ");
      struct YS ys;
      Entry_getYS(&entry, &ys);
      uint64_t ys_size = YS_size(&ys);
      for (uint64_t j = 0;  j < ys_size;  ++j) {

        // printf("[ ");
        struct XS xs;
        XSS_getXS(&xss, &xs);
        uint64_t xs_size = XS_size(&xs);
        for (uint64_t k = 0;  k < xs_size;  ++k) {

          double x = XS_get(&xs);
          double y = YS_get(&ys);
          out += 100*x + y;

          // printf("%g ", 100*x + y);

          XS_next(&xs);
        }
        // printf("] ");

        YS_next(&ys);
      }
      // printf("] ");

      XSS_next(&xss);
    }
    // printf("]");

    Entry_next(&entry);
    // printf("\n");
  }
  return out;
}
