#!/bin/sh
#PJM -N "test1"
#PJM -L rscgrp=lecture9
#PJM -L node=1
#PJM --omp thread=28
#PJM -L elapse=00:15:00
#PJM -g gt69
#PJM -j
#PJM -e err
#PJM -o t20.lst

export KMP_AFFINITY=granularity=fine,compact
./sol20
./sol20
./sol20
./sol20
./sol20
