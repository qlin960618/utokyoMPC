#!/bin/sh
#PJM -N "test1"
#PJM -L rscgrp=lecture
#PJM -L node=1
#PJM --omp thread=10
#PJM -L elapse=00:15:00
#PJM -g gt69
#PJM -j
#PJM -e err
#PJM -o core10.lst

export KMP_AFFINITY=granularity=fine,balance
./sol20
./sol20
./sol20
./sol20
./sol20
