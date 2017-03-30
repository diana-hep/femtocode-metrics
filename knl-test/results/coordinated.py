import ctypes
import multiprocessing
import sys
import time

import numpy
import psutil

REPS = 1000
SIZE = 600 * 1024

def hbw_malloc(size):
    libmemkind = ctypes.cdll.LoadLibrary("libmemkind.so")

    libmemkind.hbw_malloc.restype = ctypes.POINTER(ctypes.c_uint8)
    ptr = libmemkind.hbw_malloc(ctypes.c_size_t(size))

    assert libmemkind.hbw_verify_memory_region(ptr, ctypes.c_size_t(size), ctypes.c_int(0)) == 0
    return ptr

def numa_alloc_local(size):
    libnuma = ctypes.cdll.LoadLibrary("libnuma.so")
    assert libnuma.numa_available() == 0   # NUMA not available is -1

    libnuma.numa_alloc_local.restype = ctypes.POINTER(ctypes.c_uint8)
    return libnuma.numa_alloc_local(ctypes.c_size_t(size))

def numa_alloc_onnode(size, node):
    libnuma = ctypes.cdll.LoadLibrary("libnuma.so")
    assert libnuma.numa_available() == 0   # NUMA not available is -1

    libnuma.numa_alloc_onnode.restype = ctypes.POINTER(ctypes.c_uint8)
    return libnuma.numa_alloc_onnode(ctypes.c_size_t(size), ctypes.c_int(node))
    
def custom_allocator_array(allocator, size):
    ptr = allocator(size)
    ptr.__array_interface__ = {"version": 3,
                               "typestr": numpy.ctypeslib._dtype(type(ptr.contents)).str,
                               "data": (ctypes.addressof(ptr.contents), False),
                               "shape": (size,)}
    return numpy.array(ptr, copy=False)

class MemoryIntensiveWork(multiprocessing.Process):
    def __init__(self, allocator, index, ready, go, starts, ends, times):
        super(MemoryIntensiveWork, self).__init__()
        self.allocator = allocator
        self.index = index
        self.ready = ready
        self.go = go
        self.starts = starts
        self.ends = ends
        self.times = times

    def run(self):
        if self.allocator == "hbw_malloc":
            one = custom_allocator_array(hbw_malloc, SIZE).view(numpy.float64)
            two = custom_allocator_array(hbw_malloc, SIZE).view(numpy.float64)
            three = custom_allocator_array(hbw_malloc, SIZE).view(numpy.float64)

        elif self.allocator == "numa0":
            one = custom_allocator_array(lambda size: numa_alloc_onnode(size, 0), SIZE).view(numpy.float64)
            two = custom_allocator_array(lambda size: numa_alloc_onnode(size, 0), SIZE).view(numpy.float64)
            three = custom_allocator_array(lambda size: numa_alloc_onnode(size, 0), SIZE).view(numpy.float64)

        elif self.allocator == "numa1":
            one = custom_allocator_array(lambda size: numa_alloc_onnode(size, 1), SIZE).view(numpy.float64)
            two = custom_allocator_array(lambda size: numa_alloc_onnode(size, 1), SIZE).view(numpy.float64)
            three = custom_allocator_array(lambda size: numa_alloc_onnode(size, 1), SIZE).view(numpy.float64)

        elif self.allocator == "numa_alloc_local":
            one = custom_allocator_array(numa_alloc_local, SIZE).view(numpy.float64)
            two = custom_allocator_array(numa_alloc_local, SIZE).view(numpy.float64)
            three = custom_allocator_array(numa_alloc_local, SIZE).view(numpy.float64)

        elif self.allocator == "malloc":
            one = numpy.empty(SIZE, dtype=numpy.uint8).view(numpy.float64)
            two = numpy.empty(SIZE, dtype=numpy.uint8).view(numpy.float64)
            three = numpy.empty(SIZE, dtype=numpy.uint8).view(numpy.float64)

        else:
            assert False

        one[:] = 1.1
        two[:] = 2.2

        self.ready.put(self.index)       # do not start until everybody has allocated
        time.sleep(1)

        self.go.wait()                   # everybody must start at the same time

        startTime = time.time()
        for i in range(REPS):
            three = one + two
        endTime = time.time()

        time.sleep(5)                   # make sure everybody's done before communicating
        self.starts.put(startTime)
        self.ends.put(endTime)
        self.times.put(endTime - startTime)

allocator = sys.argv[1]
numProcesses = int(sys.argv[2])

ready = multiprocessing.Queue()
go = multiprocessing.Event()
starts = multiprocessing.Queue()
ends = multiprocessing.Queue()
times = multiprocessing.Queue()

processes = [MemoryIntensiveWork(allocator, index, ready, go, starts, ends, times) for index in range(numProcesses)]

pinnings = numpy.random.permutation(range(256))[:numProcesses]

for i, p in zip(pinnings, processes):
    p.start()
    psutil.Process(p.pid).cpu_affinity([i])

readys = []
for i in range(numProcesses):
    readys.append(ready.get())
    # print("{} is ready".format(readys[-1]))

print("all are ready with {} reps of {} MB".format(REPS, SIZE / 1024**2))
assert sorted(readys) == sorted(range(numProcesses))

time.sleep(2)
go.set()                  # starter gun

startTimes = [starts.get() for i in range(numProcesses)]
endTimes = [ends.get() for i in range(numProcesses)]
totalTimes = [times.get() for i in range(numProcesses)]

firstStart = min(startTimes)
lastEnd = max(endTimes)

print("starts {}".format(" ".join("{:.2f}".format(x - firstStart) for x in sorted(startTimes))))
print("ends   {}".format(" ".join("{:.2f}".format(lastEnd - x) for x in sorted(endTimes))))
print("times  {}".format(" ".join("{:.2f}".format(x) for x in sorted(totalTimes))))

total_time = lastEnd - firstStart

num_operations = REPS * SIZE // 8 * numProcesses

print("{} {} processes, total of {} operations in {} sec = {} MHz".format(numProcesses, allocator, num_operations, total_time, 1e-6 * num_operations / total_time))
