#!/bin/bash
#SBATCH -J dp_D
#SBATCH -p first
#SBATCH -w tms08
#SBATCH -N 1 
#SBATCH -n 48
#SBATCH --ntasks-per-node=48
##SBATCH --mem=1000G
#SBATCH -o dp_D-o.out
#SBATCH -e dp_D-e.out
##SBATCH --exclusive
#SBATCH -t 2-24:00

ulimit -s unlimited

python main/dp_D.py