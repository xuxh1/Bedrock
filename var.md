# cal_S_exp1.py:
Sr_temp1: Sr method exp1
Sr_temp1_test: Sr method original
Deficit_S: accumulate difference(ET-P)
nmax: accumulate the maximum points(0-?)
nmin: accumulate the minimum points(0-?)
Deficit_pmax: the latest time-varying maximum
Deficit_pmin: the latest time-varying minimum
Deficit_diff: time-varying diff
Deficit_Srv1: time-varying max diff

Sr: remapbil and mask
Sbedrock: Sr - Ssoil
Proportion1: Sbedrock/Sr
Proportion2: Sbedrock/ET
Proportion3: Q/PR
LH: from Sbedrock to calculate Latent Heat Flux (Ee=Sr*1000*2257/(3600*24*365)) (W/m2)
(the time have problem, try to calculate monthly)

add:
FD_temp1: First Day use bedrock water

# cal_D_exp1.py:
Dr_Y_temp1: Dr method exp1
FD_Y_temp1: First Day use bedrock water in Y year
nmax_Y: accumulate the maximum points(0-?) in Y year
nmin_Y: accumulate the minimum points(0-?) in Y year
Deficit_D: accumulate difference in Y year(ET-P)
Dbedrcok_Frequency: accumulate the frequency use Dbedrock

FD_mean_temp1: Ensemble mean the First Day
FD_mean_temp2: Remapbil
FD_mean: Mask

# count_data.py:
count_G: area, IGBP, Koppen, DTB, ET, PR, Q, LH, FD_mean, Aboveground, Belowground, Sbedrock, Sr&
Ssoil, Proportion1, Proportion2, Proportion3, mask123, Continent, Subregion, Sovereignt
Global.csv
US.csv

count_G_Db: Dbedrock_Y
Global_Db.csv

count_US: US plus state
US.csv

count_site: collect field site data from global data
Measure(Root or ET), lat, lon, Sbedrock_field min max, Sbedrock, Ssoil, Soil depth, DTB, mask1, 2, 3, mask123
site.csv

count_fDTB: collect the field DTB in US(lat from 24.4 to 49.4, lon from -125 to -66.9)
field, gNATSGO, SsoilGrids250m, SoilGrids250m_rev, Pelletier
DTB.csv

count_fSb: collect the field Sbedrock in CA and TX
field_min, field_max, Ssoil, Sbedrock
Sbedrock.csv