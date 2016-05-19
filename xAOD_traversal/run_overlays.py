# Jannicke Pearkes

# run extract_info for all files in directory
# 
import sys
import glob
import subprocess

def run_batches():
    print "beginning to talk" 
    masses = [1000,2000,3000,4000,5000]
    for mass in masses:
        files = glob.glob("/data/wfedorko/mc15_13TeV.*.Pythia8EvtGen_A14NNPDF23LO_zprime"+str(mass)+"*/DAOD_EXOT7.*.pool.root.1")
        for i in xrange(2):#len(files)):
            talk = ('python extract_info.py '+files[i]+' &')
            print(talk)
            subprocess.call(talk, shell = True)
    print "talking complete" 


if __name__ == '__main__':
    run_batches()