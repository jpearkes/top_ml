# Jannicke Pearkes

# run extract_info for all files in directory
# 
import sys
import glob
import subprocess
import time

def run_batches(signal):
    print "beginning to talk" 
    if(signal==1):
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301323.Pythia8EvtGen_A14NNPDF23LO_zprime500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896470_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301324.Pythia8EvtGen_A14NNPDF23LO_zprime750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618493_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301326.Pythia8EvtGen_A14NNPDF23LO_zprime1250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618469_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301327.Pythia8EvtGen_A14NNPDF23LO_zprime1500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618474_00/DAOD_EXOT7.*.pool.root.1")
        files = glob.glob("/data/wfedorko/mc15_13TeV.301328.Pythia8EvtGen_A14NNPDF23LO_zprime1750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618465_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301330.Pythia8EvtGen_A14NNPDF23LO_zprime2250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618509_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301332.Pythia8EvtGen_A14NNPDF23LO_zprime2750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618514_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301333.Pythia8EvtGen_A14NNPDF23LO_zprime3000*/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301329.Pythia8EvtGen_A14NNPDF23LO_zprime2000*/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301325.Pythia8EvtGen_A14NNPDF23LO_zprime1000*/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301334.Pythia8EvtGen_A14NNPDF23LO_zprime4000*/DAOD_EXOT7.*.pool.root.1")
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
        time.sleep(0.1)
    print "talking complete" 


if __name__ == '__main__':
    signal = 1
    if len(sys.argv)>1:    
        signal = sys.argv
        print("Using passed parameter: "+str(signal))
    else: 
        print("Using default parameter: "+str(signal))
    run_batches(signal)