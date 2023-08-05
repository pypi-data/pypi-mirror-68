def write_par_colibri2trilegal(input_object,input_file):

   c=input_object
###############write colibri2trilegal input file###############
   tst=open(input_file, 'w')
   tst.write('agbtrack_dir '+c.agbtrack_dir+'\n')
   tst.write('agb_mix '+c.agb_mix+'\n')
   tst.write('set_name '+c.set_name+'\n')
   tst.write('DLOGL '+c.DLOGL+'\n')
   tst.write('trilegal_dir '+c.trilegal_dir+'\n')
   tst.write('file_isotrack '+c.file_isotrack+'\n')
   tst.write('mass_loss '+c.mass_loss+'\n')
   tst.write('isotrack_dir '+c.isotrack_dir+'\n')
   tst.write('tracce_dir '+c.tracce_dir+'\n')
   tst.write('make_imfr '+c.make_imfr+'\n')
   tst.write('diagnostic_dir0 '+c.diagnostic_dir0+'\n')
   tst.write('diag_plots '+c.diag_plots+'\n')
   tst.write('over_write '+c.over_write+'\n')
   tst.close()
############################################
