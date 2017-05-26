#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>

struct Column {
  double *data;
  uint64_t *size;
  uint64_t dataindex;
  uint64_t sizeindex;
};

inline void Column_update(struct Column *to, struct Column *from) {
  to->dataindex = from->dataindex;
  to->sizeindex = from->sizeindex;
}

inline void XS_init(struct Column *xs, double *data, uint64_t *size, uint64_t dataindex, uint64_t sizeindex) {
  xs->data = data;
  xs->size = size;
  xs->dataindex = dataindex;
  xs->sizeindex = sizeindex;
}

inline uint64_t XS_size(struct Column *xs) {
  return xs->size[xs->sizeindex];
}

inline double XS_get(struct Column *xs) {
  return xs->data[xs->dataindex];
}

inline void XS_next(struct Column *xs) {
  xs->dataindex++;
}

inline void XSS_init(struct Column *xss, double *data, uint64_t *size, uint64_t dataindex, uint64_t sizeindex) {
  xss->data = data;
  xss->size = size;
  xss->dataindex = dataindex;
  xss->sizeindex = sizeindex + 1;
}

inline uint64_t XSS_size(struct Column *xss) {
  return xss->size[xss->sizeindex - 1];
}

inline void XSS_getXS(struct Column *xss, struct Column *xs) {
  XS_init(xs, xss->data, xss->size, xss->dataindex, xss->sizeindex);
}

inline void XSS_next(struct Column *xss) {
  struct Column xs;
  XSS_getXS(xss, &xs);
  uint64_t size0 = XS_size(&xs);
  for (uint64_t i = 0;  i < size0;  ++i) {
    XS_next(&xs);
  }
  Column_update(xss, &xs);
  // xss->dataindex = xs.dataindex;
  // xss->sizeindex = xs.sizeindex;
  xss->sizeindex++;
}

inline void YS_init(struct Column *ys, double *data, uint64_t *size, uint64_t dataindex, uint64_t sizeindex) {
  ys->data = data;
  ys->size = size;
  ys->dataindex = dataindex;
  ys->sizeindex = sizeindex;
}

inline uint64_t YS_size(struct Column *ys) {
  return ys->size[ys->sizeindex];
}

inline double YS_get(struct Column *ys) {
  return ys->data[ys->dataindex];
}

inline void YS_next(struct Column *ys) {
  ys->dataindex++;
}

struct Entry {
  struct Column x;
  struct Column y;
};

inline void Entry_init(struct Entry *entry, double *xdata, uint64_t *xsize, double *ydata, uint64_t *ysize) {
  entry->x.data = xdata;
  entry->x.size = xsize;
  entry->x.dataindex = 0;
  entry->x.sizeindex = 0;
  entry->y.data = ydata;
  entry->y.size = ysize;
  entry->y.dataindex = 0;
  entry->y.sizeindex = 0;
}

inline void Entry_getXSS(struct Entry *entry, struct Column *xss) {
  XSS_init(xss, entry->x.data, entry->x.size, entry->x.dataindex, entry->x.sizeindex);
}

inline void Entry_getYS(struct Entry *entry, struct Column *ys) {
  YS_init(ys, entry->y.data, entry->y.size, entry->y.dataindex, entry->y.sizeindex);
}

inline void Entry_next(struct Entry *entry) {
  struct Column xss;
  Entry_getXSS(entry, &xss);
  uint64_t xsize0 = XSS_size(&xss);
  for (uint64_t i = 0;  i < xsize0;  ++i) {
    XSS_next(&xss);
  }
  Column_update(&(entry->x), &xss);
  // entry->x.dataindex = xss.dataindex;
  // entry->x.sizeindex = xss.sizeindex;

  struct Column ys;
  Entry_getYS(entry, &ys);
  uint64_t ysize0 = YS_size(&ys);
  for (uint64_t i = 0;  i < ysize0;  ++i) {
    YS_next(&ys);
  }
  Column_update(&(entry->y), &ys);
  // entry->y.dataindex = ys.dataindex;
  // entry->y.sizeindex = ys.sizeindex;
}

double runnaive(double *xdata, uint64_t *xsize, double *ydata, uint64_t *ysize, uint64_t numEntries) {
  // struct Entry entry;
  // Entry_init(&entry, xdata, xsize, ydata, ysize);
  // for (uint64_t n = 0;  n < numEntries;  ++n) {
  //   struct Column xss;
  //   Entry_getXSS(&entry, &xss);
  //   uint64_t xsize0 = XSS_size(&xss);
  //   printf("[ ");
  //   for (uint64_t i = 0;  i < xsize0;  ++i) {
  //     struct Column xs;
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

  //   struct Column ys;
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
    struct Column xss;
    Entry_getXSS(&entry, &xss);
    uint64_t xss_size = XSS_size(&xss);
    for (uint64_t i = 0;  i < xss_size;  ++i) {

      // printf("[ ");
      struct Column ys;
      Entry_getYS(&entry, &ys);
      uint64_t ys_size = YS_size(&ys);
      for (uint64_t j = 0;  j < ys_size;  ++j) {

        // printf("[ ");
        struct Column xs;
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
