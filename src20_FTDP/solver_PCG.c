/*
 * solver_PCG
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <math.h>
#include <omp.h>

#include "solver_PCG.h"

#define SCHEDULE_CHUNK 1024

extern int
solve_PCG (int N, int NL, int NU, int *indexL, int *itemL, int *indexU, int *itemU,
		double *D, double *B, double *X, double *AL, double *AU,
  	        double EPS, int *ITR, int *IER, int N2)
{
	double **W;
	double VAL, BNRM2, WVAL, SW, RHO, BETA, RHO1, C1, DNRM2, ALPHA, ERR;
	double Stime, Etime;
	int i, j, ic, ip, L, ip1, N3;
	int R = 0;
	int Z = 1;
	int Q = 1;
	int P = 2;
	int DD = 3;

/*********
 * INIT. *
 *********/
        N3= N;
	W = (double **)malloc(sizeof(double *)*4);
	if(W == NULL) {
		fprintf(stderr, "Error: %s\n", strerror(errno));
		return -1;
	}
	for(i=0; i<4; i++) {
  	    W[i] = (double *)malloc(sizeof(double)*N3);
		if(W[i] == NULL) {
			fprintf(stderr, "Error: %s\n", strerror(errno));
			return -1;
		}
	}

	BNRM2 = 0.0;
	*ITR = N;
	// might need to start earlier in the initialization of pointer
	#pragma omp parallel default(shared) private(i, VAL, j)
	{
	/* initializationunder this block
		#pragma omp for private (i)
			for(i=0; i<N; i++) {

			}
	*/

	// Is it sufficient to do FTDP here??
		#pragma omp for schedule(static)
		for(i=0; i<N; i++) {
			X[i] = 0.0;
			W[1][i] = 0.0;
			W[2][i] = 0.0;
			W[3][i] = 0.0;
		}

	/**************************
	 * {r0} = {b} - {A}{xini} *
	 **************************/

		#pragma omp for schedule(static)
		for(i=0; i<N; i++) {
			VAL = D[i] * X[i];
			for(j=indexL[i]; j<indexL[i+1]; j++) {
				VAL += AL[j] * X[itemL[j]-1];
			}
			for(j=indexU[i]; j<indexU[i+1]; j++) {
				VAL += AU[j] * X[itemU[j]-1];
			}
			W[R][i] = B[i] - VAL;
		}

		#pragma omp for reduction (+:BNRM2) schedule(static)
		for(i=0; i<N; i++) {
		  BNRM2 += B[i]*B[i];
		}

		#pragma omp for schedule(static)
		for(i=0; i<N; i++) {
		  W[DD][i]= 1.e0/D[i];
		}

	/************************************************************** ITERATION */
        #pragma omp single
		{
            L=0;
			Stime = omp_get_wtime();
		}
		#pragma omp barrier

		// #pragma omp single
		while(L<(*ITR)) {

	/*******************
	 * {z} = [Minv]{r} *
	 *******************/
            #pragma omp barrier
            #pragma omp for schedule(static)
            for(i=0; i<N; i++) {
                W[Z][i] = W[R][i]*W[DD][i];
            }
	/****************
	 * RHO = {r}{z} *
	 ****************/

			RHO = 0.0;

            #pragma omp barrier

			#pragma omp for reduction(+:RHO) schedule(static)
			for(i=0; i<N; i++) {
			  RHO += W[R][i] * W[Z][i];
			}

	/********************************
	 * {p}  = {z} if      ITER=0    *
	 * BETA = RHO / RHO1  otherwise *
	 ********************************/
			#pragma omp single
			{
				BETA = RHO / RHO1;
			}
            if(L==0){
    			#pragma omp for schedule(static)
    			for(i=0; i<N; i++) {
					W[P][i] = W[Z][i];
				}
            }else{
                #pragma omp for schedule(static)
                for(i=0; i<N; i++) {
					W[P][i] = W[Z][i] + BETA * W[P][i];
				}
			}
	/****************
	 * {q} = [A]{p} *
	 ****************/
			#pragma omp for schedule(static)
			for(i=0; i<N; i++) {
			  VAL = D[i] * W[P][i];
			  for(j=indexL[i]; j<indexL[i+1]; j++) {
				VAL += AL[j] * W[P][itemL[j]-1];
			  }
			  for(j=indexU[i]; j<indexU[i+1]; j++) {
				VAL += AU[j] * W[P][itemU[j]-1];
			  }
			  W[Q][i] = VAL;
			}

	/************************
	 * ALPHA = RHO / {p}{q} *
	 ************************/

			C1 = 0.0;

			#pragma omp barrier

			#pragma omp for reduction(+:C1) schedule(static)
			for(i=0; i<N; i++) {
				C1 += W[P][i] * W[Q][i];
			}
			#pragma omp single
	 		{
				ALPHA = RHO / C1;
			}
	/***************************
	 * {x} = {x} + ALPHA * {p} *
	 * {r} = {r} - ALPHA * {q} *
	 ***************************/
			#pragma omp for schedule(static)
			for(i=0; i<N; i++) {
				X[i]    += ALPHA * W[P][i];
				W[R][i] -= ALPHA * W[Q][i];
			}


			DNRM2 = 0.0;
			#pragma omp barrier
			#pragma omp for reduction(+:DNRM2) schedule(static)
			for(i=0; i<N; i++) {
			  DNRM2 += W[R][i]*W[R][i];
			}

			#pragma omp single
			{
				ERR = sqrt(DNRM2/BNRM2);
		                if( (L+1)%100 ==1) {
		                        fprintf(stdout, "%5d%16.6e\n", L+1, ERR);
		                }
				L++;
			}

			#pragma omp barrier
			if(ERR < EPS) {
				*IER = 0;
				goto N900;
			} else {
				RHO1 = RHO;
			}
		}
		#pragma omp single
		{
		*IER = 1;
		}
		N900:
		#pragma omp barrier
		#pragma omp single
		{
			Etime = omp_get_wtime();
			fprintf(stdout, "%5d%16.6e\n", L, ERR);
			fprintf(stdout, "%16.6e sec. (solver)\n", Etime - Stime);
			*ITR = L;
			free(W);
		}

	}
	return 0;

}
