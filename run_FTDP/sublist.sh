#!/bin/bash


JOB_KEY="gt69"

for i in go_*.sh; do
	echo $i

	pjsub $i

	while [[ $(pjstat | grep $JOB_KEY) ]]; do
		sleep 1
		echo "waiting for $i"
	done

done
