#include <iostream>
#include <string>
#include <ctime>
#include <sys/time.h>

#define EVENTS 48131
#define MUONS 132274

double diff(struct timeval endTime, struct timeval startTime) {
  return (1000L * 1000L * (endTime.tv_sec - startTime.tv_sec) + (endTime.tv_usec - startTime.tv_usec)) / 1000.0 / 1000.0;
}

class Muon {
public:
  double pt;
  Muon(double pt) : pt(pt) { }
};

int main(int argc, char** argv) {
  struct timeval startTime, endTime;

  int total = 0;
  int* size = new int[EVENTS];
  for (int i = 0;  i < EVENTS;  i++) {
    if (i % 4 == 0)
      size[i] = 2;
    else
      size[i] = 3;
    total += size[i];
    while (total > MUONS) {
      size[i]--;
      total--;
    }
    std::cout << size[i] << std::endl;
  }

  double* pt = new double[MUONS];
  for (int i = 0;  i < MUONS;  i++)
    pt[i] = i * 1.1;

  double idiotproof = 0.0;

  // gettimeofday(&startTime, 0);
  // for (int i = 0;  i < ITEMS;  i++) {
    


  // }
  // gettimeofday(&endTime, 0);

  // std::cout << diff(endTime, startTime) << " sec" << std::endl;

  return 0;
}
