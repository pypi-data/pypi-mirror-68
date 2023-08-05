""" Utilities for converting COLIBRI tracks into TRILEGAL tracks """
import glob, logging, os, sys, re

import matplotlib.pyplot as plt
import numpy as np

from ast import literal_eval
from matplotlib import cm, rcParams
#from matplotlib.ticker import NullFormatter, MultipleLocator, ScalarFormatter, MaxNLocator

import scipy
import scipy.optimize as optimize



#############################
def func_cy5(par,x,y):
   z=par[0] + par[1]*x + par[2]*y + par[3]*x*x + par[4]*y*y
   return z

def func_cy3(par,x,y):
   z=par[0] + par[1]*x + par[2]*y # + 0*par[3] + 0*par[4]
   return z

def func_cy3_0(par,x,y):
   z=par[0] + par[1]*x + par[2]*y
   return z

def func_cy2x(par, x, y):
   z=par[0] + par[1]*x #+ 0*par[2] + 0*par[3] + 0*par[4]
   return z

def func_cy2y(par,x,y):
   z=par[0] +  + par[1]*y #par[1]*0.*x + par[2]*y #+ 0*par[3] + 0*par[4]
   return z

def resi_func5(par,x,y,z):
   return (z-func_cy5(par,x,y))**2

def resi_func3(par,x,y,z):
   return (z-func_cy3(par,x,y))**2

def resi_func2x(par,x,y,z):
   return (z-func_cy2x(par,x,y))**2

def resi_func2y(par,x,y,z):
   return (z-func_cy2y(par,x,y))**2
#############################

def colibri2trilegal(input_file):
   #if (len(sys.argv) != 2):
   #    print('Usage: colibri2trilegal parfile')
   #    exit(2)
   str_search='agb_*.dat'
   str_search_re='agb\_([0-9]*\.[0-9]*)\_.*'
   iso_hdr='# age(yr) logL logTe m_act mcore period ip Mdot(Msun/yr) X Y X_C X_N X_O \
   dlogTe/dlogL Xm Ym X_Cm X_Nm X_Om minL maxL minMenv maxMenv fits0 fits1 fits2 fits3 fits4'
   N_fit=5
   fmt0='%.4e %.4f %.4f %.5f %.5f %.4e %i %.4e'+' %.6e'*5
   fmt1=' %.4f %.6e %.6e %.6e %.6e %.6e'
   fmt2=' %.5f'*9+'\n'
    
   #with open(sys.argv[1]) as f:
   with open(input_file) as f:
       for line0 in f.readlines():
           line=line0.strip().split()
           if (len(line)<1 or '#' in line[0]): continue
           if (line[0]=='agbtrack_dir'): agbtrack_dir='./colibri' #line[1]
           elif (line[0]=='agb_mix'): agb_mix=line[1]
           elif (line[0]=='set_name'): set_name=line[1]
           elif (line[0]=='isotrack_dir'): isotrack_dir=line[1]
    
   indir=os.path.join(agbtrack_dir,agb_mix,set_name)
   outdir=os.path.join(isotrack_dir,agb_mix,set_name)
   metal_dirs=[m for m in os.listdir(indir) if os.path.isdir(os.path.join(indir,m)) and 'Z' in m]
   Zs=[re.search('Z(0\.0[0-9]*)',m).group(1) for m in metal_dirs]
   Zs_f=[float(m) for m in Zs]
   Ys=[re.search('Y(0\.[0-9]*)',m).group(1) for m in metal_dirs]
   (Zs,Ys,metal_dirs)=zip(*[(m,n,l) for (m_f,m,n,l) in sorted(zip(Zs_f,Zs,Ys,metal_dirs))])
   #print'Zs:',Zs


   tracce_fp=open(os.path.join(isotrack_dir,'tracce_'+agb_mix+'_'+set_name+'.dat'),'w')
   tracce_fp.write(str(len(Zs))+'\n')
   #Loop over Zs
   for Z,Y,metal_dir in zip(Zs,Ys,metal_dirs):
       isos,tracks=[],[]
       tracks_dir=os.path.join(indir,metal_dir)
       print(tracks_dir)
       track_files=glob.glob1(tracks_dir,str_search)
       #sort files
       track_masses=[re.search(str_search_re,m).group(1) for m in track_files]
       track_masses_f=[float(m) for m in track_masses]
       (track_masses,track_files)=zip(*[(m,n) for (l,m,n) in sorted(zip(track_masses_f,track_masses,track_files))])
       print('track masses:',track_masses)
       track_files=track_files[0:] #for test, comment out after test
       track_fp=open(os.path.join(isotrack_dir,'Z'+Z+'_'+agb_mix+'_'+set_name+'.dat'),'w')
       #Loop over tracks of the same Z
       for track_file in track_files:
           print(os.path.join(indir,metal_dir,track_file))
           with open(os.path.join(indir,metal_dir,track_file)) as f:
               hdr=f.readline().replace('#','').replace('lg', '').replace('*', 'star').replace('/','_').split()
               #dtyp=["F"] #["S100"]*len(hdr)
               #track0=np.genfromtxt(os.path.join(indir,metal_dir,track_file),skip_header=1,names=hdr,dtype=dtyp)
           track0=np.genfromtxt(os.path.join(indir,metal_dir,track_file),skip_header=1,names=hdr)
           id7,=np.where( (track0['status'] == 7.) & (track0['PHI_TP'] > 0.)\
                          & (track0['PHI_TP'] < 1.) ) #[0]
           id_phil,=np.where( (track0['status'] == 7) & (track0['PHI_TP'] > 0.2)\
                             & (track0['PHI_TP'] < 0.4) ) #[0] #Phil was taking 0.2<phi<0.4.
           #print 'len of id7:',len(id7)
           if (len(id7)==0): #totally no TPAGB
               isos.append([['-1']])
               continue
           track_tmp=track0[id7]
           #print track_tmp
           track_tmp_phil=track0[id_phil]
           track0=track0[id7[0]:] #cut the EAGB
           track_first=track_tmp[0] #the first TPAGB point is always labelled as '7' and PHI_IP==1.0.
                                    #It will be printed out in the isotrack file
           track_tmp=track_tmp[1:]
           #group tracks into pulses
           NTP_u=np.array(list(set(track_tmp['NTP'])))
           NTP_u.sort()
           NTP_u=NTP_u #unique and sorted
           track7=[]
           for m in NTP_u:
               #print 'm:',m
               #print track_tmp['NTP']
               track7.append(track_tmp[(np.where(np.array(track_tmp['NTP']) == m))[0]])
               #print track7
           #print "track7:",track7
           track7_phil=[]
           for m in NTP_u:
               track7_phil.append(track_tmp_phil[(np.where(np.array(track_tmp_phil['NTP']) == m))[0]])
           #print [(np.where(np.array(track_tmp['NTP']) == m))[0] for m in NTP_u]
           #track.append(track_tmp[[(np.where(np.array(track_tmp['NTP']) == m))[0] for m in NTP_u]])
           #print track[0]['NTP']
           #get Qs
           Qs=[m[-1] for m in track7]
           Qs.insert(0,track_first) #now remember that the first TPAGB point is inserted
           #print Qs[0]['NTP']
           #print Qs[-1]['NTP']
        
           iso=[]#; fits=[]; resi=[]; minL=[]; maxL=[]; minMenv=[]; maxMenv=[]
           #prop1=[]; prop2=[]; prop2=[]
           print("len(NTP_u):",len(NTP_u))

        
           #Loop over each TP
           for itp in np.arange(len(NTP_u)+1):
               row=Qs[itp]
               if row['Pmod']==0. : period=row['P0']
               else: period=row['P1']
   #            prop0=(fmt0 % ( row['age_yr'], row['L_star'], row['T_star'],\
   #                            row['M_star'], row['M_c'], period, row['Pmod'],\
   #                            10.**(row['dM_dt']), 1.-row['Y']-row['Z'], row['Y'],\
   #                            row['C12'], row['N14'], row['O16'] ))
               #print row['age_yr']+1
               prop0=[row['age_yr'], row['L_star'], row['T_star'],\
                               row['M_star'], row['M_c'], period, row['Pmod'],\
                               10.**(row['dM_dt']), 1.-row['Y']-row['Z'], row['Y'],\
                               row['C12'], row['N14'], row['O16']]
            

               #fiting teff
               if (itp == len(NTP_u) or len(track7[itp]['M_star'])-1 < 2):
                   fits=[0.]*5; resi=0.; minL=0.; maxL=0.; minMenv=0.; maxMenv=0.
               elif (len(track7[itp]['M_star'])-1==2):
                   Menv=track7[itp]['M_star']-track7[itp]['M_c']
                   fits=optimize.leastsq( resi_func2x,[0.]*2, \
                                          args=(track7[itp]['L_star'][1:],Menv[1:],track7[itp]['T_star'][1:]) )[0]
                   fits=list(fits)
                   fits.extend([0.,0.,0.])
                   if (abs(fits[0])<1E-5 and abs(fits[1])<1E-5):
                      fits_tmp=optimize.leastsq( resi_func2y,[0.]*5, \
                                             args=(track7[itp]['L_star'][1:],Menv[1:],track7[itp]['T_star'][1:]) )[0]
                      fits=[0.]*5
                      fits[0]=fits_tmp[0]
                      fits[2]=fits_tmp[1]
                   minL=np.min(track7[itp]['L_star'][1:])
                   maxL=np.max(track7[itp]['L_star'][1:])
                   minMenv=np.min(Menv[1:])
                   maxMenv=np.max(Menv[1:])
               elif (len(track7[itp]['M_star'])-1<=5):
                   Menv=track7[itp]['M_star']-track7[itp]['M_c']
                   print("Menv:",Menv[1:])
                   fits=optimize.leastsq( resi_func3,[0.]*3, \
                                           args=(track7[itp]['L_star'][1:],Menv[1:],track7[itp]['T_star'][1:]) )[0]
                   fits=list(fits)
                   fits.extend([0.,0.])
                   minL=np.min(track7[itp]['L_star'][1:])
                   maxL=np.max(track7[itp]['L_star'][1:])
                   minMenv=np.min(Menv[1:])
                   maxMenv=np.max(Menv[1:])
               else: #still use func3
                   Menv=track7[itp]['M_star']-track7[itp]['M_c']
                   fits=optimize.leastsq( resi_func3,[0.]*5, \
                                           args=(track7[itp]['L_star'][1:],Menv[1:],track7[itp]['T_star'][1:]) )[0]
                   minL=np.min(track7[itp]['L_star'][1:]) #the first '7' point in each pulse always show a jump
                   maxL=np.max(track7[itp]['L_star'][1:])
                   minMenv=np.min(Menv[1:])
                   maxMenv=np.max(Menv[1:])
               ###phil
               if (itp == len(NTP_u) or len(track7_phil[itp]['M_star']) < 2):
                   slope=999.; xm=999.; ym=999.; xcm=999.; xnm=999.; xom=999.
                          #check what I should do with the first point
                          #(track0[2]['lgT_star']-track0[2]['lgT_star'])/(track0[2]['lgL_star']-track0[2]['lgL_star']) #check
                          #iminh, iminy, xcm, xnm, xom will be updated later after consulting Leo.
                          #Are they necessary. How are they defined? 
               else:
                   order=1
                   slope=1./np.polyfit(track7_phil[itp]['T_star'], track7_phil[itp]['L_star'], order)[0]
                   iminL=np.argmin(track7_phil[itp]['L_star'])
                   xm=(1-track7_phil[itp]['Y']-track7_phil[itp]['Z'])[iminL]
                   ym=track7_phil[itp]['Y'][iminL]
                   xcm=track7_phil[itp]['C12'][iminL]
                   xnm=track7_phil[itp]['N14'][iminL]
                   xom=track7_phil[itp]['O16'][iminL]
                    
                    
               #prop1=(fmt1 % (slope, xm, ym, xcm, xnm, xom))
               prop1=[slope, xm, ym, xcm, xnm, xom]
               #prop2=(fmt2 % (minL, maxL, minMenv, maxMenv, fits[0],\
               #               fits[1], fits[2], fits[3], fits[4] ))
               prop2=[minL, maxL, minMenv, maxMenv, fits[0], fits[1], fits[2], fits[3], fits[4]]
               prop=prop0+prop1+prop2
               #print prop
               iso.append(prop)

            
           #push into isos
           #track_fp.write(track_file.split('_')[1]+' '+str(len(iso))+' # '+track_file+'\n')
           #if (len(iso) > 0):
           #    for i in range(len(iso)):
           #        track_fp.write(iso[i])
           isos.append(iso)

       for iso in isos:
           #print iso
           if (iso[0] != ['-1']):
              for itp in range(len(iso)):
                  iso[itp][0]=iso[itp][0]-iso[0][0]
        
       #make fake TPs
       #print isos
       for i in range(len(isos)-2,-1,-1):
           #print isos[i]
           if (isos[i][0] == ['-1']): #totally no TPAGB
               #print 'isos[i]:',isos[i]
               isos[i]=[isos[i+1][0][:]]*3
               #isos[i][0]=isos[i+1][0]
               #isos[i].append(isos[i][0])
               #isos[i].append(isos[i][0])
               #print 'i+1:',isos[i+1][0]
               #print 'i:',isos[i][0]
               #isos[i][0][0]=0.
               #isos[i][2][0]=2E-20
               #print "isos[i][1]1:",isos[i][1]
               #isos[i][1][0]=1E-20
               #print "isos[i][1]2:",isos[i][1]
               isos[i][2][13:19]=[999.]*6
               isos[i][2][19:]=[0.]*9
               #print 'here:',isos[i]
           elif (len(isos[i]) == 1):
               #print  'XXX'
               isos[i].append(isos[i][0][:]*2)
               #isos[i].append(isos[i][0])
               #print 'here:',isos[i]
               #isos[i][2][0]=2E-20
               #print "isos[i]1:",isos[i][1]
               #isos[i][1][0]=1E-20
               #print "isos[i]2:",isos[i][1]
               isos[i][2][13:19]=[999.]*6
               isos[i][2][19:]=[0.]*9
               #print isos[i]
           elif (len(isos[i]) == 2):
               #print  'YYY'
               isos[i].insert(1,isos[i][0][:])
               #isos[i][1][0]=1E-20
               #print "isos[i][1][0]1:",isos[i][1][0]
               #print 'here:',isos[i]
           
       

           #if len(NTP_u) >1: break

       #writeout
       fmt=(fmt0+fmt1+fmt2).split()
       fmt=[fmtj+' ' for fmtj in fmt]
       #print len(isos)
       #print isos[0]
       #print isos[-1]
       for i,track_file in enumerate(track_files):
           track_fp.write(iso_hdr+'\n')
           track_fp.write(track_file.split('_')[1]+' '+str(len(isos[i]))+' # '+track_file+'\n')
           iso=isos[i]
           #flag=0
           iso[0][0]==0.
           for itp in range(len(iso)):
               #iso[itp][0]=iso[itp][0]-iso[0][0]
               #if (itp > 0 and (iso[itp][0]<=0. or iso[itp][0]==iso[itp-1][0])):
               #   iso[itp][0]=iso[itp-1][0]+0.1E10
               #print "len:",len(iso[itp])
               #print "len(fmt):",len(fmt)
               #if (itp > 0 and (iso[itp][0]<=0. or iso[itp][0]==iso[itp-1][0])):
               if (itp > 0 and (iso[itp][0]==0. or iso[itp][0]==iso[itp-1][0]) ):
                  #flag=1
                  iso[itp][0]=float(iso[itp-1][0])+1E-20
               for j,fmtj in enumerate(fmt):
                   track_fp.write(fmtj % iso[itp][j])
               #if (flag==1.):
               #   flag=1
               #   iso[itp][0]=iso[itp-1][0]+1E-20
               track_fp.write('\n')


        
       track_fp.close()
       tracce_fp.write(' '+Z+' '+Y+'  '+os.path.join(isotrack_dir,'Z'+Z+'_'+agb_mix+'_'+set_name+'.dat')+'\n')
       #break

   tracce_fp.close()
   print('Done all!')
   ############
