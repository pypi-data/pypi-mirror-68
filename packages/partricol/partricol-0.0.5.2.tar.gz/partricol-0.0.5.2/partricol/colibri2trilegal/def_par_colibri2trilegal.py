class def_par_colibri2trilegal(object):
   def __init__(self):
#for colibri2trilegal input parameter files
      


# COLIBRI directory structure is [agbtrack_dir]/[agb_mix]/[set_name]
      self.agbtrack_dir='./colibri'
      self.agb_mix='CAF09'
      self.set_name='S_TST'


#sampling interval in logl for E-AGB
      self.DLOGL='0.01'


# Parameters for TRILEGAL INPUT:



# Where input files will go for TRILEGAL
      self.trilegal_dir='cmd_inputfiles/'



# Non-TP-AGB tracks to use
      self.file_isotrack='isotrack/parsec/CAF09_S12D_NS_1TP.dat'



# mass_loss parameter (for RGB stars) so far only "Reimers: [float]"
      self.mass_loss='Reimers: 0.2'



# TRILEGAL formatted TP-AGB tracks will go here:
   # structure: [isotrack_dir]/[agb_mix]/[set_name]
      self.isotrack_dir='isotrack_agb/fittedTeff/'



# File to link TRILEGAL formatted TP-AGB tracks to cmd_input:
      self.tracce_dir='isotrack_agb/fittedTeff/'



### Diag plots, extra files:



# make initial and final mass relation (and also lifetimes c and m)?
   # (Need more than one metallicity)
      self.make_imfr='True'



# Diagnostic plots base, this will have directory structure:
   # diagnostic_dir/[agb_mix]/[metallicity]/[set]/
      self.diagnostic_dir0='./diagnostics/'



# If True, will make HRD or age vs C/O, log L, log Te
      self.diag_plots='True'



### Misc Options:



# overwrite TRILEGAL formatted TP-AGB tracks and the output diag plots?
      self.over_write='True'



# only do these metallicities (if commented out, do all metallicities)
   #metals_subset       0.001, 0.004, 0.0005, 0.006, 0.008, 0.01, 0.017
