def PET_div_PR_mean():
    # Calculate PET/PR_mean
    subprocess.run(f"cdo -mulc,100 -div PET.nc4 PR_mean.nc P/PET_div_PR_mean_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/PET_div_PR_mean_tmp1.nc4 mask123.nc P/PET_div_PR_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/PET_div_PR_mean_tmp2.nc4 P/PET_div_PR_mean.nc4", shell=True, check=True)
    print(f'The PET/PR_mean has finished') 
