#!/bin/bash
#SBATCH -J dp_D
#SBATCH -p second
#SBATCH -w tms13
#SBATCH -N 1 
#SBATCH -n 48
#SBATCH --ntasks-per-node=48
##SBATCH --mem=1000G
#SBATCH -o dp_D-o.out
#SBATCH -e dp_D-e.out
##SBATCH --exclusive
#SBATCH -t 2-24:00

ulimit -s unlimited

# python main/dp_D.py
# python main_cases/cal_cases.py
python main_cases/dp_cases.py

# python draw_cases/draw_g2_scatter_cases.py
# python draw_cases/draw_g2_scatter_cases_diff.py