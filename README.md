# utokyoMPC
omp code for MultiThreaded Parallel Computing


### 1. src20
This contain the original program code from the class with no modification except for single line in line 45 where ```schedule(dynamic)``` is added to force random placement of data across the two NUMA domains.
```c
#pragma omp parallel for private (i) schedule(dynamic)
for(i=0; i<N; i++) {
    X[i] = 0.0;
    W[1][i] = 0.0;
    W[2][i] = 0.0;
    W[3][i] = 0.0;
}
```
### 2. run
This is the runtime folder for the ```src20``` program

### 3. src20_FTDP
This contain the First Touch Data Placement optimized program. the content is nearly same of that in the ```src20``` with exception to the ```solver_PCG.c``` and ``` Makefile``` files. All modification to achieve FTDP optimization is made in the given solver_PCG class file.

### 4. run_FTDP
This is the runtime folder for the ```src20_FTDP``` program

### 5. Python
This folder contain the helper python script for:

- ```generate_go_sh.py```: helper script to generate all go file for different core and affinity configuration
- ```process.py```: helper script to read output of the run and store in csv file
