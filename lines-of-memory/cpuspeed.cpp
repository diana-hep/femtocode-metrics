#include <iostream>
#include <string>
#include <ctime>
#include <sys/time.h>
// #include <numa.h>
#include <memkind.h>

// #define ITEMS 1000000
#define ITEMS 100000

double diff(struct timeval endTime, struct timeval startTime) {
  return (1000L * 1000L * (endTime.tv_sec - startTime.tv_sec) + (endTime.tv_usec - startTime.tv_usec)) / 1000.0 / 1000.0;
}

double read1(double* x1) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i];
  return out;
}

double read2(double* x1, double* x2) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i] + x2[i];
  return out;
}

double read4(double* x1, double* x2, double* x3, double* x4) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i] + x2[i] + x3[i] + x4[i];
  return out;
}

double read8(double* x1, double* x2, double* x3, double* x4, double* x5, double* x6, double* x7, double* x8) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i] + x2[i] + x3[i] + x4[i] + x5[i] + x6[i] + x7[i] + x8[i];
  return out;
}

double read16(double* x1, double* x2, double* x3, double* x4, double* x5, double* x6, double* x7, double* x8, double* x9, double* x10, double* x11, double* x12, double* x13, double* x14, double* x15, double* x16) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i] + x2[i] + x3[i] + x4[i] + x5[i] + x6[i] + x7[i] + x8[i] + x9[i] + x10[i] + x11[i] + x12[i] + x13[i] + x14[i] + x15[i] + x16[i];
  return out;
}

double read32(double* x1, double* x2, double* x3, double* x4, double* x5, double* x6, double* x7, double* x8, double* x9, double* x10, double* x11, double* x12, double* x13, double* x14, double* x15, double* x16, double* x17, double* x18, double* x19, double* x20, double* x21, double* x22, double* x23, double* x24, double* x25, double* x26, double* x27, double* x28, double* x29, double* x30, double* x31, double* x32) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i] + x2[i] + x3[i] + x4[i] + x5[i] + x6[i] + x7[i] + x8[i] + x9[i] + x10[i] + x11[i] + x12[i] + x13[i] + x14[i] + x15[i] + x16[i] + x17[i] + x18[i] + x19[i] + x20[i] + x21[i] + x22[i] + x23[i] + x24[i] + x25[i] + x26[i] + x27[i] + x28[i] + x29[i] + x30[i] + x31[i] + x32[i];
  return out;
}

double read64(double* x1, double* x2, double* x3, double* x4, double* x5, double* x6, double* x7, double* x8, double* x9, double* x10, double* x11, double* x12, double* x13, double* x14, double* x15, double* x16, double* x17, double* x18, double* x19, double* x20, double* x21, double* x22, double* x23, double* x24, double* x25, double* x26, double* x27, double* x28, double* x29, double* x30, double* x31, double* x32, double* x33, double* x34, double* x35, double* x36, double* x37, double* x38, double* x39, double* x40, double* x41, double* x42, double* x43, double* x44, double* x45, double* x46, double* x47, double* x48, double* x49, double* x50, double* x51, double* x52, double* x53, double* x54, double* x55, double* x56, double* x57, double* x58, double* x59, double* x60, double* x61, double* x62, double* x63, double* x64) {
  double out = 0.0;
  for (int i = 0;  i < ITEMS;  i++)
    out += x1[i] + x2[i] + x3[i] + x4[i] + x5[i] + x6[i] + x7[i] + x8[i] + x9[i] + x10[i] + x11[i] + x12[i] + x13[i] + x14[i] + x15[i] + x16[i] + x17[i] + x18[i] + x19[i] + x20[i] + x21[i] + x22[i] + x23[i] + x24[i] + x25[i] + x26[i] + x27[i] + x28[i] + x29[i] + x30[i] + x31[i] + x32[i] + x33[i] + x34[i] + x35[i] + x36[i] + x37[i] + x38[i] + x39[i] + x40[i] + x41[i] + x42[i] + x43[i] + x44[i] + x45[i] + x46[i] + x47[i] + x48[i] + x49[i] + x50[i] + x51[i] + x52[i] + x53[i] + x54[i] + x55[i] + x56[i] + x57[i] + x58[i] + x59[i] + x60[i] + x61[i] + x62[i] + x63[i] + x64[i];
  return out;
}

int main(int argc, char** argv) {
  struct timeval startTime, endTime;

  // double* x1 = new double[ITEMS];
  // double* x2 = new double[ITEMS];
  // double* x3 = new double[ITEMS];
  // double* x4 = new double[ITEMS];
  // double* x5 = new double[ITEMS];
  // double* x6 = new double[ITEMS];
  // double* x7 = new double[ITEMS];
  // double* x8 = new double[ITEMS];
  // double* x9 = new double[ITEMS];
  // double* x10 = new double[ITEMS];
  // double* x11 = new double[ITEMS];
  // double* x12 = new double[ITEMS];
  // double* x13 = new double[ITEMS];
  // double* x14 = new double[ITEMS];
  // double* x15 = new double[ITEMS];
  // double* x16 = new double[ITEMS];
  // double* x17 = new double[ITEMS];
  // double* x18 = new double[ITEMS];
  // double* x19 = new double[ITEMS];
  // double* x20 = new double[ITEMS];
  // double* x21 = new double[ITEMS];
  // double* x22 = new double[ITEMS];
  // double* x23 = new double[ITEMS];
  // double* x24 = new double[ITEMS];
  // double* x25 = new double[ITEMS];
  // double* x26 = new double[ITEMS];
  // double* x27 = new double[ITEMS];
  // double* x28 = new double[ITEMS];
  // double* x29 = new double[ITEMS];
  // double* x30 = new double[ITEMS];
  // double* x31 = new double[ITEMS];
  // double* x32 = new double[ITEMS];
  // double* x33 = new double[ITEMS];
  // double* x34 = new double[ITEMS];
  // double* x35 = new double[ITEMS];
  // double* x36 = new double[ITEMS];
  // double* x37 = new double[ITEMS];
  // double* x38 = new double[ITEMS];
  // double* x39 = new double[ITEMS];
  // double* x40 = new double[ITEMS];
  // double* x41 = new double[ITEMS];
  // double* x42 = new double[ITEMS];
  // double* x43 = new double[ITEMS];
  // double* x44 = new double[ITEMS];
  // double* x45 = new double[ITEMS];
  // double* x46 = new double[ITEMS];
  // double* x47 = new double[ITEMS];
  // double* x48 = new double[ITEMS];
  // double* x49 = new double[ITEMS];
  // double* x50 = new double[ITEMS];
  // double* x51 = new double[ITEMS];
  // double* x52 = new double[ITEMS];
  // double* x53 = new double[ITEMS];
  // double* x54 = new double[ITEMS];
  // double* x55 = new double[ITEMS];
  // double* x56 = new double[ITEMS];
  // double* x57 = new double[ITEMS];
  // double* x58 = new double[ITEMS];
  // double* x59 = new double[ITEMS];
  // double* x60 = new double[ITEMS];
  // double* x61 = new double[ITEMS];
  // double* x62 = new double[ITEMS];
  // double* x63 = new double[ITEMS];
  // double* x64 = new double[ITEMS];

  double* x1 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x2 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x3 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x4 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x5 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x6 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x7 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x8 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x9 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x10 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x11 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x12 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x13 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x14 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x15 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x16 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x17 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x18 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x19 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x20 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x21 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x22 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x23 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x24 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x25 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x26 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x27 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x28 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x29 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x30 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x31 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x32 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x33 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x34 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x35 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x36 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x37 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x38 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x39 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x40 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x41 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x42 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x43 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x44 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x45 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x46 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x47 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x48 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x49 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x50 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x51 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x52 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x53 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x54 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x55 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x56 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x57 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x58 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x59 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x60 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x61 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x62 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x63 = (double*)hbw_alloc(ITEMS * sizeof(double));
  double* x64 = (double*)hbw_alloc(ITEMS * sizeof(double));

  std::cout << hbw_verify_memory_region(x1, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x2, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x3, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x4, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x5, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x6, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x7, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x8, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x9, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x10, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x11, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x12, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x13, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x14, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x15, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x16, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x17, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x18, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x19, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x20, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x21, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x22, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x23, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x24, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x25, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x26, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x27, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x28, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x29, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x30, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x31, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x32, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x33, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x34, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x35, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x36, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x37, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x38, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x39, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x40, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x41, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x42, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x43, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x44, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x45, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x46, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x47, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x48, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x49, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x50, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x51, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x52, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x53, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x54, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x55, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x56, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x57, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x58, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x59, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x60, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x61, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x62, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x63, ITEMS * sizeof(double), 0) << " "
            << hbw_verify_memory_region(x64, ITEMS * sizeof(double), 0) << std::endl

  for (int i = 0;  i < ITEMS;  i++) {
    x1[i] = 0.01;
    x2[i] = 0.02;
    x3[i] = 0.03;
    x4[i] = 0.04;
    x5[i] = 0.05;
    x6[i] = 0.06;
    x7[i] = 0.07;
    x8[i] = 0.08;
    x9[i] = 0.09;
    x10[i] = 0.10;
    x11[i] = 0.11;
    x12[i] = 0.12;
    x13[i] = 0.13;
    x14[i] = 0.14;
    x15[i] = 0.15;
    x16[i] = 0.16;
    x17[i] = 0.17;
    x18[i] = 0.18;
    x19[i] = 0.19;
    x20[i] = 0.20;
    x21[i] = 0.21;
    x22[i] = 0.22;
    x23[i] = 0.23;
    x24[i] = 0.24;
    x25[i] = 0.25;
    x26[i] = 0.26;
    x27[i] = 0.27;
    x28[i] = 0.28;
    x29[i] = 0.29;
    x30[i] = 0.30;
    x31[i] = 0.31;
    x32[i] = 0.32;
    x33[i] = 0.33;
    x34[i] = 0.34;
    x35[i] = 0.35;
    x36[i] = 0.36;
    x37[i] = 0.37;
    x38[i] = 0.38;
    x39[i] = 0.39;
    x40[i] = 0.40;
    x41[i] = 0.41;
    x42[i] = 0.42;
    x43[i] = 0.43;
    x44[i] = 0.44;
    x45[i] = 0.45;
    x46[i] = 0.46;
    x47[i] = 0.47;
    x48[i] = 0.48;
    x49[i] = 0.49;
    x50[i] = 0.50;
    x51[i] = 0.51;
    x52[i] = 0.52;
    x53[i] = 0.53;
    x54[i] = 0.54;
    x55[i] = 0.55;
    x56[i] = 0.56;
    x57[i] = 0.57;
    x58[i] = 0.58;
    x59[i] = 0.59;
    x60[i] = 0.60;
    x61[i] = 0.61;
    x62[i] = 0.62;
    x63[i] = 0.63;
    x64[i] = 0.64;
  }

  double result;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read1(x1) + read1(x2) + read1(x3) + read1(x4) + read1(x5) + read1(x6) + read1(x7) + read1(x8) + read1(x9) + read1(x10) + read1(x11) + read1(x12) + read1(x13) + read1(x14) + read1(x15) + read1(x16) + read1(x17) + read1(x18) + read1(x19) + read1(x20) + read1(x21) + read1(x22) + read1(x23) + read1(x24) + read1(x25) + read1(x26) + read1(x27) + read1(x28) + read1(x29) + read1(x30) + read1(x31) + read1(x32) + read1(x33) + read1(x34) + read1(x35) + read1(x36) + read1(x37) + read1(x38) + read1(x39) + read1(x40) + read1(x41) + read1(x42) + read1(x43) + read1(x44) + read1(x45) + read1(x46) + read1(x47) + read1(x48) + read1(x49) + read1(x50) + read1(x51) + read1(x52) + read1(x53) + read1(x54) + read1(x55) + read1(x56) + read1(x57) + read1(x58) + read1(x59) + read1(x60) + read1(x61) + read1(x62) + read1(x63) + read1(x64);
    gettimeofday(&endTime, 0);
    std::cout << "read1 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read2(x1, x2) + read2(x3, x4) + read2(x5, x6) + read2(x7, x8) + read2(x9, x10) + read2(x11, x12) + read2(x13, x14) + read2(x15, x16) + read2(x17, x18) + read2(x19, x20) + read2(x21, x22) + read2(x23, x24) + read2(x25, x26) + read2(x27, x28) + read2(x29, x30) + read2(x31, x32) + read2(x33, x34) + read2(x35, x36) + read2(x37, x38) + read2(x39, x40) + read2(x41, x42) + read2(x43, x44) + read2(x45, x46) + read2(x47, x48) + read2(x49, x50) + read2(x51, x52) + read2(x53, x54) + read2(x55, x56) + read2(x57, x58) + read2(x59, x60) + read2(x61, x62) + read2(x63, x64);
    gettimeofday(&endTime, 0);
    std::cout << "read2 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read4(x1, x2, x3, x4) + read4(x5, x6, x7, x8) + read4(x9, x10, x11, x12) + read4(x13, x14, x15, x16) + read4(x17, x18, x19, x20) + read4(x21, x22, x23, x24) + read4(x25, x26, x27, x28) + read4(x29, x30, x31, x32) + read4(x33, x34, x35, x36) + read4(x37, x38, x39, x40) + read4(x41, x42, x43, x44) + read4(x45, x46, x47, x48) + read4(x49, x50, x51, x52) + read4(x53, x54, x55, x56) + read4(x57, x58, x59, x60) + read4(x61, x62, x63, x64);
    gettimeofday(&endTime, 0);
    std::cout << "read4 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read8(x1, x2, x3, x4, x5, x6, x7, x8) + read8(x9, x10, x11, x12, x13, x14, x15, x16) + read8(x17, x18, x19, x20, x21, x22, x23, x24) + read8(x25, x26, x27, x28, x29, x30, x31, x32) + read8(x33, x34, x35, x36, x37, x38, x39, x40) + read8(x41, x42, x43, x44, x45, x46, x47, x48) + read8(x49, x50, x51, x52, x53, x54, x55, x56) + read8(x57, x58, x59, x60, x61, x62, x63, x64);
    gettimeofday(&endTime, 0);
    std::cout << "read8 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read16(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16) + read16(x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32) + read16(x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48) + read16(x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64);
    gettimeofday(&endTime, 0);
    std::cout << "read16 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read32(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32) + read32(x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64);
    gettimeofday(&endTime, 0);
    std::cout << "read32 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    gettimeofday(&startTime, 0);
    result = read64(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64);
    gettimeofday(&endTime, 0);
    std::cout << "read64 result " << result << " in " << diff(endTime, startTime) << " sec" << std::endl;
  }
  std::cout << std::endl;

  return 0;
}
