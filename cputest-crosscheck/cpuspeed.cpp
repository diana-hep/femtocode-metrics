#include <iostream>
#include <string>
#include <ctime>
#include <sys/time.h>

#define ITEMS 1000000

double diff(struct timeval endTime, struct timeval startTime) {
  return (1000L * 1000L * (endTime.tv_sec - startTime.tv_sec) + (endTime.tv_usec - startTime.tv_usec)) / 1000.0 / 1000.0;
}

int main(int argc, char** argv) {
  struct timeval startTime, endTime;

  double* one = new double[ITEMS];
  double* two = new double[ITEMS];
  double* three = new double[ITEMS];
  for (int i = 0;  i < ITEMS;  i++) {
    one[i] = 1.1;
    two[i] = 2.2;
    three[i] = 0.0;
  }

  gettimeofday(&startTime, 0);
  for (int i = 0;  i < ITEMS;  i++)
    three[i] = one[i] + two[i];
  gettimeofday(&endTime, 0);

  std::cout << diff(endTime, startTime) << " sec" << std::endl;

  return 0;
}
