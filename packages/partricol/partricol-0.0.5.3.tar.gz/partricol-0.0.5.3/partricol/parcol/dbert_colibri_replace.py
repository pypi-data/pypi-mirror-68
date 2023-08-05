import numpy as np
import os, sys, glob, string
import re

extension=['.LOW','.HB','.INT']
Linterp=[2.0, 2.5] #[-1.,-1.] ##L range for interpolating the Teff. It can be dismissed by setting Linterp=[-1,-1], or something alike.
lgL_insert=0. #now dismissed#2.5 #replace the EAGB, but below 2.5 the Teff is interpolated
apply_NTP=True


def dbert_colibri_replace(parsec_dbert_dir=None,inpdir=None,indir=None,outdir=None):
    print('dbert_colibri_replace.py: code for replacing PARSEC E-AGB with that from COLIBRI')
    print('Make sure that the number of track points are contained after the fourth line in .HB and the nineth line in .INT.')
    print('The code relies on this to load the track number points.')
    #if (len(sys.argv) !=2):
    #    print('python dbert_colibri_replace.py input.list ' #[lgL_insert]')
    #    sys.exit(2)
    #print "check the definition of C,N,O abundances"

    if (parsec_dbert_dir==None): parsec_dbert_dir=os.path.join(os.environ.get('TRILEGAL_DIR'),'../isotracks/isotrack_parsec/CAF09_V1.2S_M36_S12D_NS_MAS3/dbert_comp/')
    if (inpdir==None): inpdir=os.path.join(os.environ.get('TRILEGAL_DIR'),'../colibri_tracks/INP')
    if (indir==None): indir=os.path.join(os.environ.get('TRILEGAL_DIR'),'../colibri_tracks/S_035')
    Set=os.path.split(indir)[-1].replace('S_','')
    if (outdir==None): outdir=os.path.join('./isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3','dbert_comp'+Set)
    if (not os.path.isdir(outdir)): os.makedirs(outdir)
  
    parsecs = [os.path.join(parsec_dbert_dir, f) for f in os.listdir(parsec_dbert_dir) if os.path.isfile(os.path.join(parsec_dbert_dir, f))]
    colibri_dirs = [os.path.join(indir, f) for f in os.listdir(indir) if os.path.isdir(os.path.join(indir, f))]
    col_inps = [os.path.join(inpdir, f) for f in os.listdir(inpdir) if os.path.isfile(os.path.join(inpdir, f))]
    Zs=[re.search('_Z(.*)_Y',tmpdir).group(1) for tmpdir in colibri_dirs]


    inps_names='n1 env m1 l1 te1 t1'.split() #for reading COLIBRI INP files
    #outer loop over different Zs
    for Zi in Zs:
        #COLIBRI INP files
        col_inpi = [s for s in col_inps if '_Z'+Zi+'_Y' in s]
        if (len(col_inpi) != 1):
           print(col_inpi)
           sys.exit(1)
        col_inpi=col_inpi[0]
        print('COLIBRI .INP file:', col_inpi)
        #inps=np.genfromtxt(col_inpi,dtype=("S100","S100","S100","S100","S100","S100"),names=inps_names,skip_footer=1,usecols=(0,3,5,6,7,36))
        inps=np.genfromtxt(col_inpi,dtype=("S100","S100","S100","S100","S100","S100"),names=inps_names,invalid_raise=False,usecols=(0,3,5,6,7,36))
        masses0=np.unique(inps['m1']) #get unique masses based on the INP file
        mode0=inps['n1'][np.argwhere(inps['env'] == b'-2')] #get the starting index for each mass
        logl0=inps['l1'][np.argwhere(inps['env'] == b'-2')]
        logt0=inps['te1'][np.argwhere(inps['env'] == b'-2')]
        if (len(masses0) != len(mode0)):
            print('Wrong INP file, stop! Please check')
            exit(2)
    
        #COLIBRI track file names
        colibri_diri=[s for s in colibri_dirs if '_Z'+Zi+'_Y' in s] #contains COLIBRI track file names
        if (len(colibri_diri) != 1):
           print(colibri_diri)
           sys.exit(1)
        colibri_diri=colibri_diri[0]
        colibris=[]
        for tmp in glob.glob(os.path.join(colibri_diri,'agb_*.dat')):
            with open(tmp) as tmpf:
                for tmpi,tmpl in enumerate(tmpf):
                    if tmpi > 10: break
            if (tmpi<10):
                print('skip track (with less than 10 line):',tmp)
                continue
            colibris.append(tmp)
        masses1=[(re.search('agb_[0-9]\.[0-9]*_',os.path.basename(x)).group(0)).split('_')[1] for x in colibris]
        #masses1,colibris=zip(*[(x,y) for (z,x,y) in sorted(zip(np.array(masses1).astype(np.float),masses1,colibris))]) #sorting
        masses1,colibris=list(zip(*[(x,y) for (z,x,y) in sorted(zip(np.array(masses1).astype(np.float),masses1,colibris))])) #sorting
        masses1=np.array(masses1)
        colibris=np.array(colibris)
    
        #some tracks might be missing compared to the INP file, so get the same masses
        idx0=[j for j,x in enumerate(masses0) if float(x) in masses1.astype(float)] #for each[i] masses0[i] == masses1[i]
        idx1=[j for j,x in enumerate(masses1) if float(x) in masses0.astype(float)] #for each masses1[i] == masses0[i]
        masses1=list(masses1[idx1])
        colibris=list(colibris[idx1])
        masses0=list(masses0[idx0])
        mode0=list(mode0[idx0])
        logl0=list(logl0[idx0])
        logt0=list(logt0[idx0])
        masses0f=list(np.array(masses0).astype(float))
    
        #load the INP array
        #out_inp=[filter(lambda x: x[0] == mass, zip(inps['m1'],inps['n1'],inps['l1'],inps['te1'],inps['t1'])) for mass in masses0]
        #mass_inp,mode_inp,logl_inp,logt_inp,age_inp=zip(*[zip(*outi) for outi in out_inp])
        out_inp=[[x for x in zip(inps['m1'],inps['n1'],inps['l1'],inps['te1'],inps['t1']) if x[0] == mass] for mass in masses0]
        mass_inp,mode_inp,logl_inp,logt_inp,age_inp=list(zip(*[list(zip(*outi)) for outi in out_inp]))

        parseci=[s.replace('.HB2','') for s in parsecs if '_Z'+Zi+'_Y' in s and '.HB2' in s] #contains COLIBRI track file names
        if (len(parseci) != 1):
           print(parseci)
           sys.exit(1)
        parseci=parseci[0]
        ##loop over .HB .INT of the same Z
        for iext,ext in enumerate(extension):
            if (ext == '.LOW'):
                print('Simply copy .LOW file:', parseci+ext)
                os.system('cp '+parseci+ext+' '+outdir+'/'+os.path.basename(parseci)+ext)
                continue
            
            #load PARSEC file
            print('PARSEC file: ', parseci+ext)
            parsec_a=open(parseci+ext,'r').read() #load the whole PARSEC HB/INT file
            parsec_l=parsec_a.split('\n')
            
            #split the PARSEC track into several parts
            ihdr_end=-1
            itracks_end=-1
            icri_start=-1
            icri_end=-1
            for j in np.arange(len(parsec_l)): #-1,-1,-1):
                line=parsec_l[j]
                if ('AGE' in line): ihdr_end=j
                if ('HeLST' in line or 'Loop_C' in line): itracks_end=j #'HeLST' -> 'TPAGB'
                if ('M' in line): icri_end=j
                if ('M=' in line and (not 'npt=' in line) and icri_start==-1): icri_start=j
            if (ext == '.HB'):
                hdr_pre=parsec_l[0:4]
                hdr=parsec_l[4:ihdr_end]
                start_i=0
            else:
                hdr_pre=parsec_l[0:9]
                hdr=parsec_l[9:ihdr_end]
                star_i=int(hdr_pre[3].split()[0])-1
            hdr_app=parsec_l[ihdr_end]
            tracks=parsec_l[ihdr_end+1:itracks_end+1]
            tail_pre=parsec_l[itracks_end+1:icri_start]
            tail=parsec_l[icri_start:icri_end+1]
            if (ext == '.HB'): tail_app=parsec_l[icri_end+1:]
            else: tail_app=parsec_l[icri_end+1:-1]
    
            #get masses and npts
            for hdr_j, hdr_l in enumerate(hdr):
                if float(hdr_l.split()[0]) < 1.0: break
            hdr_mass_lines=hdr[hdr_j:]
            #print "hdr_mass_lines:",hdr_mass_lines
            hdr=' '.join(hdr).split()
            npts=hdr[0:int(len(hdr)/2)]
            #print 'npts:',npts
            masses2=hdr[int(len(hdr)/2):]
            if ( len(masses2) != int(hdr_pre[-1]) ):
                print('Wrong in',parseci+ext,':')
                print('number of masses unequal the claimed')
                exit(2)
            TP_flag=['{:10.7f}'.format(0.) for x in range(len(masses2))]
            NTP=np.zeros(len(masses2))
            eagb_mass_imatch=np.zeros(len(masses2)).astype(int)-1
            #print "len(TP_flag)",len(TP_flag)
            npts_new=npts
            #print "len :npts_new:", len(npts_new)
            for k in range(len(masses2)): npts_new[k]='{:>8s}'.format(npts[k])
            #print "len: npts_new:", len(npts_new)
    
            #match masses between PARSEC and COLIBRI
            for k in range(start_i,len(masses2)):
                if (float(masses2[k]) < float(masses0[0]) or float(masses2[k]) > float(masses0[-1])): continue
                for j in range(len(masses0)):
                    if float(masses2[k]) == float(masses0[j]):
                        eagb_mass_imatch[k]=j
    
            #loop over each line of a PARSEC file at given Z
            im_par=-1
            line_keep=True
            new_tracks=[]
            inew=0
            line_npt=0
            k0=-1
            k1=-1
            for j,line in enumerate(tracks):
                if j < len(tracks)-1: line_next=tracks[j+1]
                if ('He1' in line or 'PMS_BEG' in line): #begining of a new mass
                    check_He0=0
                    line_keep=True
                    insert_new=False
                    line_npt=inew
                    im_par=im_par+1
                    i_inp=-1
                    
                if (eagb_mass_imatch[im_par] != -1):
                    if (line.split()[-1] == 'He0' or line.split()[-1] == 'Loop_C'):
                        check_He0=1
                        imass=eagb_mass_imatch[im_par] #imass is the index of mass in eagb
                        fp=open(colibris[imass],'r')
                        hdr_col=fp.readline()[1:]
                        fp.close()
                        hdr_col=hdr_col.replace('*','star').replace('/','_').split()
                        col=np.genfromtxt(colibris[imass],names=hdr_col,skip_header=1) #load the COLIBRI track
                        id_tpagb=np.argwhere(col['step'] <= 1.) #'1' is the first TP-AGB point
                        if (1. in col['step']): #For low masses, there is no TPAGB
                            if (k0==-1):k0=im_par #TPAGB flag: start of TPAGB and end of TPAGB.
                            k1=im_par             #For .HB, actually only k0 needed, while for .INT, only k1 is needed
    
                    if (check_He0 == 1):
                        tmpamin=np.abs(np.array(age_inp[imass]).astype(float)-float(line_next.split()[0])) #find the closest age.
                        valid_idx=np.where(tmpamin >= 0.)[0] #
                        i_inp=valid_idx[tmpamin[valid_idx].argmin()]
                        if (i_inp <0):
                            print('wrong0')
                            exit(2)
                        if (int(line_next.split()[4])-1 >= int(mode0[imass][0]) \
                            and int(line_next.split()[4])-1 <= int(mode_inp[imass][-1]) \
                            and float(line_next.split()[1]) >= lgL_insert): #2.0 works, but still jump. 2.5: trilegal run error
                            #just to make sure 'mode' is in the range
                            #The COLIBRI EAGB phase could be shorter than that of PARSEC. If the logL criterium is too large, the point could be out of the range of COLIBRI.
                            #In some cases, the first of point of COLIBRI EAGB is before 'He0', then the PARSEC point could be out of range. 
                            line_keep=False
                            insert_new=True
                            check_He0=0
    
                if (line_keep == True): #just copy un-replaced lines
                    new_tracks.append(line)
                    inew=inew+1
                elif(insert_new == False): #skip PARSEC lines after the first replace point
                    if (check_He0 == 1):
                        print('line_keep',line_keep)
                        print('wrong1')
                        exit(2)
                    if (line.split()[-1] == 'He0' or line.split()[-1] == 'Loop_C'):
                        print('Wrong! He0 point is after the first point in COLIBRI INP:',colibris[imass])
                    continue
                else: #replace with COLIBRI points
                    insert_new=False 
                    if (check_He0 == 1):
                        print('wrong2')
                        exit(2)
                    new_tracks.append(line)
                    inew=inew+1
                    line_last_keep_s=line.split()
    
                    print('inserting colibri track: ',colibris[imass])
    
                    #interp the Teff. Linterp
                    #get the PARSEC L-Teff relation
                    iplus=j; Lpar=[]; Tpar=[]
                    while True:
                        if (iplus == len(tracks)): break
                        tmppar=tracks[iplus].split()
                        jpar=int(tmppar[3])-1
                        if (jpar == 0): break
                        iplus=iplus+1
                        if (float(tmppar[1]) < Linterp[0] or float(tmppar[1]) > Linterp[1]): continue
                        Lpar.append(float(tmppar[1]))
                        Tpar.append(float(tmppar[2]))
                    if (len(Lpar) > 0):
                        NTP[im_par]=col['NTP'][-1]
                        if col['status'][-1] < 7: NTP[im_par]=NTP[im_par]-1
                        Lcolmax=-1
                        for k in range(i_inp,len(id_tpagb)):
                            if (float(col['lgL_star'][k]) > Lcolmax): Lcolmax=float(col['lgL_star'][k])
                        for k in range(i_inp,len(id_tpagb)):
                            Lcol=float(col['lgL_star'][k])
                            Tcol=float(col['lgT_star'][k])
                            if ((Lcol >= Linterp[0]) and (Lcol <= Linterp[1])):
                                Tinter=np.interp(Lcol, Lpar, Tpar)
                                fact=(Lcol-Linterp[0])/(min(Linterp[1],Lcolmax)-Linterp[0])
                                if fact > 1.0: fact=1.
                                if fact < 0.:  fact=0.
                                Ti=(1-fact)*Tinter + fact*Tcol
                                col['lgT_star'][k]=str(Ti)
    
                    
                    new_lines=[]
                    print('i_inp,len(id_tpagb):',i_inp,len(id_tpagb))
                    for k in range(i_inp,len(id_tpagb)): #age is corrected. #mode_inp[imass][k] is shifted by 1 WRT PARSEC
                        new_line=('{:20.12E}'+'{:10.5f}'*2+'{:8d}'*2+'{:11.5f}'*7+'{:>11s}'*5)\
                        .format(float(line_next.split()[0])+col['age_yr'][k]-col['age_yr'][i_inp],\
                        col['lgL_star'][k], col['lgT_star'][k],\
                        int(line_last_keep_s[3])+k-i_inp+1, int(mode_inp[imass][k])+1,\
                        col['M_star'][k], np.log10(col['H'][k]),\
                        np.log10(col['He4'][k]), np.log10(col['C12'][k]), np.log10(col['O16'][k]),\
                        np.log10(col['N14'][k]), col['lgdM_dt'][k], line_last_keep_s[12],\
                        line_last_keep_s[13], line_last_keep_s[14],\
                        line_last_keep_s[15], line_last_keep_s[16])
                        new_lines.append(new_line)
                        if (k==i_inp):
                            print('age diff of inserted (line_next):', float(age_inp[imass][k])-float(line_next.split()[0]))
                            print('mode:', mode_inp[imass][k], line_next.split()[4])
                            print('delta(mode)=', int(mode_inp[imass][k])-int(line_next.split()[4]))
                            print('logL:', logl_inp[imass][k], line_next.split()[1])
                            print('logTe:', logt_inp[imass][k], line_next.split()[2])
                            if(abs(float(age_inp[imass][k])-float(line_next.split()[0])) > 1E4):
                                print('the age difference is too large, please check, or dismiss the following line')
                                sys.exit(2)
                            print('age diff of inserted (line):', float(age_inp[imass][k])-float(line.split()[0]))
                            print('lgL diff (line_next):', float(logl_inp[imass][k])-float(line_next.split()[1]))
                            print('lgL diff (line):', float(logl_inp[imass][k])-float(line.split()[1]))
    
                    if (len(new_lines)>0): #I do not know why ==0 would happen.
                        if (ext == '.HB'): new_lines[-1]=new_lines[-1]+'      HeLST'
                        else: new_lines[-1]=new_lines[-1]+'      TPAGB'
                        new_tracks.extend(new_lines)
                        inew=inew+len(new_lines)
                        #change npt
                        npt_new=int(line_last_keep_s[3])+len(new_lines) #npt_new+len(new_lines)
                        npts_new[im_par]='{:>8d}'.format(npt_new)
                        new_tracks[line_npt]=re.sub('%s(.*)%s' % ('npt=', 'kind='),'npt='+str(npt_new)+'  kind=',new_tracks[line_npt])
                        out1='L1 & T1: PARSEC('+line_next.split()[1]+','+line_next.split()[2]+\
                              ')--COLIBRI('+'{}'.format(col['lgL_star'][i_inp])+','+'{}'.format(col['lgT_star'][i_inp])+')'
                        print(out1)
                        ltmp=tail[im_par]
                        ltmp_all=re.search('( *[0-9]*)( *.?)%s%s' % ('M=','{:5.3f}'.format(float(masses0[imass]))),ltmp)
                        if (ltmp_all == None):
                            print('somthing wrong, no match!')
                            print(ltmp, mass, masses0[imass])
                            sys.exit(2)
                        ltmp0=ltmp_all.group(0)
                        ltmp1=ltmp_all.group(1)
                        ltmp0_new=re.sub('%s' % ltmp1, ' '+'{:4d}'.format(npt_new),ltmp0)
                        tail[im_par]=ltmp.replace(ltmp0,ltmp0_new)
    
                    
            if (ext == '.HB'):
                k1=len(masses2)
                if k1 < len(TP_flag): k1=len(TP_flag)
                if len(TP_flag) != len(NTP):
                    print('wrong')
                    exit(1)
                itp=np.where(NTP > 1.)[0][0]
                if (apply_NTP == True):
                    if k0 < itp: k0=itp
            else:
                tmp=np.array(' '.join(tail_app).split()).astype(float)
                print("tmp:",tmp)
                tp_idx=np.where((tmp > 0.)&(tmp <1.5))[0]
                id_tmp=tp_idx[tmp[tp_idx].argmax()]
                print("id_tmp:",id_tmp)
                if (k1<id_tmp+1): k1=id_tmp+1
                if k0 != 0: k0=0
            TP_flag[k0:k1]=['{:10.7f}'.format(1.)]*(k1-k0)
            
            #writing out
            print('Writting output:',outdir+'/'+os.path.basename(parseci)+ext)
            fp=open(outdir+'/'+os.path.basename(parseci)+ext,'w')
            fp.write(('\n'.join(hdr_pre)+'\n').replace('\n\n','\n'))
            #fp.write('\n'.join(hdr_pre)+'\n')

            npts_new_lines=[''.join(npts_new[10*k: 10*k+10]) for k in range(0, int(np.ceil(len(npts_new)/10)))]
            if (len(npts_new)%10 != 0): npts_new_lines.extend([''.join(npts_new[10*k+10:])])
            fp.write(('\n'.join(npts_new_lines)+'\n').replace('\n\n','\n'))
            
            fp.write(('\n'.join(hdr_mass_lines)+'\n').replace('\n\n','\n'))
    
            fp.write((hdr_app+'\n').replace('\n\n','\n'))
            fp.write(('\n'.join(new_tracks)+'\n').replace('\n\n','\n'))
            fp.write(('\n'.join(tail_pre)+'\n').replace('\n\n','\n'))
            fp.write(('\n'.join(tail)+'\n').replace('\n\n','\n'))
    
    
            TP_flag_a=[''.join(TP_flag[10*k: 10*k+10]) for k in range(0, int(np.ceil(len(TP_flag)/10)))]
            if (len(TP_flag)%10 != 0): TP_flag_a.extend([''.join(TP_flag[10*k+10:])])        
            fp.write(('\n'.join(TP_flag_a)+'\n').replace('\n\n','\n'))
    
            if (ext == '.INT'):fp.write((parsec_l[len(parsec_l)-1]+'\n').replace('\n\n','\n'))
            fp.close()
    
                                                       
        print('Done for one Z!')
                        
                        
    print('All done: replacing PARSEC E-AGB with that from COLIBRI\n')
'''
0.001 5.0
0.002 4.8
0.004 5.4
0.006 5.4
0.008 5.6
0.010 5.6
0.014 6.0
0.017 6.0
0.020 6.0
'''
