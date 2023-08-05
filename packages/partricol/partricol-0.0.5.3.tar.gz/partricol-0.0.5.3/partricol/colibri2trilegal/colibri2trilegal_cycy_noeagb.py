""" Utilities for converting COLIBRI tracks into TRILEGAL tracks """
import glob
import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from ast import literal_eval
from matplotlib import cm, rcParams
from matplotlib.ticker import NullFormatter, MultipleLocator, ScalarFormatter, MaxNLocator

import scipy
import scipy.optimize as optimize

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("EAGB: Yang Chen's modified version of colibri2trilegal")

#rcParams['text.usetex'] = True
#rcParams['text.latex.unicode'] = False
rcParams['axes.linewidth'] = 1
rcParams['ytick.labelsize'] = 'large'
rcParams['xtick.labelsize'] = 'large'
rcParams['axes.edgecolor'] = 'black'

nullfmt = NullFormatter()  # no labels

#the following two parametes can be used to correct the loops presented in the trilegal simulated isochcrones
#basically you can increase valid_points_cy and decrease fits0_thresh_cy to overcome strange behaviors
valid_points_cy=5#10 #10 Ok #this parameter can help to remove red loops, at 6-8, there is still a little loop for S_NOV13 sets. However, with 10, the loop for Z=0.00155 are not eliminated. For the moment, I ignore this.
#fits0_thresh_cy=5.0
N_Tgrid=50001 #51
#N_eagb=10+2
DLOGL_g=0.02 #0.0025

#def colibri2trilegal(input_file):
def colibri2trilegal(agbtrack_dir='CAF09/S_035',agb_mix='CAF09',set_name='S_035',DLOGL=0.02,\
                     isotrack_dir='./',\
                     make_imfr=True,diagnostic_dir0='diagnostics',metals_subset=None,over_write=True,diag_plots=True):
    '''
    This script formats Paola's tracks and creates the files needed to use them
    with TRILEGAL as well as the option to make diagnostic plots.

    infile is an input_file object. See class InputFile

    WHAT'S GOING ON:
    Here is what it takes to go from COLIBRI agb tracks to TRILEGAL:

    1. COLIBRI tracks
    2. COLIBRI tracks formatted for TRILEGAL
    3. TRILEGAL files that link to COLIBRI re-formatted tracks

    1. COLIBRI tracks must have naming scheme
        [mix]/[set]/[Trash]_[metallicity]_[Y]/[track_identifier]
    ex: agb_caf09_z0.008/S1/agb_*Z*.dat
    ex: CAF09/S_SCS/*Z*/agb_*Z*.dat
    These can live anywhere, and do not need to be included in TRILEGAL
    directories.

    2. COLIBRI tracks are formatted for TRILEGAL with no header file.
    They only include the quiescent phases and a column with dL/dT
    (See AGBTracks)

    3. TRILEGAL needs two files to link to COLIBRI re-formatted tracks
       a. track file goes here: isotrack/tracce_[mix]_[set].dat
       b. cmd_input_file that links to the track file
          goes here trilegal_1.3/cmd_input_[mix]_[set].dat
    '''

    global DLOGL_g
    if ((DLOGL > 0) & (DLOGL < DLOGL_g)): DLOGL_g=DLOGL
    logger.info('DLOGL0 {}'.format(DLOGL_g))


    # set up file names and directories, cd to COLIBRI tracks.
    '''set up files and directories for TPAGB parsing.'''
    home_dir = os.getcwd()

    # Check for Paola's formatted tracks
    os.system("pwd")
    logger.info("isotrack_dir:"+isotrack_dir)
    ensure_dir(isotrack_dir)

    
    # are we making diagnostic plots, check directory.
    if diagnostic_dir0:
        pass
    else:
        logger.info('not making diagnostic plots')

    # set name convention: [mix]_[set].dat
    name_conv = '{}_{}.dat'.format(agb_mix, set_name)

    # set track search string
    track_identifier = 'agb*_*Z*.dat'


    # track file to link from cmd_input to paola's formatted tracks
    tracce_fh = '_'.join(('tracce', name_conv))

    tracce_file = os.path.join(isotrack_dir, tracce_fh)


    # moving to the the directory with metallicities.
    working_dir = agbtrack_dir
    os.chdir(working_dir)
    metal_dirs = [m for m in os.listdir(working_dir)
                  if os.path.isdir(m) and 'Z' in m]

    if metals_subset is not None:
        logger.info('doing a subset of metallicities')
        metal_dirs = [m for m in metal_dirs
                      if metallicity_from_dir(m)[0] in metals_subset]
    metals = np.argsort([metallicity_from_dir(m)[0] for m in metal_dirs])
    metal_dirs = np.array(metal_dirs)[metals]
    logger.info('found {} metallicities'.format(len(metal_dirs)))







    # list of isofiles, zs, and ys to send to tracce file.
    isofiles, Zs, Ys = [], [], []
    imfr_data = np.array([])
    lifetime_data = np.array([])

    for metal_dir in metal_dirs:
        metallicity, Y = metallicity_from_dir(metal_dir)
        logger.info('Z = {}'.format(metallicity))
        if diag_plots is True:
            if diagnostic_dir0 is not None:
                diagnostic_dir = os.path.join(isotrack_dir, diagnostic_dir0, metal_dir)  + '/'
            else:
                logger.error('Must specifiy diagnostic_dir0 diag plots')
                sys.exit(2)

        agb_tracks = get_files(os.path.join(agbtrack_dir, metal_dir), track_identifier)
        #logger.info(os.path.join(agbtrack_dir, agb_mix, set_name, metal_dir))
        agb_tracks.sort()
        assert len(agb_tracks) > 0, 'No agb tracks found!'
        iso_name_conv = '_'.join(('Z%.4f' % metallicity, name_conv))
        isofile = os.path.join(home_dir, isotrack_dir, iso_name_conv)
        isofile_cy=isofile+'.cycy'


        if over_write is False and os.path.isfile(isofile):
            logger.warning('not over writing {}'.format(isofile))
            out = None
        else:
            out = open(isofile, 'w')
            out_cy=open(isofile_cy, 'w')
            out_cy.write('# Mini age(yr) logL logTe m_act mcore period ip Mdot(Msun/yr) X Y X_C X_N X_O dlogTe/dlogL Xm Ym X_Cm X_Nm X_Om minL maxL minMenv maxMenv fits0 fits1 fits2 fits3 fits4 resi\n')

        isofile_rel_name = os.path.join('isotrack', isotrack_dir,
                                        iso_name_conv)
        logger.info('found {} tracks'.format(len(agb_tracks)))
        for i, agb_track in enumerate(agb_tracks):
            logger.info("")
            logger.info('track: '+agb_track)
            # load track
            track = get_numeric_data(agb_track)

            if track == -1:
                continue

#            if track.n_tpagb == 0:
#                logger.info('track without no TP-AGB, skip: '+agb_track)
#                continue
            
            if track.bad_track is True: #commet this out to output also tracks without TP-AGB
                continue
            if len(track.Qs) <=2:  #commet this out to output also tracks without TP-AGB
                continue

            

            assert metallicity == track.metallicity, \
                'directory and track metallicity do not match'

            # make iso file for trilegal
            if out is not None:
                if i == 0:
                    make_iso_file(track, out, out_cy, write_header=True)
                else:
                    make_iso_file(track, out, out_cy)

            if track.bad_track is True:
                continue

            # save information for lifetime file.
            lifetime_datum = np.array([metallicity, track.mass, track.tauc,
                                       track.taum])

            lifetime_data = np.append(lifetime_data, lifetime_datum)

            # make diagnostic plots
            if diag_plots is True and diagnostic_dir0 is not None:
                assert metallicity_from_dir(diagnostic_dir)[0] == \
                    track.metallicity, 'diag dir met wrong!'
                diag_plots_cy(track, home_dir=home_dir, agb_mix=agb_mix, set_name=set_name, diagnostic_dir=diagnostic_dir)

            # save information for imfr
            if make_imfr is True:
                M_s = track.data_array['M_star']
                imfr_datum = np.array([M_s[0], M_s[-1], float(metallicity)])
                imfr_data = np.append(imfr_data, imfr_datum)

        if out is not None:
            out.close()
            logger.info('wrote {}'.format(isofile))

        # keep information for tracce file
        isofiles.append(isofile_rel_name)
        Ys.append(Y)
        Zs.append(metallicity)

    # make file to link cmd_input to formatted agb tracks
    make_met_file(tracce_file, Zs, Ys, isofiles)


    if make_imfr is True and diagnostic_dir0 is not None:
        ifmr_file = os.path.join(isotrack_dir, diagnostic_dir0, '_'.join(('ifmr', name_conv)))
        ncols = 3
        nrows = int(imfr_data.size/ncols)
        savetxt(ifmr_file, imfr_data.reshape(nrows, ncols),
                       header='# M_i M_f Z \n')
        plot_ifmr(ifmr_file)

    if diagnostic_dir0 is not None and diag_plots is True:
        lifetime_file = os.path.join(isotrack_dir, diagnostic_dir0, '_'.join(('tau_cm', name_conv)))
        ncols = 4
        nrows = int(lifetime_data.size / ncols)
        savetxt(lifetime_file, lifetime_data.reshape(nrows, ncols),
                       header='# z mass tauc taum\n')
        plot_cluster_test(lifetime_file)

    os.chdir(home_dir)
    return(tracce_file)



def metallicity_from_dir(met):
    ''' take Z and Y values from string'''
    if met.endswith('/'):
        met = met[:-1]

    if len(os.path.split(met)) > 0:
        met = os.path.split(met)[1]

    z = float(met.split('_')[1].replace('Z', ''))
    y = float(met.split('_')[-1].replace('Y', ''))

    return z, y



################################fitting functions
def func_cy0(par, x, y):
   return par[0]+par[1]*x

def func_cy1(x,y,z0, alpha, beta):
   return z0 + alpha*x + beta*y

def func_cy2(par, x, y):
   return par[0]*x + par[1]*y

def func_cy3(par, x, y):
   return par[0]*x + par[1]*x**2

def func_cy4(par, x, y):
   z=np.array([])
   for r in x:
      if r < par[0]:
         z=np.append(z,par[1]*r)
      else:
         z=np.append(z,par[2]*r)
   return z

def func_cy5(par,x,y):
   z=par[0]*x+par[1]*x**par[2]
   return z

def func_cy6(par,x,y):
   z=par[0] +par[1]*x+par[2]*x**2 #+par[1]*x**par[2]
   return z

def func_cy7(par,x,y):
   z=par[0] +par[1]*x+par[2]*10.**(par[3]*x) #+par[1]*x**par[2]
   return z

def func_cy(par,x,y): ##fine! #I am taking this one!
   z=par[0]+par[1]*x+par[2]*y #+par[1]*x**par[2]
   return z

def func_cy8_1(par,x,y): ##fine! #I am taking this one!
   z=par[0]+par[1]*x#+par[2]*0 #+par[1]*x**par[2]
   return z

def func_cy8_2(par,x,y): ##fine! #I am taking this one!
   z=par[0]+par[1]*y
   return z

def func_cy9(par,x,y): ##fine!
   z=par[0]+par[1]*x+par[2]*y+par[3]*x**2 + 0.*par[4]*y**2
   return z

def func_cy10(par,x,y): ##compared to func11, it is better at mass>1.4
   z=par[0]+par[1]*x+par[2]*y+par[3]*y**2 #+par[1]*x**par[2]
   return z

def func_cy11(par,x,y): ##fine!
   z=par[0]+par[1]*x+par[2]*x**2+par[3]*y**2 #+par[1]*x**par[2]
   return z

def func_cy12(par,x,y): ##fine!
   z=par[0]+par[1]*x+par[2]*10.**(par[3]*y) #+par[1]*x**par[2]
   return z

def func_cy13(par,x,y): ##good!
   z=par[0]+par[1]*x+par[2]*10.**(par[3]*y) +par[4]*y  #+par[1]*x**par[2]
   return z

def func_cy14(par,x,y): ##perfect!
   z=par[0]+par[1]*x+par[2]*10.**(par[3]*y) + par[4]*x**2 #+par[1]*x**par[2]
   return z

def func_cy15(par,x,y): ##perfect!
   z=par[0] + par[1]*x + par[2]*y + 0*par[3]*x**2 + 0*par[4]*y**2 # +par[5]*0.+par[6]*0. #+par[1]*x**par[2]
   return z

def func_cy16(par,x,y): ##perfect!
   z=par[0]+par[1]*x+par[2]*10.**(par[3]*y) +par[4]*y + par[5]*x**2 #+par[1]*x**par[2]
   return z

def func_cy17(par,x,y): 
   z=par[0]+par[1]*y+par[2]*y**2 #+par[1]*x**par[2]
   return z

def func_cy18(par,x,y): ##perfect!
   z=par[0] + par[1]*x + par[2]*y + par[3]*x**2 + par[4]*y**2 + par[5]*x*y # +par[5]*0.+par[6]*0. #+par[1]*x**par[2]
   return z

def func_cy19(par,x,y):
   for r in x:
      if r < par[4]:
         z=par[0] +par[1]*7+par[2]*10.**(par[3]*y) #+par[1]*x**par[2]
      if r > par[5]:
         z=par[0]
   return z



def residual_cy0(par,x,y,z):
   return (z-func_cy15(par,x,y))**2 #Take care, zero multiplied in this function

def residual_cy1(par,x,y,z):
   return (z-func_cy(par,x,y))**2

def residual_cy2(par,x,y,z):
   return (z-func_cy0(par,x,y))**2

def residual_cy3(par,x,y,z):
   return (z-func_cy8_2(par,x,y))**2

def residual_cy4(par,x,y,z):
   return (z-func_cy9(par,x,y))**2
################################



class AGBTracks(object):
    '''AGB data class'''
    def __init__(self, data_array, col_keys, name):
#        self.data_array = data_array
        self.key_dict = dict(zip(col_keys, range(len(col_keys))))

        if len(np.atleast_1d(data_array['NTP']))>1: self.n_eagb = len([i for i in data_array['NTP'] if i == -1.])
        self.n_tpagb = len(data_array['NTP']) - self.n_eagb
#        logger.info('n_eagb & n_tpagb:')
#        logger.info(self.n_eagb)
#        logger.info(self.n_tpagb)
        if (self.n_eagb > 0): self.eagb_in=data_array[0:self.n_eagb]
#        logger.info(self.eagb_in['step'][0])
#        logger.info(self.eagb_in['step'][-1])
        self.col_keys=col_keys
        
#TPAGBs
        self.data_array = data_array[self.n_eagb:]
        logger.info("n_tpagb {}".format(self.n_tpagb))
        if (self.n_tpagb > 0): self.data_array['PHI_TP'][0] = -1. #replace the fix_phi

#        logger.info(self.data_array['step'][0])
        self.name = name
        self.firstname = os.path.split(name)[1]
        self.mass = float(self.firstname.split('_')[1])
        self.metallicity = float(self.firstname.split('_')[2].replace('Z', ''))
        # initialize: it's a well formatted track with more than one pulse
        self.bad_track = False
        # if only one thermal pulse, stop the press.
        self.check_ntp()
        self.get_TP_inds()
        self.fits_cy=[]
        self.resi_cy=[]
        self.minL_cy=[]
        self.maxL_cy=[]
        self.minMenv_cy=[]
        self.maxMenv_cy=[]

#        print self.name

        if not self.bad_track:
            # force the beginning phase to not look like it's quiescent
#            self.fix_phi() #commented on 2017-05-17 by Yang chen. I have to check!!!!!!
            # load quiescent tracks
#            logger.info('NTP of the first point: {}'.format(self.data_array['PHI_TP'][0]))
            self.get_quiescent_inds()
            # load indices of m and c stars
            self.m_cstars()
            # calculate the lifetimes of m and c stars
            self.tauc_m()
            # add points to low mass quiescent track for better interpolation
            self.addpt = []
#comment out the following two lines to dismiss inserting points
#            if len(self.Qs) <= 9 and self.mass < 3.:
#                self.add_points_to_q_track()
            # find dl/dt of track
            self.find_dldt()
#            print 'cycy:',self.addpt
        else:
            logger.error('bad track: {}'.format(name))

            

    def eagb_write(self,row0, isofile=''):
          col_keys=self.col_keys
          fmt = '%.4e %.4f %.4f %.5f %.5f %.4e %i %.4e %.6e %.6e %.6e %.6e %.6e %.4f %.6e %.6e %.6e %.6e %.6e %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f\n'

          if row0['Pmod']==0 : period=row0['P0']
          else: period=row0['P1']

          mdot = 10 ** (row0['dMdt'])

          xc = np.sum([row0[c] for c in col_keys if c.startswith('C1')])
          xn = np.sum([row0[c] for c in col_keys if c.startswith('N1')])
          xo = np.sum([row0[c] for c in col_keys if c.startswith('O1')])

          imin = row0 #mins[i]
          xcm = np.sum([imin[c] for c in col_keys if c.startswith('C1')])
          xnm = np.sum([imin[c] for c in col_keys if c.startswith('N1')])
          xom = np.sum([imin[c] for c in col_keys if c.startswith('O1')])
          iminh = imin['H']
          iminy = imin['Y']
          if (isofile != ''):
             isofile.write(fmt % (row0['ageyr'], row0['L_star'], row0['T_star'],
                            row0['M_star'], row0['M_c'], period, row0['Pmod'],
                            mdot, row0['H'], row0['Y'], xc, xn, xo, 0.,
                            iminh, iminy, xcm, xnm, xom,
                            0., 0.,
                            0., 0.,
                            0., 0.,0.,0.,0.))


    def eagb(self, isofile=''):
       
       logger.info('resampling the eagb phase:')
       col_keys=self.col_keys

       n_eagb_out=0
       row0=self.eagb_in[0]
       logl0=self.eagb_in['L_star'][0]
       loglp=logl0
       logger.info("DLOGL1: {}".format(DLOGL_g))
       for i,row in enumerate(self.eagb_in):
          logl=row['L_star']
          if ((n_eagb_out != 0) & (i != self.n_eagb-1) & (abs(logl-loglp) < DLOGL_g)):
             if ((logl-loglp)*(logl-self.eagb_in['L_star'][i+1])<=0):
                 logl0=logl
                 row0=row
                 continue

          if (i == self.n_eagb-1): row0=row
          else:
              if ((logl-loglp)*(logl-self.eagb_in['L_star'][i+1])>0): row0=row
          
          if False: self.eagb_write(row0, isofile=isofile)
          
          n_eagb_out=n_eagb_out+1
          logl0=logl
          loglp=logl
          row0=row

       self.n_eagb_out=n_eagb_out                     
    

       
       
    def find_dldt(self, order=1):
        '''
        Finds dL/dt of track object by a poly fit of order = 1 (default)
        '''
        TPs = self.TPs
        qs = list(self.Qs)
        status = self.data_array['status']
        logl = self.data_array['L_star']
        logt = self.data_array['T_star']
        phi = self.data_array['PHI_TP']
        # if a low mass interpolation point was added it will get
        # the same slope as the rest of the thermal pulse.
        #dl/dT seems somewhat linear for 0.2 < phi < 0.4 ...
        lin_rise, = np.nonzero((status == 7) & (phi < 0.4) & (phi > 0.2))
        rising = [list(set(TP) & set(lin_rise)) for TP in TPs] #rising: index of status==7 points for each TPs
        fits = [np.polyfit(logt[r], logl[r], order) for r in rising if len(r) > 0]

##for the last cycle

        slopes = np.array([])
        # first line slope
        slopes = np.append(slopes, (logl[2] - logl[0]) / (logt[2] - logt[0]))
        # poly fitted slopes
        slopes = np.append(slopes, [fits[i][0] for i in range(len(fits))])

        # pop in an additional copy of the slope if an interpolation point
        # was added.
        ##By testing on S_NOV13 and S_MAR16(Z=0.004 and 0.006) addpt is alwyas empty (Yang Chen 31/03/2016)
        if len(self.addpt) > 0:
            tps_of_addpt = np.array([i for i in range(len(TPs))
                                    if list(set(self.addpt) & set(TPs[i])) > 0])
            slopes = np.insert(slopes, tps_of_addpt, slopes[tps_of_addpt])

        self.Qs = np.insert(self.Qs, 0, 0)
        self.rising = rising
        self.slopes = slopes
        self.fits = fits

####fitting by Yang Chen
        step_cy=self.data_array['step']-1
        menv_cy=self.data_array['M_star']-self.data_array['M_c']
        minTid_cy=np.argmin(logt)
        lin_rise_cy, = np.nonzero( (status == 7) )
        rising_cy0 = [list(set(TP) & set(lin_rise_cy)) for TP in TPs]
#        rising_cy = [np.sort(tmp_cy)[1:] for tmp_cy in rising_cy0] #removing the first point, as there is always a jump
        rising_cy = [np.sort(tmp_cy) for tmp_cy in rising_cy0] #removing the first point, as there is always a jump


#finding the fitting range through judging the Teff
#        bad_tp=np.array([])
        for i1 in range(len(rising_cy)):
           continue
#           print i1
           tmp_cy=rising_cy[i1]
           if (len(tmp_cy) <=valid_points_cy):
#              bad_tp=np.append(bad_tp,True)
              continue
           minTid1=tmp_cy[np.argmin(logt[tmp_cy])]
#           id0=np.where( (tmp_cy <=minTid1) & (tmp_cy >=maxTid1) )[0]
           id0=np.where(tmp_cy <=minTid1)[0]
           rising_cy[i1] = tmp_cy[id0]
#           print i1,len(rising_cy[i1])
           tmp_cy=rising_cy[i1]
           maxTid1=tmp_cy[np.argmax(logt[tmp_cy])]


#finding the fitting range through judging the Teff but may not be neccessary
        for i1 in range(len(rising_cy)):
         continue
         if (False):
           tmp_cy=rising_cy[i1]
           if (len(tmp_cy) <=valid_points_cy):
              continue
           minLid1=tmp_cy[np.argmin(logl[tmp_cy])]
           maxLid1=tmp_cy[np.argmax(logl[tmp_cy])]
           id0=np.where( (tmp_cy >=minLid1) & (tmp_cy <=maxLid1) )[0]
           rising_cy[i1] = tmp_cy[id0]

#selecting points for fitting, but may not be neccessary
        for i1 in range(len(rising_cy)):
           continue
#         if (False):
           tmp_cy=rising_cy[i1]
#           print i1,len(rising_cy[i1]),len(tmp_cy)
           if (len(tmp_cy) <=valid_points_cy):
              continue
           minT1=np.min(logt[tmp_cy])
           maxT1=np.max(logt[tmp_cy])
           Tgrid=np.linspace(maxT1,minT1,num=N_Tgrid)
           id1 = np.array([tmp_cy[0]])

           for i2 in range(1,len(Tgrid)-2):

              id2=np.argmin( np.abs(logt[tmp_cy]-Tgrid[i2]) )
              id1=np.append(id1,tmp_cy[id2])

           id1=np.append(id1,tmp_cy[-1])

           rising_cy[i1] = np.unique(id1) #important


        cy_i=0
        fits_cy=np.array([0.,0.,0.,0.,0.])
        resi_cy=np.array([0.])
        minL_cy=np.array([0.])
        maxL_cy=np.array([0.])
        minMenv_cy=np.array([0.])
        maxMenv_cy=np.array([0.])


#        print rising_cy
        for r in rising_cy:
           if (len(r) >= valid_points_cy):
              fits_cy_tmp = optimize.leastsq(residual_cy0,[0.,0.,0.,0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]

#2016-10-11
#              if (fits_cy_tmp[0] < 0.):
#                 fits_cy_tmp=fits_cy_tmp*0. #important!!!


              resi_cy_tmp=np.max(residual_cy0(fits_cy_tmp,logl[r],menv_cy[r],logt[r]))

#              if  (resi_cy_tmp > 1E-3):
#                 fits_cy_tmp = optimize.leastsq(residual_cy4,[0.,0.,0.,0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]
#                 resi_cy_tmp=np.max(residual_cy4(fits_cy_tmp,logl[r],menv_cy[r],logt[r]))


              cy_i=cy_i+1
              fits_cy= np.vstack([fits_cy,fits_cy_tmp]) #[fits_cy,fits_cy_tmp] #np.append(fits_cy,fits_cy_tmp)
              resi_cy=np.append(resi_cy,resi_cy_tmp)

              minL_cy = np.append(minL_cy,np.min(logl[r]))
              maxL_cy = np.append(maxL_cy,np.max(logl[r]))
              minMenv_cy = np.append(minMenv_cy,np.min(menv_cy[r]))
              maxMenv_cy = np.append(maxMenv_cy,np.max(menv_cy[r]))
#              print cy_i,self.mass,fits_cy_tmp
           elif (len(r) >= 3):
#              fits_cy_tmp = optimize.leastsq(residual_cy_L,[0.,0.,0.,0.,0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]
              fits_cy_tmp = optimize.leastsq(residual_cy1,[0.,0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]

#2016-10-11
#              if (fits_cy_tmp[0] < 0.):
#                 fits_cy_tmp=fits_cy_tmp*0. #important!!!

              resi_cy_tmp=np.max(residual_cy1(fits_cy_tmp,logl[r],menv_cy[r],logt[r]))
              cy_i=cy_i+1
              fits_cy= np.vstack([fits_cy,[fits_cy_tmp[0],fits_cy_tmp[1],fits_cy_tmp[2],0.,0.]]) #[fits_cy,fits_cy_tmp] #np.append(fits_cy,fits_cy_tmp)
              resi_cy=np.append(resi_cy,resi_cy_tmp)

#              fits_cy = np.vstack([fits_cy,np.array([0.,0.,0.,0.,0.,0.])])
#              resi_cy = np.append(resi_cy,np.array([0.]))
              minL_cy = np.append(minL_cy,np.min(logl[r]))
              maxL_cy = np.append(maxL_cy,np.max(logl[r]))
              minMenv_cy = np.append(minMenv_cy,np.min(menv_cy[r]))
              maxMenv_cy = np.append(maxMenv_cy,np.max(menv_cy[r]))
           elif (len(r) == 2):
#              fits_cy_tmp = optimize.leastsq(residual_cy_L,[0.,0.,0.,0.,0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]
              fits_cy_tmp = optimize.leastsq(residual_cy2,[0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]

#2016-10-11
#              if (fits_cy_tmp[0] < 0.):
#                 fits_cy_tmp=fits_cy_tmp*0. #important!!!

              resi_cy_tmp=np.max(residual_cy2(fits_cy_tmp,logl[r],menv_cy[r],logt[r]))
              cy_i=cy_i+1
              fits_cy= np.vstack([fits_cy,[fits_cy_tmp[0],fits_cy_tmp[1],0.,0.,0.]]) #[fits_cy,fits_cy_tmp] #np.append(fits_cy,fits_cy_tmp)
              resi_cy=np.append(resi_cy,resi_cy_tmp)

              if ( (abs(fits_cy_tmp[0]) < 1E-5) & (abs(fits_cy_tmp[1]) < 1E-5) ):
                 fits_cy_tmp = optimize.leastsq(residual_cy3,[0.,0.],args=(logl[r],menv_cy[r],logt[r]))[0]
                 resi_cy_tmp=np.max(residual_cy3(fits_cy_tmp,logl[r],menv_cy[r],logt[r]))
                 fits_cy= np.vstack([fits_cy,[fits_cy_tmp[0],0.,fits_cy_tmp[1],0.,0.]])
                 resi_cy=np.append(resi_cy,resi_cy_tmp)


#              fits_cy = np.vstack([fits_cy,np.array([0.,0.,0.,0.,0.,0.])])
#              resi_cy = np.append(resi_cy,np.array([0.]))
              minL_cy = np.append(minL_cy,np.min(logl[r]))
              maxL_cy = np.append(maxL_cy,np.max(logl[r]))
              minMenv_cy = np.append(minMenv_cy,np.min(menv_cy[r]))
              maxMenv_cy = np.append(maxMenv_cy,np.max(menv_cy[r]))
           else:
              fits_cy = np.vstack([fits_cy,np.array([0.,0.,0.,0.,0.])])
              resi_cy = np.append(resi_cy,np.array([0.]))
              minL_cy = np.append(minL_cy,np.array([0.]))
              maxL_cy = np.append(maxL_cy,np.array([0.]))
              minMenv_cy = np.append(minMenv_cy,np.array([0.]))
              maxMenv_cy = np.append(maxMenv_cy,np.array([0.]))


        self.rising_cy = rising_cy
        self.fits_cy = fits_cy
        self.resi_cy = resi_cy
        self.minL_cy = minL_cy
        self.maxL_cy = maxL_cy
        self.minMenv_cy = minMenv_cy
        self.maxMenv_cy = maxMenv_cy
#        print self.fits_cy



#By testing on S_NOV13 and S_MAR16(Z=0.004 and 0.006) addpt is alwyas empty (Yang Chen 31/03/2016)
    def add_points_to_q_track(self):
        '''
        when to add an extra point for low masses
        if logt[qs+1] is hotter than logt[qs]
        and there is a point inbetween logt[qs] and logt[qs+1] that is cooler
        than logt[qs] add the coolest point.
        '''
        addpt = self.addpt
        qs = list(self.Qs)
        logt = self.data_array['T_star']
        tstep = self.data_array['step']
        status = self.data_array['status']
        Tqs = logt[qs]
        # need to use some unique array, not logt, since logt could repeat,
        # index would find the first one, not necessarily the correct one.
        Sqs = tstep[qs] - 1.  # steps start at 1, not zero
        # takes the sign of the difference in logt(qs)
        # if the sign of the difference is more than 0, we're going from cold to hot

        # finds where the logt goes from getting colder to hotter...
        ht, = np.nonzero(np.sign(np.diff(Tqs)) > 0)
        ht = np.append(ht, ht + 1)  # between the first and second
        Sqs_ht = Sqs[ht]
        # the indices between each hot point.
        t_mids = [map(int, tstep[int(Sqs_ht[i]): int(Sqs_ht[i + 1])])
                  for i in range(len(Sqs_ht) - 1)]
        Sqs_ht = Sqs_ht[: -1]
        for i in range(len(Sqs_ht) - 1):
            hot_inds = np.nonzero(logt[int(Sqs_ht[i])] > logt[t_mids[i]])[0]
            if len(hot_inds) > 0:
                # index of the min T of the hot index from above.
                addpt.append(list(logt).index(np.min(logt[[t_mids[i][hi]
                                                           for hi in hot_inds]])))

        if len(addpt) > 0:
            addpt = np.unique([a for a in addpt if status[a] == 7.])
        # hack: if there is more than one point, take the most evolved.
        if len(addpt) > 1:
            addpt = [np.max(addpt)]
        # update Qs with added pts.
        self.Qs = np.sort(np.concatenate((addpt, qs)))
        # update mins to take the same point as Qs.
        self.mins = list(np.sort(np.concatenate((addpt, self.mins))))
        self.addpt = addpt



    def check_ntp(self):
        '''sets self.bad_track = True if only one thermal pulse.'''
        ntp = self.data_array['NTP']
        if ntp.size <= 1:
            logger.error('no tracks! {}'.format(self.name))
            self.bad_track = True

    def fix_phi(self):
        '''The first line in the agb track is 1. This isn't a quiescent stage.'''
        self.data_array['PHI_TP'][0] = -1.

    def m_cstars(self, mdot_cond=-5, logl_cond=3.3):
        '''
        adds mstar and cstar attribute of indices that are true for:
        mstar: co <=1 logl >= 3.3 mdot <= -5
        cstar: co >=1 mdot <= -5
        (by default) adjust mdot with mdot_cond and logl with logl_cond.
        '''
        data = self.data_array

        self.mstar, = np.nonzero((data['CO'] <= 1) &
                                 (data['L_star'] >= logl_cond) &
                                 (data['dMdt'] <= mdot_cond))
                                 
                                 
        self.cstar, = np.nonzero((data['CO'] >= 1) &
                                 (data['dMdt'] <= mdot_cond))

    def tauc_m(self):
        '''lifetimes of c and m stars'''
        try:
            tauc = np.sum(self.data_array['dt'][self.cstar]) / 1e6
        except IndexError:
            tauc = 0.
            logger.warning('no tauc')
        try:
            taum = np.sum(self.data_array['dt'][self.mstar]) / 1e6
        except IndexError:
            taum = 0.
            logger.warning('no taum')
        self.taum = taum
        self.tauc = tauc

    def get_TP_inds(self):
        '''find the thermal pulsations of each file'''
        self.TPs = []
        if self.bad_track:
            return
        ntp = self.data_array['NTP']
        un, iTPs = np.unique(ntp, return_index=True)
        if un.size == 1:
            logger.warning('only one themal pulse.')
            self.TPs = un
        else:
            # The indices each TP is just filling values between the iTPs
            # and the final grid point
            iTPs = np.append(iTPs, len(ntp))
            self.TPs = [np.arange(iTPs[i], iTPs[i+1])
                        for i in range(len(iTPs) - 1)]

        if len(self.TPs) == 1:
#            logger.info('a good track should contain at least two pulses! check.')
            self.bad_track = True

    def get_quiescent_inds(self):
        '''
        The quiescent phase, Qs,  is the the max phase in each TP,
        i.e., closest to 1.
        '''
        status = self.data_array['status']  #Yang 2017-01-12 remove the last bad thermal pulse
        phi = self.data_array['PHI_TP']
        logl = self.data_array['L_star']
#        self.Qs = np.unique([TP[np.argmax(phi[TP])] for TP in self.TPs])  #Phil's original definition but one index shifted
#wrong        self.Qs = np.unique([TP[   np.where((phi[TP]) == np.max(phi[TP]))[0]   ] for TP in self.TPs])
#        self.Qs = np.unique([TP[-1] for TP in self.TPs]) #Yang 2016-10-12
        self.Qs = np.unique([TP[-1] for TP in self.TPs if status[TP[-1]] == 7]) #Yang 2017-01-12 remove the last bad thermal pulse
        self.mins = np.unique([TP[np.argmin(logl[TP])] for TP in self.TPs])


def get_numeric_data(filename):
    '''
    made to read all of Paola's tracks. It takes away her "lg" meaning log.
    Returns an AGBTracks object. If there is a problem reading the data, all
    data are passed as zeros.
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    line = lines[0]
    if len(lines) == 1:
        logger.warning('only one line in {}'.format(filename))
        return -1
    col_keys = line.replace('#', '').replace('lg', '').replace('*', 'star')
    col_keys = col_keys.strip().split()
    try:
        data = np.genfromtxt(filename, missing_values='************',
                             names=col_keys)
    except ValueError:
        logger.error('problem with', filename)
        data = np.zeros(len(col_keys))
    return AGBTracks(data, col_keys, filename)


def calc_c_o(row):
    """
    C or O excess
    if (C/O>1):
        excess = log10 [(YC/YH) - (YO/YH)] + 12
    if C/O<1:
        excess = log10 [(YO/YH) - (YC/YH)] + 12

    where YC = X(C12)/12 + X(C13)/13
          YO = X(O16)/16 + X(O17)/17 + X(O18)/18
          YH = XH/1.00794
    """
    yh = row['H'] / 1.00794
    yc = row['C12'] / 12. + row['C13'] / 13.
    yo = row['O16'] / 16. + row['O17'] / 17. + row['O18'] / 18.

    if row['CO'] > 1:
        excess = np.log10((yc / yh) - (yo / yh)) + 12.
    else:
        excess = np.log10((yo / yh) - (yc / yh)) + 12.

    return excess


def make_iso_file(track, isofile, isofile_cy, write_header=False):
    '''
    this only writes the quiescent lines and the first line.
    format of this file is:
    age : age in yr
    logl : logL
    logte : logTe
    mass : actual mass along track
    mcore : core mass
    per : period in days
    period mode : 1=first overtone, 0=fundamental mode
    mlr : mass loss rate in Msun/yr
    x_min : X
    y_min : Y
    X_C : X_C
    X_N : X_N
    X_O : X_O
    slope : dTe/dL
    x_min : Xm at log L min of (the following) TP
    y_min : Ym at log L min of (the following) TP
    X_Cm : X_C at log L min of (the following) TP
    X_Nm : X_N at log L min of (the following) TP
    X_Om : X_O at log L min of (the following) TP
    '''
    isofile.write('# age(yr) logL logTe m_act mcore period ip')
    isofile.write(' Mdot(Msun/yr) X Y X_C X_N X_O dlogTe/dlogL Xm Ym X_Cm X_Nm X_Om minL maxL minMenv maxMenv fits0 fits1 fits2 fits3 fits4\n')

    fmt = '%.4e %.4f %.4f %.5f %.5f %.4e %i %.4e %.6e %.6e %.6e %.6e %.6e %.4f %.6e %.6e %.6e %.6e %.6e %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f\n' #without residual
    fmt_cy = '%.4f %.4e %.4f %.4f %.5f %.5f %.4e %i %.4e %.6e %.6e %.6e %.6e %.6e %.4f %.6e %.6e %.6e %.6e %.6e %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.10f\n' #without residual

    if track.bad_track:
        if (track.n_eagb > 0):
            track.eagb()
            if False: isofile.write(' %.4f %i %i # %s \n' % (track.mass, 0, 0+track.n_eagb_out,track.firstname))
            else: isofile.write(' %.4f %i # %s \n' % (track.mass, 0,track.firstname))
            track.eagb(isofile=isofile)
        else:
            isofile.write(' %.4f %i # %s \n' % (track.mass, 0, track.firstname))
        return

    
    fits0_sec=track.fits_cy[1,0]
    fits1_sec=track.fits_cy[1,1]
    fits2_sec=track.fits_cy[1,2]
    fits3_sec=track.fits_cy[1,3]
    fits4_sec=track.fits_cy[1,4]

    # cull agb track to quiescent
    rows = track.Qs
    
    # min of each TP
    mins = track.data_array[track.mins]
    if len(rows) - len(mins) > 1:
        import pdb; pdb.set_trace()

    keys = track.key_dict.keys()
    vals = track.key_dict.values()
    col_keys = np.array(list(keys))[np.argsort(list(vals))]

    if (track.n_eagb > 0):
        track.eagb()
        if False: isofile.write(' %.4f %i %i # %s \n' % (track.mass, len(rows), len(rows)+track.n_eagb_out,track.firstname))
        else: isofile.write(' %.4f %i # %s \n' % (track.mass, len(rows), track.firstname))
        track.eagb(isofile=isofile)
    else:
        isofile.write(' %.4f %i # %s \n' % (track.mass, len(rows), track.firstname))


    
    fits_cy_previous=np.array([0.,0.,0.,0.,0.])
#    fits_cy_previous_pre=np.array([0.,0.,0.,0.,0.,0.])
    for i, r in enumerate(rows):
        slope = 999
        fits_cy_tmp=np.array([0.,0.,0.,0.,0.])
        minL_cy_tmp=np.array([0.])
        maxL_cy_tmp=np.array([0.])
        minMenv_cy_tmp=np.array([0.])
        maxMenv_cy_tmp=np.array([0.])
        resi_cy_tmp=np.array([0.])

        xcm = 999
        xnm = 999
        xom = 999
        iminh = 999
        iminy = 999
        row = track.data_array[r]

        period = row['P1']
        if row['Pmod'] == 0:
            period = row['P0']

        mdot = 10 ** (row['dMdt'])

        # CNO and excess are no longer used
        #CNO = np.sum([row[c] for c in cno])
        #excess = calc_c_o(row)
        xc = np.sum([row[c] for c in col_keys if c.startswith('C1')])
        xn = np.sum([row[c] for c in col_keys if c.startswith('N1')])
        xo = np.sum([row[c] for c in col_keys if c.startswith('O1')])

#        print 'cycy2:',i,r
#        print 'cycy12:',rows,row
        if r != rows[-1]:
            imin = mins[i]
            xcm = np.sum([imin[c] for c in col_keys if c.startswith('C1')])
            xnm = np.sum([imin[c] for c in col_keys if c.startswith('N1')])
            xom = np.sum([imin[c] for c in col_keys if c.startswith('O1')])
            iminh = imin['H']
            iminy = imin['Y']
            try:
                slope = 1. / track.slopes[list(rows).index(r)]
            except:
                logger.error('bad slope: {}, row: {}'.format(track.firstname, i))

        if r != rows[0]:
            try:
                fits_cy_tmp=track.fits_cy[list(rows).index(r)]
#                if (i !=0 ):
#                   fits_cy_previous0=fits_cy_tmp
                minL_cy_tmp=track.minL_cy[list(rows).index(r)]
                maxL_cy_tmp=track.maxL_cy[list(rows).index(r)]
                minMenv_cy_tmp=track.minMenv_cy[list(rows).index(r)]
                maxMenv_cy_tmp=track.maxMenv_cy[list(rows).index(r)]
                resi_cy_tmp=track.resi_cy[list(rows).index(r)]
            except:
                logger.error('bad thermal cycle: {}, row: {}'.format(track.firstname, i))

        try:
            if (i == 0):
               age0=row['ageyr']
               fits_cy_tmp[0]=fits0_sec #fits0_med #(fits0_med+fits_cy_tmp[0])/2.
               fits_cy_tmp[1]=fits1_sec #fits1_med #(fits1_med+fits_cy_tmp[1])/2. #fits1_med
               fits_cy_tmp[2]=fits2_sec #fits2_med #(fits2_med+fits_cy_tmp[2])/2. #fits2_med
               fits_cy_tmp[3]=fits3_sec #fits0_med #(fits0_med+fits_cy_tmp[0])/2.
               fits_cy_tmp[4]=fits4_sec #fits1_med #(fits1_med+fits_cy_tmp[1])/2. #fits1_med
            else:
               if ((abs(fits_cy_tmp[0]) < 1E-5) & (abs(fits_cy_tmp[1]) < 1E-5) & (abs(fits_cy_tmp[2]) < 1E-5) & (abs(fits_cy_tmp[3]) < 1E-5) & (abs(fits_cy_tmp[4]) < 1E-5)): # or fits_cy_tmp[0] > 5.):
                  fits_cy_tmp=fits_cy_previous #track.fits_cy[i-1,:] 

#2016-10-11
#               if ((i == len(rows)-1) & (fits_cy_tmp[0] > fits0_thresh_cy)): # or fits_cy_tmp[0] > 5.):
#                  fits_cy_tmp=fits_cy_previous #track.fits_cy[i-1,:] 


            fits_cy_previous=fits_cy_tmp


            isofile.write(fmt % (row['ageyr']-age0, row['L_star'], row['T_star'],
                                 row['M_star'], row['M_c'], period, row['Pmod'],
                                 mdot, row['H'], row['Y'], xc, xn, xo, slope,
                                 iminh, iminy, xcm, xnm, xom, #1.,2.,3.,4.,5.))
                                 minL_cy_tmp, maxL_cy_tmp,
                                 minMenv_cy_tmp, maxMenv_cy_tmp,
                                 fits_cy_tmp[0],fits_cy_tmp[1], 
                                 fits_cy_tmp[2], fits_cy_tmp[3],
                                 fits_cy_tmp[4]) #, fits_cy_tmp[5]) #,
                                 #resi_cy_tmp) with no residual
                         )

            isofile_cy.write(fmt_cy % (track.mass, row['ageyr']-age0, row['L_star'], row['T_star'],
                                 row['M_star'], row['M_c'], period, row['Pmod'],
                                 mdot, row['H'], row['Y'], xc, xn, xo, slope,
                                 iminh, iminy, xcm, xnm, xom, #1.,2.,3.,4.,5.))
                                 minL_cy_tmp, maxL_cy_tmp,
                                 minMenv_cy_tmp, maxMenv_cy_tmp,
                                 fits_cy_tmp[0],fits_cy_tmp[1], 
                                 fits_cy_tmp[2], fits_cy_tmp[3],
                                 fits_cy_tmp[4], resi_cy_tmp) #, fits_cy_tmp[5]) #,
                                 #resi_cy_tmp) with no residual
                            )

        except IndexError:
            logger.error('this row: {}'.format(list(rows).index(r)))
            logger.error('row length: {} slope array length {}'.format(len(rows), len(track.slopes)))
            logger.error('slope reciprical: {}'.format(1. / slope[list(rows).index(r)]))
    return






def make_met_file(tracce, Zs, Ys, isofiles):
    with open(tracce, 'w') as t:
        t.write(' %i\n' % len(isofiles))
        [t.write(' %.4f\t%.3f\t%s\n' % (Zs[i], Ys[i], isofiles[i]))
         for i in np.argsort(Zs)]
    logger.info('wrote {}'.format(tracce))
    return


def get_files(src, search_string):
    '''
    returns a list of files, similar to ls src/search_string
    '''
    if not src.endswith('/'):
        src += '/'
    try:
        files = glob.glob1(src, search_string)
    except IndexError:
        logging.error('Can''t find %s in %s' % (search_string, src))
        sys.exit(2)
    files = [os.path.join(src, f)
             for f in files if ensure_file(os.path.join(src, f), mad=False)]
    return files


def ensure_file(f, mad=True):
    '''
    Parameters
    ----------
    f : string
        if f is not a file will log warning.
    mad : bool [True]
        if mad is True, will exit if f is not a file
    '''
    test = os.path.isfile(f)
    if test is False:
        logging.warning('there is no file', f)
        if mad:
            sys.exit(2)
    return test




def ensure_dir(f):
    '''
    will make all dirs necessary for input to be an existing directory.
    if input does not end with '/' it will add it, and then make a directory.
    '''
    if not f.endswith('/'):
        f += '/'

    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)
        logging.info('made dirs: {}'.format(d))


def savetxt(filename, data, fmt='%.4f', header=None):
    '''
    np.savetxt wrapper that adds header. Some versions of savetxt
    already allow this...
    '''
    with open(filename, 'w') as f:
        if header is not None:
            f.write(header)
        np.savetxt(f, data, fmt=fmt)
    logger.info('wrote {}'.format(filename))


def is_numeric(lit):
    """
    value of numeric: literal, string, int, float, hex, binary
    From http://rosettacode.org/wiki/Determine_if_a_string_is_numeric#Python
    """
    # Empty String
    if len(lit) <= 0:
        return lit
    # Handle '0'
    if lit == '0':
        return 0
    # Hex/Binary
    if len(lit) > 1:  # sometimes just '-' means no data...
        litneg = lit[1:] if lit[0] == '-' else lit
        if litneg[0] == '0':
            if litneg[1] in 'xX':
                return int(lit, 16)
            elif litneg[1] in 'bB':
                return int(lit, 2)
            else:
                try:
                    return int(lit, 8)
                except ValueError:
                    pass
    # Int/Float/Complex
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass
    try:
        return complex(lit)
    except ValueError:
        pass
    return lit


def setup_multiplot(nplots, xlabel=None, ylabel=None, title=None,
                    subplots_kwargs={}):
    '''
    fyi subplots args:
        nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
        subplot_kw=None, **fig_kw
    '''
    nx = np.round(np.sqrt(nplots))
    nextra = nplots - nx ** 2
    ny = nx
    if nextra > 0:
        ny += 1
    nx = int(nx)
    ny = int(ny)

    (fig, axs) = plt.subplots(nrows=nx, ncols=ny, **subplots_kwargs)
    if ylabel is not None:
        axs[0][0].annotate(ylabel, fontsize=45, xy=(0.04, 0.5),
                         xycoords='figure fraction', va='center',
                         rotation='vertical')
    if xlabel is not None:
        axs[0][0].annotate(xlabel, fontsize=45, xy=(0.5, 0.04),
                         xycoords='figure fraction', va='center')
    if title is not None:
        axs[0][0].annotate(title, fontsize=45, xy=(0.5, 1. - 0.04),
                         xycoords='figure fraction', va='center')

    return (fig, axs)


def discrete_colors(ncolors, colormap='gist_rainbow'):
    colors = []
    cmap = cm.get_cmap(colormap)
    # color will now be an RGBA tuple
    colors = [(cmap(1. * i / ncolors)) for i in range(ncolors)]
    return colors


def two_panel_plot_vert(fign=2):
    fig = plt.figure(fign, figsize=(8, 8))
    left, width = 0.13, 0.83
    bottom, height = 0.1, 0.41
    dh = 0.03

    axis1 = [left, bottom, width, height]
    axis2 = [left, (bottom + height + dh), width, height]

    ax1 = plt.axes(axis1)
    ax2 = plt.axes(axis2)
    ax2.xaxis.set_major_formatter(nullfmt)
    return ax1, ax2





def diag_plots_cy(track, home_dir=None,agb_mix='CAF09', set_name='S_035', diagnostic_dir=None, plot_slopes=False):
    os.chdir(home_dir)
    ext = '.png'
#    logt_lim = (3.75, 3.35)
#    logl_lim = (2.4, 4.8)
#    lage_lim = (1., 1e7)
#    co_lim = (0, 5)

    logl = track.data_array['L_star']
    logt = track.data_array['T_star']
    logl_lim = (logl.min()-0.05,logl.max()+0.05)
    logt_lim = (logt.max()+0.01,logt.min()-0.01)

    addpt = track.addpt
    Qs = list(track.Qs)
    # HRD
    fig = plt.figure()
    ax = plt.axes()
    plotpath = os.path.join(diagnostic_dir, 'HRD/')
    ensure_dir(plotpath)
    ax.annotate(r'$%s$' % agb_mix.replace('_', '\ '), xy=(0.61,0.185), xycoords='figure fraction', xytext=(0,0), textcoords='offset points')
    ax.annotate(r'$%s$' % set_name.replace('_', '\ '), xy=(0.61,0.15), xycoords='figure fraction', xytext=(0,0), textcoords='offset points')
    ax.annotate(r'$M=%.2f$' % track.mass, xy=(0.61,0.115), xycoords='figure fraction', xytext=(0,0), textcoords='offset points')
    ax.plot(logt, logl, color='black',lw=0.25)


    hrd_slopes_cy(track, ax)
    fit_teff_check_cy(track, ax)
#    ax.set_xlim(logt_lim)
#    ax.set_ylim(logl_lim)
    ax.set_xlim(ax.get_xlim()[::-1])
    ax.set_xlabel(r'$\log\ Te$')
    ax.set_ylabel(r'$\log\ L_{\odot}$')
    fname = os.path.split(track.name)[1].replace('.dat', '')
    fig_name = os.path.join(plotpath, '_'.join(('diag', fname)))
    plt.savefig('%s%s' % (fig_name, ext))
    plt.close()








def hrd_slopes_cy(track, ax):  #just plotting
#    print 'running hrd_slopes_cy'
    logl = track.data_array['L_star']
    logt = track.data_array['T_star']
#    logmenv_cy=np.log10(track.data_array['M_star']-track.data_array['M_c'])
    menv_cy=track.data_array['M_star']-track.data_array['M_c']
#    x = [np.linspace(r1, r2) for r1,r2 in track.minL_cy,track.maxL_cy]
#    y = [np.linspace(r1, r2) for r1,r2 in track.minMenv_cy,track.maxMenv_cy]

#    [ax.scatter(np.sort(logt[r]), logl[r][np.argsort(logt[r])], color='red', s=2.5)
#     for r in track.rising_cy if len(r) > valid_points_cy]
    [ax.scatter(np.sort(logt[r]), logl[r][np.argsort(logt[r])], color='red', s=2.5)
     for r in track.rising_cy  if len(r) > 0]

    qs = list(track.Qs)
    i=0
#    i_valid=0
    for r in track.rising_cy:


     if len(r) > 0:
       if (len(r) >= 2):
          i=i+1
#          i_valid=i_valid+1
          x=logl[r]
          y=menv_cy[r]
#          z=func_cy15(track.fits_cy[i],x,y) #+logt[qs[i]]
#          ax.scatter(z,x, color='blue', s=20.,alpha=0.5, facecolors='none')
          if ((abs(track.fits_cy[i][0]) < 1E-5) & (abs(track.fits_cy[i][1]) < 1E-5) & (abs(track.fits_cy[i][2]) < 1E-5) & (abs(track.fits_cy[i][3]) < 1E-5) & (abs(track.fits_cy[i][4]) < 1E-5)):
             logger.info('#########################################')
             logger.info(track.fits_cy[i][0])
             z=func_cy15(track.fits_cy[i-1],x,y) #+logt[qs[i]]
             deltaz=func_cy(track.fits_cy[i-1],logl[qs[i]],menv_cy[qs[i]])-logt[qs[i]]
#             ax.scatter(z-deltaz,x, color='green', s=20.,alpha=0.5, facecolors='none')
             ax.scatter(z,x, color='green', s=20.,alpha=0.5, facecolors='none')
          else:
             z=func_cy15(track.fits_cy[i],x,y) #+logt[qs[i]]
             ax.scatter(z,x, color='blue', s=20.,alpha=0.5, facecolors='none')
       else:
          i=i+1
          x=logl[r]
          y=menv_cy[r]
          z=func_cy15(track.fits_cy[i],x,y) #+logt[qs[i]]
          logger.info(x) #np.float(x),np.float(y),np.float(z),np.float(logt[qs[i]]))
          logger.info(y)
          logger.info(z)
          logger.info(logt[qs[i]])
          deltaz=func_cy15(track.fits_cy[i],logl[qs[i]],menv_cy[qs[i]])-logt[qs[i]]
          ax.scatter(z-deltaz,x, color='green', s=35.,alpha=0.5, facecolors='none')

       ax.scatter(logt[qs[i]], logl[qs[i]], color='cyan', s=50., alpha=0.5, facecolors='none')



     continue
     if len(r) > 0:
       if (len(r) >= valid_points_cy):
          i=i+1
          i_valid=i_valid+1
          x=logl[r]
          y=menv_cy[r]
#          print 'cycy5',track.fits_cy[i] 
#          print x,y
          z=func_cy15(track.fits_cy[i],x,y) #+logt[qs[i]]
#          print 'cycy7',x,y,z
          ax.scatter(z,x, color='blue', s=20.,alpha=0.5, facecolors='none')
       elif (len(r) > 2):
          i=i+1
          x=logl[r]
          y=menv_cy[r]
          z=func_cy(track.fits_cy[i],x,y) #+logt[qs[i]]
          ax.scatter(z,x, color='blue', s=20.,alpha=0.5, facecolors='none')
       elif (len(r) == 2):
          i=i+1
          x=logl[r]
          y=menv_cy[r]
          z=func_cy0(track.fits_cy[i],x,y) #+logt[qs[i]]
          ax.scatter(z,x, color='blue', s=20.,alpha=0.5, facecolors='none')
       else:
          i=i+1
          x=logl[r]
          y=menv_cy[r]
#          z=func_cy(track.fits_cy[i_valid],x,y) #+logt[qs[i]]
          z=func_cy(track.fits_cy[i],x,y) #+logt[qs[i]]
#          deltaz=func_cy(track.fits_cy[i_valid],logl[qs[i]],menv_cy[qs[i]])-logt[qs[i]]
          deltaz=func_cy(track.fits_cy[i],logl[qs[i]],menv_cy[qs[i]])-logt[qs[i]]
#          logger.info(deltaz)
          ax.scatter(z-deltaz,x, color='green', s=35.,alpha=0.5, facecolors='none')

       ax.scatter(logt[qs[i]], logl[qs[i]], color='cyan', s=50., alpha=0.5, facecolors='none')

#       [ax.scatter(logt[q], logl[q], 'o', color='black', alpha=0.5, facecolors='none') for q in track.mins]





def fit_teff_check_cy(track, ax):
    logl = track.data_array['L_star']
    logt = track.data_array['T_star']
    menv_cy=track.data_array['M_star']-track.data_array['M_c']

    i=0
    for r in track.rising_cy:
       if len(r) > valid_points_cy:
          i=i+1
          x=logl[r]
          y=menv_cy[r]
          z=func_cy(track.fits_cy[i],x,y)
#          ax.scatter(z,x, color='blue', s=20.,alpha=0.5, facecolors='none')
          diff=z-logt[r]
#          ax.scatter(x,diff, color='blue', s=20.,alpha=0.5, facecolors='none')
          print("median, mean and std of (logTe_fit-logTe_mod):",np.median(diff),diff.mean(), diff.std())
          print("max of (logTe_fit-logTe_mod):",np.max(diff))
 


def plot_ifmr(imfrfile, ax=None, zs=None, data_mi=None, data_mf=None,
              data_mierr=None, data_mferr=None):
    mi, mf, z = np.loadtxt(imfrfile, unpack=True)
    zinds, unz = get_unique_inds(z)
    if zs is None:
        zs = np.unique(z)
    cols = discrete_colors(len(zs))
    cols = cols * len(zinds)
    if ax is None:
        fig, ax = plt.subplots()
#    [ax.plot(mi[zinds[i]], mf[zinds[i]], color=cols[i], label=str(z[unz[i]]))
#        for i in range(len(unz)) if z[unz[i]] in zs]
#    [ax.plot(mi[zinds[i]], mf[zinds[i]], 'o', ms=4, color=cols[i],
#              mec='white', alpha=0.5) for i in range(len(unz)) if z[unz[i]] in zs]
    if (isinstance(unz,list)):
        [ax.plot(mi[zinds[i]], mf[zinds[i]], color=cols[i], label=str(z[unz[i]]))
            for i in range(len(unz)) if z[unz[i]] in zs]
        [ax.plot(mi[zinds[i]], mf[zinds[i]], 'o', ms=4, color=cols[i],
            mec='white', alpha=0.5) for i in range(len(unz)) if z[unz[i]] in zs]
    else:
        [ax.plot(mi[zinds[i]], mf[zinds[i]], color=cols[i], label=str(z[unz]))
            for i in range(1) if z[unz] in zs]
        [ax.plot(mi[zinds[i]], mf[zinds[i]], 'o', ms=4, color=cols[i],
              mec='white', alpha=0.5) for i in range(1) if z[unz] in zs]


    if data_mf is not None:
        if data_mierr is not None:
            from matplotlib.patches import Rectangle
            bottom_left = (data_mi - data_mierr/2., data_mf - data_mferr/2.)
            width = data_mierr
            height = data_mferr
            rect = Rectangle(bottom_left, width, height, color='black', alpha=.25)
            ax.add_patch(rect)
    ax.legend(loc=2, frameon=False)
    ax.set_xlabel(r'$M_i/M_{\odot}$', fontsize=20)
    ax.set_ylabel(r'$M_f/M_{\odot}$', fontsize=20)
    plt.savefig(imfrfile.replace('dat', 'png'))
    #plt.close()
    return ax


def plot_cluster_test(lifetimesfile):
    def cluster_data():
        cmass = np.array([5.9, 4.75, 3.85, 3.17, 2.66, 2.17, 1.66, 1.18, 0.82])
        ctauc = np.array([0.032,  0., 0., 0., 2.8, 2.59, 1.57, 0., 0.])
        ecp = np.array([0.075, 0.5, 0.07, 0.9, 2.21, 0.67, 0.71, 1.49, 0.66])
        ecm = np.array([0.026, 0., 0., 0., 1.34, 0.55, 0.51, 0., 0.])
        ctaum = np.array([0.26, 2.19, 0.19, 0.79, 2.8, 3.77, 1.74, 2.62, 0.66])
        emp = np.array([0.13, 1.47, 0.18, 1.81, 2.21, 0.79, 0.74, 3.44, 0.])
        emm = np.array([0.090, 0.940, 0.100, 0.660, 1.340, 0.660, 0.540, 1.690,
                    100.000])
        return cmass, ctauc, ecp, ecm, ctaum, emp, emm

    z, mass, tauc, taum = np.loadtxt(lifetimesfile, unpack=True)
    zinds, unz = get_unique_inds(z)
    cols = discrete_colors(len(zinds))

    ax1, ax2 = two_panel_plot_vert(fign=3)
    ax2.set_ylabel(r'$\tau_M\ (\rm{Myr})$', fontsize=20)
    ax1.set_ylabel(r'$\tau_C\ (\rm{Myr})$', fontsize=20)
    ax1.set_xlabel(r'$M_{TO}\ (\rm{M}_\odot)$', fontsize=20)

    cmass, ctauc, ecp, ecm, ctaum, emp, emm = cluster_data()
    ax1.errorbar(cmass, ctauc, yerr=[ecm, ecp], fmt='o', color='black',
                 label='LMC')
    ax2.errorbar(cmass, ctaum, yerr=[emm, emp], fmt='o', color='black')

#    for i in range(len(unz)):
#        ax1.plot(mass[zinds[i]], tauc[zinds[i]], color=cols[i],
#                 label=str(z[unz[i]]))
#        ax2.plot(mass[zinds[i]], taum[zinds[i]], color=cols[i])
    if (isinstance(unz,list)):
       for i in range(len(unz)):
           ax1.plot(mass[zinds[i]], tauc[zinds[i]], color=cols[i],
                    label=str(z[unz[i]]))
           ax2.plot(mass[zinds[i]], taum[zinds[i]], color=cols[i])
    else:
       for i in range(1):
           ax1.plot(mass[zinds[i]], tauc[zinds[i]], color=cols[i],
                    label=str(z[unz]))
           ax2.plot(mass[zinds[i]], taum[zinds[i]], color=cols[i])

    [ax.set_ylim(0, ax.get_ylim()[1]) for ax in [ax1, ax2]]
    ax1.legend(loc='best', ncol=2, frameon=False, numpoints=1)
    plt.savefig(lifetimesfile.replace('dat', 'png'))
    logger.info('wrote {}'.format(lifetimesfile.replace('dat', 'png')))
    plt.close()
    return


def get_unique_inds(ntp):
    un = np.unique(ntp)
    if un.size == 1:
        logger.warning('only one themal pulse/one value.')
        return un, list(ntp).index(un)  #un:the NTP, list(ntp).index(un):the index of the first point with NTP==un
    else:
        # this is the first step in each TP.
        iTPs = [list(ntp).index(u) for u in un]
        # The indices of each TP.
        TPs = [np.arange(iTPs[i], iTPs[i + 1]) for i in range(len(iTPs) - 1)]
        # don't forget the last one.
        TPs.append(np.arange(iTPs[-1], len(ntp)))
        return TPs, iTPs  #TPs:the NTPs, iTPs:the indexes of the first point for each NTP

#if (len(sys.argv) == 2):
#    colibri2trilegal(sys.argv[1])

    
