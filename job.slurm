#!/bin/bash
#SBATCH -J run
#SBATCH -p first
#SBATCH -w tms05
#SBATCH -N 1 
#SBATCH -n 48
#SBATCH --ntasks-per-node=48
##SBATCH --mem=1000G
#SBATCH -o python.%j
#SBATCH -e python.%j
##SBATCH --exclusive
#SBATCH -t 2-24:00

ulimit -s unlimited


python /home/xuxh22/stu01/Bedrock/run/run.py
# python a_pre_diff.py
# python c_plot_other.py
# python c_plot_mask.py
# python /home/xuxh22/stu01/Bedrock/all/a_pre/a_pre_all_exp1.py
# python /home/xuxh22/stu01/Bedrock/all/a_pre/a_pre_all_exp1.py
# python /home/xuxh22/stu01/Bedrock/exp1/b_cal/b_cal_area_conclusion.py
# python /home/xuxh22/stu01/Bedrock/exp1/b_cal/b_cal_area.py
# python /home/xuxh22/stu01/Bedrock/exp1/c_plot/c_plot_violin.py
# python /home/xuxh22/stu01/Bedrock/exp1/c_plot/c_plot_line.py
# python /home/xuxh22/stu01/Bedrock/exp1/remap.py
# python /home/xuxh22/stu01/Bedrock/exp1/tran_tif2nc.py
# python /home/xuxh22/stu01/Bedrock/all/a_pre/a_pre_all_ctrl.py


# python /home/xuxh22/stu01/Bedrock/exp1/b_cal/b_cal_area.py
# python /home/xuxh22/stu01/Bedrock/exp1/b_cal/b_cal_area_US.py
# python /home/xuxh22/stu01/Bedrock/exp1/c_plot/c_plot_states.py
# python /home/xuxh22/stu01/Bedrock/exp1/c_plot/c_plot_violin.py
# python /home/xuxh22/stu01/Bedrock/exp1/c_plot/c_plot_US.py
# python /home/xuxh22/stu01/Bedrock/exp1/c_plot/c_plot_S_G_scatter.py

# mpirun -np 12 ESMF_RegridWeightGen -s /tera11/zhwei/students/Xionghui/data/mask1/mask1_v3/average_soil_and_sedimentary-deposit_thickness_remap_cm.nc -d /tera11/zhwei/students/Xionghui/data/mask1/mask1_v3/DTB_temp1.nc -w weights.nc -m bilinear




