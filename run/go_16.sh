#!/bin/sh
#PJM -N "test1"
#PJM -L rscgrp=lecture
#PJM -L node=1
#PJM --omp thread=32
#PJM -L elapse=00:15:00
#PJM -g gt69
#PJM -j
#PJM -e err
#PJM -o core32.lst

export KMP_AFFINITY=granularity=fine,balanced
./sol20
./sol20
./sol20
./sol20
./sol20
