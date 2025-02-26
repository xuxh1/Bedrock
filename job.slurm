#!/bin/bash
#SBATCH -J dp_S
#SBATCH -p second
#SBATCH -w tms13
#SBATCH -N 1 
#SBATCH -n 48
#SBATCH --ntasks-per-node=48
##SBATCH --mem=1000G
#SBATCH -o dp_S-o.out
#SBATCH -e dp_S-e.out
#SBATCH --exclusive
#SBATCH -t 2-24:00

ulimit -s unlimited

python main/dp_S.py
# python main/dp_index.py
# python run/run.py
