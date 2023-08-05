
#def_par_trilegal:

class cmd(object):
   def __init__(self):

#for CMD_input.dat
      self.kind_tracks='2'  
                 #1: Girarid2000 style
                 #2: PARSEC style
                 #3: seismic tracks: MESA
      self.file_isotrack='isotrack/parsec/CAF09_V1.2S_M36_S12D_NS_MAS3_comp.dat'
                 #tracks for low+intermediate mass 
      self.file_lowzams='isotrack/bassazams_fasulla.dat'
                 #tracks for low-ZAMS

      self.kind_tpagb='4'   
                 #0: none
                 #1: Girardi et al., synthetic on the flight, no dredge up
                 #2: Marigo & Girardi 2001, from file, includes mcore and C/O
                 #3: Marigo & Girardi 2007, from file, with period, mode and mloss  
                 #4: Marigo et al. 2012, from file, with period, mode and mloss  
      self.file_tpagb='isotrack/isotrack_agb/tracce_CAF09_S_NOV13.dat'
                 #tracks for TP-AGB
      self.kind_pulsecycle='3' #actually this variable is not read from input file but has become a varialbe with default value '3'.
                 #0: quiescent
                 #1: quiescent interpolated in mloss
                 #2: quiescent luminosity with mean mloss
                 #3: detailed pulse cycle reconstructed

      self.kind_postagb='0' 
                 #0: none
                 #1: from file
      self.file_postagb='isotrack/final/pne_wd_test.dat'
                 #PN+WD tracks

      self.kind_ifmr='0'
                 #initial-to-final-mass-relation
      self.file_ifmr='tab_ifmr/weidemann.dat'

      self.kind_rgbmloss='RGB_MLR'
                 #0: RGB mass loss is turned-off
                 #1: RGB_MLR
      self.funkind='Reimers'
      self.eta_reimers='0.2'

#      self.rgbmin='MLR_MMIN 1.0' #actually not implemented yet
#      self.rgbmax='MLR_MMAX 1.7'

      self.dust_m08='M08_v2'
#      self.fcd='0.1'
      self.print_postagb='NO'

      self.flag_lpv='LPV_PERIOD'
      self.kind_lpv='Trabucchi'

#      self.print_postagb=''
      self.print_tpagb=''
###########################################################


#for triinput.dat
class tri(object):
   def __init__(self):


      self.simulation_kind='2'
                 #1: Galactic coordinates
                 #2: Equatorial coordinates
      self.eq_alpha='12.918862' #for M31 #'82.1849778'
                 #in hours
                 #or gc_l (deg)
      self.eq_delta='41.197344' #for M31 #'-66.2356728'
                 #in deg
                 #or gc_b (deg)
      self.field='0.00053' #for PHAT 83.*83./3600./3600.=#'0.0007486'
                 #deg^2

      self.kind_mag='4'
                 #1: models with no dust and using Loidl et al. models for C stars, no dust table expected 
                 #2: ?
                 #3: Aringer et al. models for C stars, C star tables to be expected
      self.file_mag='YBC/YBC/2mass'
      #self.file_cspec='bc_odfnewbern/vista/bc_cspec.dat'
      self.file_cspec='YBC/YBC/Avodonnell94Rv3.1YBC.list 1 -100. 5500. 6500. 4550. 4850. 1.5 2.'
      self.kind_dustM='1'
                 #1: uses Groenewegen 06 approach
                 #2: uses Bressan 98 approach
                 #3: uses Nanni 15 approach. Then kind_dustC=0, AS Nanni's tables are valid for both C and M.
                 #4: new Nanni tables
      self.file_dustM='tab_dust/tab_dust_dpmod60alox40_2mass.dat'
                 #'tab_dust/tab_dusty_nd_var_2mass.dat'
                 #1: tab_dust/tab_dust_dpmod60alox40_2mass.dat
                 #2: tab_dust/tab_dust_sil70_2mass.dat
                 #3: tab_dust/tab_dusty_LMC_2mass_spitzer_wise.dat
                 #4: tab_dust/tab_dusty_nd_var_vista.dat
      self.kind_dustC='1'
      self.file_dustC='tab_dust/tab_dust_AMCSIC15_2mass.dat'
                 #1: tab_dust/tab_dust_AMCSIC15_2mass.dat
                 #2: tab_dust/tab_dust_gra70_2mass.dat
      self.mag_limit='3 22 0.028'
      self.error1='' #'error 3 error_J.dat'
      self.error2='' #'error 5 error_Ks.dat'
#filter_num='5'
#mag_limit='22'
#mag_resolution='0.028'

      self.r_sun='8700.0'
      self.z_sun='24.2'

      self.file_imf='tab_imf/imf_chabrier_lognormal.dat'
      self.binary_kind='0'
                 #0: no binaries
                 #1: yes
      self.binary_frac='0.0'
      self.binary_mrinf='0.7'
      self.binary_mrsup='1.0'

      self.extinction_kind='0'
                 #0: none
                 #1: exp with local calibration???
                 #2: exp with calibration at infty
      self.extinction_rho_sun='0.00015'
                 #local extinction density Av, in mag/pc
      self.extinction_infty='0.04'
                 #extinction at infinity
      self.extinction_sigma='0.0'
                 #extinction relative sigma dispersion
      self.extinction_h_r='100000.0' 
                 #extinction radial scale length
      self.extinction_h_z='110.0'
                 #extinction vertical scale height

      self.thindisk_kind='0'
      self.thindisk_rho_sun='55.4082'
      self.thindisk_h_r='2913.36'
      self.thindisk_r_min='0.0'
      self.thindisk_r_max='15000.0'
      self.thindisk_h_z0='94.6902'
      self.thindisk_hz_tau0='5.55079e9' 
      self.thindisk_hz_alpha='1.6666'
      self.file_sfr_thindisk='tab_sfr/file_sfr_thindisk_mod.dat'
      self.A_thindisk='0.8'
      self.B_thindisk='0.0e9'

      self.thickdisk_kind='0'
                 # thickdisk kind: 0=none, 1=z_exp, 2=z_sech, 3=z_sech2
      self.rho_thickdisk_sun='0.0010'
      self.thickdisk_h_r='2394.07'
      self.thickdisk_r_min='0.0'
      self.thickdisk_r_max='15000.0'
      self.thickdisk_h_z='800'
      self.file_sfr_thickdisk='tab_sfr/file_sfr_thickdisk.dat'
      self.A_thickdisk='1.0'
      self.B_thickdisk='0.0e9'
S_035_phat_regions_M08.par
      self.halo_kind='0'
                 # halo kind: 0=none, 1=1/r^4 cf Young 76, 2=oblate cf Gilmore, 3=power-law cf. de Jong et al 2009
      self.halo_rho_sun='0.0001'
      self.halo_r_eff='2698.93'
      self.halo_q='0.62'
      self.halo_n='2.75'
      self.file_sfr_halo='tab_sfr/file_sfr_halo.dat'
      self.A_halo='1.0'
      self.B_halo='0.0e9'

      self.bulge_kind='0'
      self.bulge_rho_central='406.0'
      self.bulge_am='2500.0'
      self.bulge_a0='95.0'
      self.bulge_eta='0.68'
      self.bulge_csi='0.31'
      self.bulge_phi0='15.0'
      self.bulge_cutoffmass='0.6'
      self.file_sfr_bulge='tab_sfr/file_sfr_bulge_zoccali_p03.dat'
      self.A_bulge='1.0'
      self.B_bulge='0.0e9'

      self.object_kind='1'
                # object kind: 0=none, 1=at fixed distance 
      self.object_mass='150000.0'
                #total mass inside object field in solar mass
      self.object_dist='50000.0'
                #distance to the object in pc
      self.object_avkind='0'
                #0: Av added to foreground
                #1: Av not added to foreground
      self.object_av='0.07'
                #Av added to foreground
      self.object_cutoffmass='0.8'
                #object_cutoffmass: (Msun) masses lower than this will be ignored
      self.file_sfr='' 
                #../../SC/trilegal_run/sfr_NGC1978_1.9Gyr_t400_Z0.008.dat'
      self.A_object='1.0'
      self.B_object='0.0e9'
                #tab_sfr/sfr_NGC1978.dat 1.0 0.0e9 # File with (t, SFR, Z), factors A, B 

      self.output_kind='1'
                #1: output catalogue
                #>=2: output Hess diagram
##############################################################

#def def_par_trilegal():
class def_par_trilegal(object):
   def __init__(self):
      self.cmd=cmd()
      self.tri=tri()

#return trilegal
