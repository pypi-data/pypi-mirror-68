
#def def_par_trilegal(cmdinput_file, triinput_file):

#if (len(sys.argv) != 3):
#   print 'write_par_trilegal.py usage: write_par_trilegal(cmd_object, cmdinput_file, tri_object, triinput_file)'
#   sys.exit(2)

#cmdinput_file=sys.argv[0]
#cmd_object=sys.argv[1]
#tri_object=sys.argv[2]
#triinput_file=sys.argv[3]


def write_par_trilegal(cmd_object, cmdinput_file, tri_object, triinput_file):

   c=cmd_object
   t=tri_object
###############write cmd file###############
   cmd=open(cmdinput_file, 'w')
   cmd.write(c.kind_tracks+' '+c.file_isotrack+' '+c.file_lowzams+' #\n')
   cmd.write(c.kind_tpagb+' '+c.file_tpagb+' '+c.kind_pulsecycle+' #\n')
   cmd.write(c.kind_postagb+' '+c.file_postagb+' #\n')
   cmd.write(c.kind_ifmr+' '+c.file_ifmr+' #\n')
   cmd.write(c.kind_rgbmloss+' '+c.funkind+' '+c.eta_reimers+' #\n')
   cmd.write("DUST_M08"+' '+c.dust_m08+' #\n')
   cmd.write("PRINT_POSTAGB"+' '+c.print_postagb+' #\n')   
#   cmd.write("FCD"+' '+c.fcd+' #\n')
#   cmd.write(c.rgbmin+' #\n')
#   cmd.write(c.rgbmax+' #\n')
   cmd.write(c.flag_lpv+' '+c.kind_lpv+' #\n')
#   cmd.write(c.print_postagb+' #\n')
   cmd.write(c.print_tpagb+' #\n')
   cmd.close()
############################################



######################write triinput file#########################
   tri=open(triinput_file, 'w')
   tri.write(t.simulation_kind+' '+t.eq_alpha+' '+t.eq_delta+' '+t.field+' #\n')
   tri.write('\n')

   tri.write(t.kind_mag+' '+t.file_mag+' #\n')  #!!!!!
   if (t.kind_mag !=1):
      tri.write(t.file_cspec+' #\n')
      tri.write(t.kind_dustM+' '+t.file_dustM+' #\n')
      tri.write(t.kind_dustC+' '+t.file_dustC+' #\n')
   tri.write(t.mag_limit+' #\n')
   if (len(t.error1) > 1):
      tri.write(t.error1+' #\n')
   if (len(t.error2) > 1):
      tri.write(t.error2+' #\n')
   tri.write('\n')

   tri.write(t.r_sun+' '+t.z_sun+' #\n')
   tri.write('\n')

   tri.write(t.file_imf+' #\n')
   tri.write(t.binary_kind+' #\n')
   tri.write(t.binary_frac+' #\n')
   tri.write(t.binary_mrinf+' '+t.binary_mrsup+' #\n')
   tri.write('\n')

   tri.write(t.extinction_kind+' #\n')
   tri.write(t.extinction_rho_sun+' #\n')
   tri.write(t.extinction_infty+' '+t.extinction_sigma+' #\n')
   tri.write(t.extinction_h_r+' '+t.extinction_h_z+' #\n')
   tri.write('\n')

   tri.write(t.thindisk_kind+' #\n')
   tri.write(t.thindisk_rho_sun+' #\n')
   tri.write(t.thindisk_h_r+' '+t.thindisk_r_min+' '+t.thindisk_r_max+' #\n')
   tri.write(t.thindisk_h_z0+' '+t.thindisk_hz_tau0+' '+t.thindisk_hz_alpha+' #\n')
   tri.write(t.file_sfr_thindisk+' '+t.A_thindisk+' '+t.B_thindisk+' #\n')
   tri.write('\n')

   tri.write(t.thickdisk_kind+' #\n')
   tri.write(t.rho_thickdisk_sun+' #\n')
   tri.write(t.thickdisk_h_r+' '+t.thickdisk_r_min+' '+t.thickdisk_r_max+' #\n')
   tri.write(t.thickdisk_h_z+' #\n')
   tri.write(t.file_sfr_thickdisk+' '+t.A_thickdisk+' '+t.B_thickdisk+' #\n')
   tri.write('\n')

   tri.write(t.halo_kind+' #\n')
   tri.write(t.halo_rho_sun+' #\n')
   tri.write(t.halo_r_eff+' '+t.halo_q+' '+t.halo_n+' #\n')
   tri.write(t.file_sfr_halo+' '+t.A_halo+' '+t.B_halo+' #\n')
   tri.write('\n')

   tri.write(t.bulge_kind+' #\n')
   tri.write(t.bulge_rho_central+' #\n')
   tri.write(t.bulge_am+' '+t.bulge_a0+' #\n')
   tri.write(t.bulge_eta+' '+t.bulge_csi+' '+t.bulge_phi0+' #\n')
   tri.write(t.bulge_cutoffmass+' #\n')
   tri.write(t.file_sfr_bulge+' '+t.A_bulge+' '+t.B_bulge+' #\n')
   tri.write('\n')

   tri.write(t.object_kind+' #\n')
   tri.write(t.object_mass+' '+t.object_dist+' #\n')
   tri.write(t.object_avkind+' '+t.object_av+' #\n')
   tri.write(t.object_cutoffmass+' #\n')
   tri.write(t.file_sfr+' '+t.A_object+' '+t.B_object+' #\n')
   tri.write('\n')

   tri.write(t.output_kind+' #\n')
   tri.close()
##############################################################
   return
