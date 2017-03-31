#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>

// #define NUM_POINTS 33554432  //    1 GB of 32-bit floats

#define NUM_POINTS 10000000

int main(int argc, char** argv) {
  double* olddata = new double[NUM_POINTS];
  double* newdata = new double[NUM_POINTS];

  for (int i = 0;  i < NUM_POINTS;  i++)
    olddata[i] = i;

  for (int j = 0;  j < 5;  j++) {
    std::clock_t startTime = std::clock();
    for (int i = 0;  i < NUM_POINTS;  i++)
      newdata[i] = 1.0 - olddata[i];
    std::cout << "immutable " << 1e3 * (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int j = 0;  j < 5;  j++) {
    std::clock_t startTime = std::clock();
    for (int i = 0;  i < NUM_POINTS;  i++)
      olddata[i] = 1.0 - olddata[i];
    std::cout << "mutable " << 1e3 * (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  return 0;
}

// int main(int argc, char** argv) {
//   std::vector<float*> olddatas;
//   std::vector<float*> newdatas;

//   int numBlocks = 0;
//   for (int block = 0;  block < NUM_POINTS;  block += 1024*1024) {
//     float* olddata = new float[1024*1024];
//     float* newdata = new float[1024*1024];

//     for (int j = 0;  j < 1024*1024;  j++)
//       olddata[j] = j;

//     olddatas.push_back(olddata);
//     newdatas.push_back(newdata);
//     numBlocks++;
//   }

//   for (int j = 0;  j < 5;  j++) {
//     std::clock_t startTime = std::clock();
//     for (int block = 0;  block < numBlocks;  block++) {
//       float* olddata = olddatas[block];
//       float* newdata = newdatas[block];

//       for (int i = 0;  i < 1024*1024;  i++)
//         newdata[i] = 1.0 - olddata[i];
//     }
//     std::cout << "immutable " << 1e3 * (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
//   }

//   for (int j = 0;  j < 5;  j++) {
//     std::clock_t startTime = std::clock();
//     for (int block = 0;  block < numBlocks;  block++) {
//       float* olddata = olddatas[block];

//       for (int i = 0;  i < 1024*1024;  i++)
//         olddata[i] = 1.0 - olddata[i];
//     }
//     std::cout << "mutable " << 1e3 * (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
//   }

//   return 0;
// }
