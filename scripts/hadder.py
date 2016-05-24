import sys
import glob
import subprocess
import time
from pprint import pprint


def hadder():
    prefix = "dijetJZ"
    #prefix = "zprime"
    suffix = "jet_pt.root"
    
    #masses = [400, 500, 750,1000,1250,1500,1750,2000,2250,2750,3000,4000,5000]
    masses = [2,3,4,5,6,7,8,9]
    print "beginning to hadd" 
    for i in xrange(len(masses)):
        name = "outputs/"+prefix+str(masses[i])+"*"+suffix
        #print(name)
        files = glob.glob(name)
        name2 = "outputs/"+prefix+str(masses[i])+"_000000"+suffix
        if name2 in files:
            print("File "+name2+" already exists, do nothing")
            files.remove(name2)
            #pprint(files)
        if (len(files)>0):
            talk = "hadd -f "+name2+" "+' '.join(map(str, files))
            print talk 
            print " "
            subprocess.check_call(talk, shell = True)

    
if __name__ == '__main__':
    hadder()