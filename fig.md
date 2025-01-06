# Draw Code and Fig Introduction

This project generates global distribution maps and plots for various environmental parameters.

## Code Overview

The following Python scripts are used:

- `draw_g1_imshow.py`: Generates global distribution (imshow) maps for various parameters.
- `draw_g1_imshow_FMFY.py`: Generates global distribution (imshow) maps for First Month and Year.
- `draw_g1r1_DF.py`: Generates global and regional distribution (imshow) maps for Dbedrock Frequency.
- `draw_g2_scatter.py`: Generates global distribution (scatter) maps for various parameters.
- `draw_g2_scatter_partition.py`: Generates global distribution (scatter) maps for partition parameters.
- `draw_g2_scatter_statistics.py`: Generates global distribution (scatter) maps for statistics parameters.
- `draw_g2_scatter_Db.py`: Generates global distribution (scatter) maps for Dbedrock.
- `draw_r1_imshow.py`: Generates regional distribution (imshow) maps for various parameters.
- `draw_r2_scatter.py`: Generates regional distribution (scatter) maps for various parameters.
- `draw_h1_field.py`: Draw the field data (DTB and Sbedrock) histogram map.
- `draw_h2_histogram.py`: Draw the sum data (different Continent and Subregion) histogram map.
- `draw_l1_change.py`: Site change line chart plot.
- `draw_l2_latlon.py`: Sum Area and Sbedrock Line chart plot.
- `draw_l3_test.py`: .
- `draw_b1_box.py`: Boxplot of different Koppen and IGBP.
- `draw_c1_DTB.py`: Combination of DTB in Iowa.
- `draw_v1_class.py`: Violin plot in different class (Continent, Subregion, Sovereignt, IGBP and Koppen).

## Global Distribution Map

### draw_g1_imshow.py

#### Sbedrock

- `g1_Sb.png`
- `g1_Sb_n2p.png`
- `g1_Sb_n2p_nm.png`

#### Sr

- `g1_Sr.png`
- `g1_Sr_nm.png`

#### Ssoil

- `g1_Ss.png`

#### PR

- `g1_PR.png`

#### ET

- `g1_ET.png`

#### Q

- `g1_Q.png`

#### LH(Latent Heat)

- `g1_LH.png`

#### PET

#### Proportion1(Sbedrock/Sr)

- `g1_P1.png`
- `g1_P1_n2p.png`
- `g1_P1_n2p_nm.png`

#### Proportion2(Sbedrock/ET)

- `g1_P2.png`
- `g1_P2_n2p.png`
- `g1_P2_n2p_nm.png`

#### Proportion3(Q/PR)

- `g1_P3.png`
- `g1_P3_n2p.png`
- `g1_P3_n2p_nm.png`

#### Proportion4(ET/PR)

#### Proportion5(PET/PR)

#### Proportion6(ASI)

#### FD(first day)

- `g1_FD.png`
- `g1_FD_mean.png`
    modify month

#### DTB

- `g1_DTB.png`
- `g1_DTB_mask2.png`
    DTB and DTB with woody vegetation

#### Biomass

- `g1_Ag.png`
- `g1_Ag_nm.png`
- `g1_Bg.png`
- `g1_Bg_nm.png`

### IGBP

- `g1_IGBP.png`

### Koppen:
g1_Koppen.png
    global IGBP and Koppen
#### mask:
g1_mask123.png  
g1_mask12.png  
g1_mask1.png  
g1_mask2.png  
g1_mask3.png
<!-- #### Dr:
g1_Dr_(2003-2020).png -->
#### Dbedrock:
g1_Db_(2003-2020).png

### draw_g1_imshow_FDFMFY.py:

### draw_g2_scatter.py:
    all of this data with mask123
#### Sbedrock:
g2_Sb.png
#### Sr:
g2_Sr.png
#### Ssoil:
g2_Ss.png
#### PR:
g2_PR.png
#### ET:
g2_ET.png
#### Q:
g2_Q.png
#### LH(Latent Heat):
g2_LH.png
#### PET:
#### Proportion1(Sbedrock/Sr):
g2_P1.png
#### Proportion2(Sbedrock/ET):
g2_P2.png
#### Proportion3(Q/PR):
g2_P3.png
#### Proportion4(ET/PR):
#### Proportion5(PET/PR):
#### Proportion6(ASI):
#### FD(first day):
g2_FD_mean.png
#### DTB:
g2_DTB.png
#### Biomass:
g2_Ag.png
g2_Bg.png
### IGBP:
g2_IGBP.png
### Koppen:
g2_Koppen.png

### draw_g2_scatter_Db.py:
    all of this data with mask123
<!-- #### Dr:
g1_Dr_(2003-2020).png -->
#### Dbedrock:
g2_Db_(2003-2020).png

### c_plot_DFG.py:
#### Dbedrock Frequency:
g3_DF.png






## Regional Distribution Map：
Sr
Sbedrock
Ssoil
...

## Fit Station Map:
p_cao_t1.png
change.png

## Box plot：
p_fSb_test1.pdf

## Violin plot:
Continent:
Subregion:
Sovereignt:

## Histogram (Site Validation)
DTB site:
Sbedrock site:

fig_scatter:
scatter绘图

fig1:
各种diff

fig3:
lat\lon.png
各种diff

fig4_US:
对比US数据

fig5:
violin图

