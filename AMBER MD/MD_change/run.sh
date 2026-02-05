#!/usr/bin/env bash
sander -O -i min.in -o min.out -p count16_amber.parm7 -c count16_amber.rst7 -r min.rst7
sander -O -i production.in -o md.out -p count16_amber.parm7 -c min.rst7 -r md.rst7 -x md.nc
