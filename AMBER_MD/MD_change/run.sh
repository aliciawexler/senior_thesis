#!/usr/bin/env bash
sander -O -i <name of your minimization file>.in -o min.out -p sequence_<sequence_number>_amber.parm7 -c sequence_<sequence_number>_amber.rst7 -r min.rst7
sander -O -i <name of your production file>.in -o md.out -p sequence_<sequence_number>_amber.parm7 -c min.rst7 -r md.rst7 -x md.nc