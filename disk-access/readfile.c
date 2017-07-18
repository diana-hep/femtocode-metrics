#include <unistd.h>
#include <stdio.h>
#include <inttypes.h>

#define CHUNK 8192L

int main(int argc, char** argv) {
  double out = 0.0;
  double buffer[CHUNK];

  FILE *f = fopen("/mnt/sdb-instancestore/big-file.raw", "r");
  int fd = fileno(f);

  uint64_t i;
  uint64_t j;
  for (i = 0;  i < 40L*1024L*1024L*1024L/8L/CHUNK;  i++) {   // 34359738368/CHUNK
    read(fd, buffer, 8*CHUNK);
    for (j = 0;  j < CHUNK;  j++)
      out += buffer[j];
  }

  fclose(f);
  printf("out: %g\n", out);

  return 0;
}

// 40 GB /mnt/sdb-instancestore/big-file.raw  95

// 1 GB /mnt/sdb-instancestore/big-file.raw    2.46
// 1 GB /mnt/sdc-gp2/big-file.raw             13.46
// 1 GB /mnt/sdd-io1/big-file.raw             13.46
// 1 GB /mnt/sde-sc1/big-file.raw             23.72
// 1 GB /mnt/sdf-st1/big-file.raw             14.50
// 1 GB /mnt/sdg-standard/big-file.raw        14.17
