#!/bin/sh

echo time python read_mmap.py
ulimit -Sv 1048576
time python read_mmap.py

echo time python read_plain.py
ulimit -Sv 1048576
time python read_plain.py

echo time ./readfile
ulimit -Sv 1048576
time ./readfile

echo time python read_mmap.py
ulimit -Sv 1048576
time python read_mmap.py

echo time python read_plain.py
ulimit -Sv 1048576
time python read_plain.py

echo time ./readfile
ulimit -Sv 1048576
time ./readfile

echo time python read_mmap.py
ulimit -Sv 1048576
time python read_mmap.py

echo time python read_plain.py
ulimit -Sv 1048576
time python read_plain.py

echo time ./readfile
ulimit -Sv 1048576
time ./readfile
