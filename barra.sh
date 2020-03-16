#!/bin/bash
#PBS -P iu60
#PBS -q normal
#PBS -l ncpus=2
#PBS -l mem=8GB
#PBS -l jobfs=1GB
#PBS -l walltime=10:10:00
#PBS -l storage=gdata/ub7+gdata/ma05
#PBS -l wd

module load python3/3.7.4

python3 transform_Barra_data.py
