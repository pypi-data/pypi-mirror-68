import numpy as np
import os, sys, glob, string
import re

#replacing the perl version of revisegrid_comp.pl

def revisegrid_comp(exe=None,inoutdir=None,inpdir=None,outfile=None,cut=False):
    if (exe==None): exe=os.path.join(os.environ.get('TRILEGAL_DIR'),'../isotracks/code/revisegrid/main')
    if (inoutdir==None): inoutdir=os.path.join(os.environ.get('TRILEGAL_DIR'),'../isotracks/isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3','dbert_comp035')
    set=os.path.split(inoutdir)[-1].replace('dbert_comp','')
    if (inpdir==None): inpdir=os.path.join(os.environ.get('TRILEGAL_DIR'),'../colibri_tracks/INP')
    if (outfile==None): outfile='./CAF09_V1.2S_M36_S12D_NS_MAS3_parcol_comp035.dat'

    filesHB = [os.path.join(inoutdir, f) for f in os.listdir(inoutdir) if os.path.isfile(os.path.join(inoutdir,f)) and '.HB' in f and '.HB2' not in f]
    filesINT = [f.replace('.HB','.INT') for f in filesHB]
    filesLOW = [f.replace('.HB','.LOW') for f in filesHB]
    Zs=np.array([float(re.search('_Z(.*)_Y',f).group(1)) for f in filesHB])
    Ys=np.array([float(re.search('_Y(.*)\.dat',f).group(1)) for f in filesHB])
    MHs=np.log10((Zs/(1.0-Zs-Ys))/0.0207)
    if (len(Zs) != len(filesHB)):
        print(len(Zs) != len(filesHB))
        sys.exit(1)

    Zstrs = [re.search('_Z(.*)_Y',f).group(1) for f in filesHB]
    Zstrs = [x for x,_ in sorted(zip(Zstrs,Zs))]
    Ystrs = [re.search('_Y(.*)\.dat',f).group(1) for f in filesHB]
    Ystrs = [x for x,_ in sorted(zip(Ystrs,Zs))]
    filesHB = [x for x,_ in sorted(zip(filesHB,Zs))]
    filesINT = [x for x,_ in sorted(zip(filesINT,Zs))]
    filesLOW = [x for x,_ in sorted(zip(filesLOW,Zs))]

    filesINP_all = [os.path.join(inpdir, f) for f in os.listdir(inpdir) if os.path.isfile(os.path.join(inpdir,f)) and '1TP.INP' in f]
    filesINP = []
    for Zi in Zstrs:
        filesINP.append([f for f in filesINP_all if Zi in f][0])
    #Zps=np.array([float(re.search('_Z(.*)_Y',f).group(1)) for f in filesINP])
    #Yps=np.array([float(re.search('_Y(.*)_EAGB_1TP.INP',f).group(1)) for f in filesINP])

    tmpfile='/tmp/tmp_revise_grid.txt'
    with open(tmpfile,'w') as tmpf:
       tmpf.write(str(len(Zstrs))+'\n')
       for i,_ in enumerate(Zstrs):
           tmpf.write(Zstrs[i]+' '+Ystrs[i]+'\n')
           tmpf.write(filesLOW[i]+'\n')
           if (cut == True):
               tmpf.write(filesHB[i]+' '+filesINP[i]+'\n')
               tmpf.write(filesINT[i]+' '+filesINP[i]+'\n')
           else:
               tmpf.write(filesHB[i]+'\n')
               tmpf.write(filesINT[i]+'\n')

           #check masses of .LOW and .HB files
           print([filesLOW[i],filesHB[i]])
           for trackfile in [filesLOW[i],filesHB[i]]:
               masses=[]
               with open(trackfile,'r') as track:
                   lines=track.readlines()
                   for line in lines:
                       if (' M= ' in line):
                           mass=re.search('\ M=\ (.*)\ npt',line).group(1)
                           masses.append(mass)
               print(trackfile)
               print(masses)
               print(trackfile+": found "+str(len(masses))+" masses, last one is "+masses[-1]+" Msun\n")
              

    print("Now proceed with: "+exe+' '+tmpfile+' '+outfile+' 0.04 0.01\n')
    log=os.system(exe+' '+tmpfile+' '+outfile+' 0.04 0.01')

    os.system("sed -i \'s/isotrack\/parsec/isotrack\/parcol/g\' "+outfile)
