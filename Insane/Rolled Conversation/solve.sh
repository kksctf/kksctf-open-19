#!/usr/bin/env bash

for i in `ls ./conversation/word*`; # Decode all words
do 
    ./solve.py $i; 
done