#!/usr/bin/env python
import os
#import time
import sys
#import subprocess
import numpy as np
from partricol import tripar
from partricol import cypar
import astropy
from astropy.io import ascii
from astropy.table import Table, Column

#modified from pytri_phat
def run_trilegal(par_file, tri_bin='./main', out_options='-fits -iso iso_str'):

   #parsing the parameter file
   #if (len(sys.argv) < 2):
   #   print 'trilegal.py usage: trilegal par_file tri_bin [-fits] [-iso iso_str]' #tri_bin: trilegal executable, must be after par_file if exists
   #   sys.exit(2)

   trilegal_object=tripar.def_par_trilegal()
   cmd_object=trilegal_object.cmd
   tri_object=trilegal_object.tri

   str_uniq=par_file.replace('.par','')
   mod_par=cypar.read(par_file)
   par_name=mod_par.par_name
   par_val=mod_par.par_val


   #trilegal executable
   if (not os.path.isfile(tri_bin)):
      old_tri_bin=tri_bin
      tri_bin=os.path.join(os.environ.get('TRILEGAL_DIR'),'code/main')
      old_tri_bin=old_tri_bin+' '+tri_bin
      if (not os.path.isfile(tri_bin)):
         tri_bin=os.path.join(os.environ.get('TRILEGALDIR'),'code/main')
         old_tri_bin=old_tri_bin+' '+tri_bin
         if (not os.path.isfile(tri_bin)):
            print('not exist: '+old_tri_bin)

   print(tri_bin)
   fits_output=''
   options0=''

   if ('-fits' in out_options):
      print('fits output')
      fits_output='.fits'
   if ('-iso' in out_options):
      print('isochrone output:')
      fits_output='.iso.output' #for the moment no fits output support for isochrones
      options0='-i '+out_options[out_options.rfind("-iso"):]

   i1=-1
   for par_id in par_name:
      i1=i1+1
      if (par_id == 'file_sfr'):
         tri_object.file_sfr=par_val[i1]

   cmdinput_file=str_uniq+'_cmd_input.dat'
   triinput_file=str_uniq+'_tri_input.dat'
   log_file=str_uniq+'_log.dat'

   ##modify cmd parameters
   for key_name in cmd_object.__dict__.keys():
      i1=-1
      for par_id in par_name:
         i1=i1+1
         if (par_id == key_name):
            setattr(cmd_object,key_name, par_val[i1])

   ##modify tri parameters
   for key_name in tri_object.__dict__.keys():
      i1=-1
      for par_id in par_name:
         i1=i1+1
         if (par_id == key_name):
            setattr(tri_object,key_name, par_val[i1])

   ####write out the modified cmd and tri input paramter files
   write_par_trilegal.write_par_trilegal(cmd_object, cmdinput_file, tri_object, triinput_file)



   #trilegal command line
   options=options0+' -s -a -l -f'
                 #-i: print isochrone(s) and exit
                 #-f: cmdinputfile followed
                 #-t: ?
                 #-k: output kinematics
                 #-a: output AGB data
                 #-l: output labels (TP-AGB=8, E-AGB, ...)
                 #-s: output star variables
                 #-b: print full info on binaries
                 #output file name with ".fits": output in fits format
   # output isochrone with fits will result in segmentation fault
   #output simulation with fits lacks some properties as output with ascii format

   output_file=par_file.replace('.par','.fits')


   command='nice -20 '+tri_bin+' '+options+' '+cmdinput_file+' '+triinput_file+' '+output_file+fits_output + '>' + log_file #+ '&'
   if ('-iso' in sys.argv):
      command='nice -20 '+tri_bin+' '+options+' '+cmdinput_file+' '+triinput_file+' '+output_file+fits_output + '>' + log_file.replace('log.dat','log_iso.dat') #+ '&'
   print(command)
   os.system(command)
