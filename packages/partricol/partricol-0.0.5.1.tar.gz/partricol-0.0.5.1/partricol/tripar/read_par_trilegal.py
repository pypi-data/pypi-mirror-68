import sys

#if (len(sys.argv) != 1):
#   print 'read_par_trilegal.py usage: read_par_trilegal(par_file)'
#   sys.exit(2)
#par_file=sys.argv[0]

#def def_par_trilegal(par_file_name):
class read_par_trilegal(object):

   def __init__(self,par_file_name):

      par_file=open(par_file_name,'r')

      par_name=['']
      par_val=['']

      for line in par_file:
         pos=line.find('#')
         if (pos != -1):
            line=line[0:pos]

#      line=line.strip()
         pos=line.find('=')
         if (pos != -1):
            par_name.append(line[0:pos].strip())
         else:
            continue

         pos1=line.find("'")
         pos2=line.rfind("'")
         if (pos1 == -1 or pos2 == -1 or pos1 == pos2):
            print 'wrong parameter line'
            sys.exit(2)
         else:
            par_val.append(line[pos1+1:pos2])

      par_file.close()


      par_name=par_name[1:]
      par_val=par_val[1:]

      self.par_name=par_name
      self.par_val=par_val
 #  class mod_par_trilegal():
#   def __init__(self, name, val):
#      self.par_name=name
#      self.par_val=val

#   print "Hi there"
#   mod_par=read_par_trilegal(par_name, par_val)
#   return mod_par



