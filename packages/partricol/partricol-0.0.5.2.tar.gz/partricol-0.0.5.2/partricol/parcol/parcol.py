import sys
from .dbert_colibri_replace import dbert_colibri_replace
from .revisegrid_comp import revisegrid_comp

#sys.path.append(os.path.abspath("/run/media/chen/SED/gitlab/partricol/partricol/parcol/"))
#parcol(exe="../isotracks/code/revisegrid/main",parsec_dbert_dir="../isotracks/isotrack_parsec/CAF09_V1.2S_M36_S12D_NS_MAS3/dbert_comp",inpdir="./INP",indir="./S_035",outdir="isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3/dbert_comp035",outfile="isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3_parcol_comp035.dat")


def parcol(exe=None,parsec_dbert_dir=None,inpdir=None,indir=None,outdir=None,outfile=None,cut=False):

    dbert_colibri_replace(parsec_dbert_dir=parsec_dbert_dir,inpdir=inpdir,indir=indir,outdir=outdir)
    revisegrid_comp(exe=exe,inoutdir=outdir,inpdir=inpdir,outfile=outfile,cut=cut)



'''
import numpy as np
import os, sys, glob, string
import re
sys.path.append(os.path.abspath("/run/media/chen/SED/gitlab/partricol/partricol/parcol/"))
from dbert_colibri_replace import dbert_colibri_replace
dbert_colibri_replace()



import numpy as np
import os, sys, glob, string
import re
sys.path.append(os.path.abspath("/run/media/chen/SED/gitlab/partricol/partricol/parcol/"))
from revisegrid_comp import revisegrid_comp
#revisegrid_comp()
revisegrid_comp(exe="../isotracks/code/revisegrid/main",indir="isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3/dbert_comp035",inpdir="INP",outfile="./CAF09_V1.2S_M36_S12D_NS_MAS3_parcol_comp035.dat")



import os,sys
sys.path.append(os.path.abspath("/run/media/chen/SED/gitlab/partricol/partricol/parcol/"))
from parcol import parcol
parcol(exe="../isotracks/code/revisegrid/main",parsec_dbert_dir="../isotracks/isotrack_parsec/CAF09_V1.2S_M36_S12D_NS_MAS3/dbert_comp",inpdir="./INP",indir="./S_035",outdir="isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3/dbert_comp035",outfile="isotrack_parcol/CAF09_V1.2S_M36_S12D_NS_MAS3_parcol_comp035.dat")
'''
