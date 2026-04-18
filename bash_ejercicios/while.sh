#!/usr/bin/bash

i=1

while [[ $i -le 10 ]] ; do
	echo "Número: $i"
	(( i += 1 ))
done
