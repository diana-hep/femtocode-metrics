#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <sys/time.h>
#include <vector>

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

  double* pt = new double[MUONS];
  int* size = new int[EVENTS];

  std::ifstream ptfile("muptfile.txt");
  for (int i = 0;  i < MUONS;  i++) {
    ptfile >> pt[i];
  }

  int outsize = 0;
  std::ifstream sizefile("musizefile.txt");
  for (int i = 0;  i < EVENTS;  i++) {
    sizefile >> size[i];
    outsize += size[i] * size[i];
  }

  std::cout << "ready" << std::endl;

  double* output = new double[outsize];

  int pti = 0;
  int outi = 0;

  gettimeofday(&startTime, 0);
  for (int i = 0;  i < EVENTS;  i++) {
    // for (int one = 0;  one < size[i];  ++one) {
    //   for (int two = 0;  two < size[i];  ++two) {
    //     output[outi] = pt[one] + pt[two];
    //     outi++;
    //   }
    // }

    std::vector<Muon*> muons;
    for (int j = 0;  j < size[i];  j++) {
      muons.push_back(new Muon(pt[pti]));
      pti++;
    }

    for (std::vector<Muon*>::const_iterator one = muons.begin();  one != muons.end();  ++one) {
      for (std::vector<Muon*>::const_iterator two = muons.begin();  two != muons.end();  ++two) {
        output[outi] = (*one)->pt + (*two)->pt;
        outi++;
      }
    }

    // for (std::vector<Muon*>::const_iterator one = muons.begin();  one != muons.end();  ++one) {
    //   output[outi] = (*one)->pt * 2;
    //   outi++;
    // }

    for (std::vector<Muon*>::const_iterator one = muons.begin();  one != muons.end();  ++one) {
      delete (*one);
    }
  }
  gettimeofday(&endTime, 0);

  std::cout << "TIME: " << diff(endTime, startTime) << " sec" << std::endl;

  return 0;
}
