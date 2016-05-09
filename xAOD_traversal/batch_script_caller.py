# Jannicke Pearkes

# run extract_info for all files in directory
# 
import sys
import glob
import subprocess

def run_batches(signal):
    print "beginning to talk" 
    if(signal==1):
        files = glob.glob("/data/wfedorko/mc15_13TeV.*.Pythia8EvtGen_A14NNPDF23LO_zprime*/DAOD_EXOT7.*.pool.root.1")
        #/hep300/data/jpearkes/ZvvH125_bb/mc15_13TeV.341101.Pythia8EvtGen_A14NNPDF23LO_ZvvH125_bb.merge.AOD.e3885_s2608_s2183_r6630_r6264_tid05539891_00/AOD.05539891._0000[6-9][0-9].pool.root.1")
    else:
        files =  glob.glob("/data/wfedorko/mc15_13TeV.*.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ*W.merge.DAOD_EXOT7*/DAOD_EXOT7.*.pool.root.1")
    #already_processed = glob.glob("/home1s/jpearkes/xAODAanalysis2.1.34/*_5000e_bg.csv")
    #files = [x for x in files if x not in already_processed]
    print("Number of files"+str(len(files)))
    for file in files: 
        talk = ('qsub -vinput1=\"'+file+'\" batch_extract_info.pbs')
        print(talk)
        subprocess.call(talk, shell = True)
    print "talking complete" 


if __name__ == '__main__':
    signal = 0
    if len(sys.argv)>1:    
        signal = sys.argv
        print("Using passed parameter: "+str(signal))
    else: 
        print("Using default parameter: "+str(signal))
    run_batches(signal)