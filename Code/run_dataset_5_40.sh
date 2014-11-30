#!/bin/bash

program="python "
argument=$2

for i in 5 10
do
	for j in 0 1 
	do
		eval $program" "$1" "$i" "$argument" "$j" &"
	done
done