#include <iostream>
#include <cstdlib>
#include <ctime>

#define NUM_POINTS 33554432    // 1 GB of 32-bit floats

float cpu_dataset[NUM_POINTS];
float cpu2_dataset[NUM_POINTS];

__global__ void hitAtomic(float* where) {
  atomicAdd(where, 1.0);
}

__global__ void hitAtomicBy32(float* where) {
  atomicAdd(&where[threadIdx.x % 32], 1.0);
}

__global__ void hitAtomicThreadLocal(float* where) {
  atomicAdd(&where[threadIdx.x], 1.0);
}

__global__ void hitNaiveThreadLocal(float* where) {
  where[threadIdx.x] += 1.0;
}

__global__ void inplaceOperation(float* data) {
  int id = threadIdx.x + blockIdx.x * blockDim.x;
  data[id] = 1.0 - data[id];
}

__global__ void immutableOperation(float* datain, float* dataout) {
  int id = threadIdx.x + blockIdx.x * blockDim.x;
  dataout[id] = 1.0 - datain[id];
}

__global__ void constImmutableOperation(const float* datain, float* dataout) {
  int id = threadIdx.x + blockIdx.x * blockDim.x;
  dataout[id] = 1.0 - datain[id];
}

int main(int argc, char** argv) {
  srand(12345);
  for (int i = 0;  i < NUM_POINTS;  i++)
    cpu_dataset[i] = ((float)rand()) / RAND_MAX;

  struct cudaDeviceProp cdp;
  cudaGetDeviceProperties(&cdp, 0);
  std::cout << "Device at 0:" << std::endl;
  std::cout << "    name: " << cdp.name << std::endl;
  std::cout << "    totalGlobalMem: " << cdp.totalGlobalMem / 1024.0 / 1024.0 / 1024.0 << " GB" << std::endl;
  std::cout << "    sharedMemPerBlock: " << cdp.sharedMemPerBlock / 1024.0 << " kB" << std::endl;
  std::cout << "    regsPerBlock: " << cdp.regsPerBlock << std::endl;
  std::cout << "    warpSize: " << cdp.warpSize << std::endl;
  std::cout << "    memPitch: " << cdp.memPitch / 1024.0 / 1024.0 / 1024.0 << " GB" << std::endl;
  std::cout << "    maxThreadsPerBlock: " << cdp.maxThreadsPerBlock << std::endl;
  std::cout << "    maxThreadsDim: " << cdp.maxThreadsDim[0] << " " << cdp.maxThreadsDim[1] << " " << cdp.maxThreadsDim[2] << " " << std::endl;
  std::cout << "    maxGridSize: " << cdp.maxGridSize[0] << " " << cdp.maxGridSize[1] << " " << cdp.maxGridSize[2] << " " << std::endl;
  std::cout << "    totalConstMem: " << cdp.totalConstMem / 1024.0 << " kB" << std::endl;
  std::cout << "    version: " << cdp.major << "." << cdp.minor << std::endl;
  std::cout << "    clockRate: " << cdp.clockRate / 1000.0 << " MHz" << std::endl;
  std::cout << "    textureAlignment: " << cdp.textureAlignment << std::endl;
  std::cout << "    deviceOverlap: " << (cdp.deviceOverlap ? "true" : "false") << std::endl;
  std::cout << "    multiProcessorCount: " << cdp.multiProcessorCount << std::endl;
  std::cout << "    kernelExecTimeoutEnabled: " << (cdp.kernelExecTimeoutEnabled ? "true" : "false") << std::endl;
  std::cout << "    integrated: " << (cdp.integrated ? "true" : "false") << std::endl;
  std::cout << "    canMapHostMemory: " << (cdp.canMapHostMemory ? "true" : "false") << std::endl;
  std::cout << "    computeMode: " << (cdp.computeMode == cudaComputeModeDefault ? "cudaComputeModeDefault" : (cdp.computeMode == cudaComputeModeExclusive ? "cudaComputeModeExclusive" : (cdp.computeMode == cudaComputeModeProhibited ? "cudaComputeModeProhibited" : "unknown"))) << std::endl;
  std::cout << "    concurrentKernels: " << (cdp.concurrentKernels ? "true" : "false") << std::endl;
  std::cout << "    ECCEnabled: " << (cdp.ECCEnabled ? "true" : "false") << std::endl;
  std::cout << "    pciBusID: " << cdp.pciBusID << std::endl;
  std::cout << "    pciDeviceID: " << cdp.pciDeviceID << std::endl;
  std::cout << "    tccDriver: " << (cdp.tccDriver ? "true" : "false") << std::endl;
  std::cout << std::endl;

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      memcpy(cpu2_dataset, cpu_dataset, NUM_POINTS * 4);
    }
    std::cout << "1 GB host -> host: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  float* gpu_dataset;
  float* gpu2_dataset;
  cudaMalloc((void**)&gpu_dataset, NUM_POINTS * 4);
  cudaMalloc((void**)&gpu2_dataset, NUM_POINTS * 4);

  std::cout << "check " << cpu_dataset[0] << " " << cpu_dataset[1] << " " << cpu_dataset[2] << std::endl;

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      cudaMemcpy(gpu_dataset, cpu_dataset, NUM_POINTS * 4, cudaMemcpyHostToDevice);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB host -> device: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      inplaceOperation<<<NUM_POINTS / cdp.maxThreadsPerBlock, cdp.maxThreadsPerBlock>>>(gpu_dataset);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device in-place operation: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      immutableOperation<<<NUM_POINTS / cdp.maxThreadsPerBlock, cdp.maxThreadsPerBlock>>>(gpu_dataset, gpu2_dataset);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device immutable operation: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      constImmutableOperation<<<NUM_POINTS / cdp.maxThreadsPerBlock, cdp.maxThreadsPerBlock>>>(gpu_dataset, gpu2_dataset);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device const immutable operation: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      cudaMemcpy(cpu_dataset, gpu_dataset, NUM_POINTS * 4, cudaMemcpyDeviceToHost);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device -> host: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  std::cout << "check " << cpu_dataset[0] << " " << cpu_dataset[1] << " " << cpu_dataset[2] << std::endl;

  float* pinned_dataset;
  cudaMallocHost((void**)&pinned_dataset, NUM_POINTS * 4);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      memcpy(pinned_dataset, cpu_dataset, NUM_POINTS * 4);
    }
    std::cout << "1 GB host -> pinned: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  float* mapped_dataset;
  cudaHostGetDevicePointer((void**)&mapped_dataset, (void*)pinned_dataset, 0);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      inplaceOperation<<<NUM_POINTS / cdp.maxThreadsPerBlock, cdp.maxThreadsPerBlock>>>(mapped_dataset);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device in-place operation: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      immutableOperation<<<NUM_POINTS / cdp.maxThreadsPerBlock, cdp.maxThreadsPerBlock>>>(mapped_dataset, gpu2_dataset);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device immutable operation: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      constImmutableOperation<<<NUM_POINTS / cdp.maxThreadsPerBlock, cdp.maxThreadsPerBlock>>>(mapped_dataset, gpu2_dataset);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device const immutable operation: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      memcpy(cpu_dataset, pinned_dataset, NUM_POINTS * 4);
    }
    std::cout << "1 GB pinned -> host: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  std::cout << "check " << cpu_dataset[0] << " " << cpu_dataset[1] << " " << cpu_dataset[2] << std::endl;

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      cudaMemcpy(gpu2_dataset, gpu_dataset, NUM_POINTS * 4, cudaMemcpyDeviceToDevice);
      cudaDeviceSynchronize();
    }
    std::cout << "1 GB device -> device: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  const float atomic_init[32] = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
  float* global_atomics;
  cudaMalloc((void**)&global_atomics, 32 * 4);
  float cpu_atomics[32];

  cudaMemcpy(global_atomics, atomic_init, 32 * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomic<<<32768, 32>>>(global_atomics);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomics on global <<<32768, 32>>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics, global_atomics, 32 * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * 32 * 5 << ": ";
  for (int i = 0;  i < 32;  i++)
    std::cout << cpu_atomics[i] << " ";
  std::cout << std::endl;

  cudaMemcpy(global_atomics, atomic_init, 32 * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomic<<<32768, 64>>>(global_atomics);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomics on global <<<32768, 64>>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics, global_atomics, 32 * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * 64 * 5 << ": ";
  for (int i = 0;  i < 32;  i++)
    std::cout << cpu_atomics[i] << " ";
  std::cout << std::endl;

  cudaMemcpy(global_atomics, atomic_init, 32 * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomic<<<32768, cdp.maxThreadsPerBlock>>>(global_atomics);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomics on global <<<32768, " << cdp.maxThreadsPerBlock << ">>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics, global_atomics, 32 * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * cdp.maxThreadsPerBlock * 5 << ": ";
  for (int i = 0;  i < 32;  i++)
    std::cout << cpu_atomics[i] << " ";
  std::cout << std::endl;

  cudaMemcpy(global_atomics, atomic_init, 32 * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomicBy32<<<32768, 32>>>(global_atomics);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomics by 32 on global <<<32768, 32>>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics, global_atomics, 32 * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * 32 * 5 / 32 << ": ";
  for (int i = 0;  i < 32;  i++)
    std::cout << cpu_atomics[i] << " ";
  std::cout << std::endl;

  cudaMemcpy(global_atomics, atomic_init, 32 * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomicBy32<<<32768, 64>>>(global_atomics);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomics by 32 on global <<<32768, 64>>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics, global_atomics, 32 * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * 64 * 5 / 32 << ": ";
  for (int i = 0;  i < 32;  i++)
    std::cout << cpu_atomics[i] << " ";
  std::cout << std::endl;

  cudaMemcpy(global_atomics, atomic_init, 32 * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomicBy32<<<32768, cdp.maxThreadsPerBlock>>>(global_atomics);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomics by 32 on global <<<32768, " << cdp.maxThreadsPerBlock << ">>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics, global_atomics, 32 * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * cdp.maxThreadsPerBlock * 5 / 32 << ": ";
  for (int i = 0;  i < 32;  i++)
    std::cout << cpu_atomics[i] << " ";
  std::cout << std::endl;

  float* atomic_init2 = (float*)malloc(cdp.maxThreadsPerBlock * 4);
  float* global_atomics2;
  cudaMalloc((void**)&global_atomics2, cdp.maxThreadsPerBlock * 4);
  float* cpu_atomics2 = new float[cdp.maxThreadsPerBlock];

  for (int i = 0;  i < cdp.maxThreadsPerBlock;  i++)
    atomic_init2[i] = 0.0;

  cudaMemcpy(global_atomics2, atomic_init2, cdp.maxThreadsPerBlock * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitNaiveThreadLocal<<<32768, cdp.maxThreadsPerBlock>>>(global_atomics2);
      cudaDeviceSynchronize();
    }
    std::cout << "hit naive thread local by " << cdp.maxThreadsPerBlock << " on global <<<32768, " << cdp.maxThreadsPerBlock << ">>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics2, global_atomics2, cdp.maxThreadsPerBlock * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * 5 << ": ";
  for (int i = 0;  i < cdp.maxThreadsPerBlock;  i++)
    std::cout << cpu_atomics2[i] << " ";
  std::cout << std::endl;

  for (int i = 0;  i < cdp.maxThreadsPerBlock;  i++)
    atomic_init2[i] = 0.0;

  cudaMemcpy(global_atomics2, atomic_init2, cdp.maxThreadsPerBlock * 4, cudaMemcpyHostToDevice);

  for (int i = 0;  i < 5;  i++) {
    std::clock_t startTime = std::clock();
    for (int j = 0;  j < 1000;  j++) {
      hitAtomicThreadLocal<<<32768, cdp.maxThreadsPerBlock>>>(global_atomics2);
      cudaDeviceSynchronize();
    }
    std::cout << "hit atomic thread local by " << cdp.maxThreadsPerBlock << " on global <<<32768, " << cdp.maxThreadsPerBlock << ">>>: " << (std::clock() - startTime) / (double) CLOCKS_PER_SEC << " ms" << std::endl;
  }

  cudaMemcpy(cpu_atomics2, global_atomics2, cdp.maxThreadsPerBlock * 4, cudaMemcpyDeviceToHost);

  std::cout << "check for " << 32768 * 5 << ": ";
  for (int i = 0;  i < cdp.maxThreadsPerBlock;  i++)
    std::cout << cpu_atomics2[i] << " ";
  std::cout << std::endl;

  return 0;
}
