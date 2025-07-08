#!/bin/bash
#SBATCH -J job3
#SBATCH -p second
##SBATCH -w tms04
#SBATCH -N 1 
#SBATCH -n 48
#SBATCH --ntasks-per-node=48
##SBATCH --mem=1000G
#SBATCH -o job3.%J
#SBATCH -e job3.%J
##SBATCH --exclusive
#SBATCH -t 2-24:00

ulimit -s unlimited

# python main/cmp_class.py
python main/cmp_G.py