# Jannicke Pearkes

# run extract_info for all files in directory
# 
import sys
import glob
import subprocess
import time
from pprint import pprint

def run_batches(signal):
    print "beginning to talk" 

    if(signal==1):
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301323.Pythia8EvtGen_A14NNPDF23LO_zprime500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896470_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301324.Pythia8EvtGen_A14NNPDF23LO_zprime750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618493_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301326.Pythia8EvtGen_A14NNPDF23LO_zprime1250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618469_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301327.Pythia8EvtGen_A14NNPDF23LO_zprime1500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618474_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301328.Pythia8EvtGen_A14NNPDF23LO_zprime1750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618465_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301330.Pythia8EvtGen_A14NNPDF23LO_zprime2250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618509_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301332.Pythia8EvtGen_A14NNPDF23LO_zprime2750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618514_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301333.Pythia8EvtGen_A14NNPDF23LO_zprime3000*/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301329.Pythia8EvtGen_A14NNPDF23LO_zprime2000*/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301325.Pythia8EvtGen_A14NNPDF23LO_zprime1000*/DAOD_EXOT7.*.pool.root.1")
        #files = glob.glob("/data/wfedorko/mc15_13TeV.301334.Pythia8EvtGen_A14NNPDF23LO_zprime4000*/DAOD_EXOT7.*.pool.root.1")
        #all_files = [
        #glob.glob("/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301323.Pythia8EvtGen_A14NNPDF23LO_zprime500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896470_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301324.Pythia8EvtGen_A14NNPDF23LO_zprime750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618493_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301326.Pythia8EvtGen_A14NNPDF23LO_zprime1250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618469_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301327.Pythia8EvtGen_A14NNPDF23LO_zprime1500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618474_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301328.Pythia8EvtGen_A14NNPDF23LO_zprime1750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618465_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301330.Pythia8EvtGen_A14NNPDF23LO_zprime2250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618509_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301332.Pythia8EvtGen_A14NNPDF23LO_zprime2750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618514_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301333.Pythia8EvtGen_A14NNPDF23LO_zprime3000*/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301329.Pythia8EvtGen_A14NNPDF23LO_zprime2000*/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301325.Pythia8EvtGen_A14NNPDF23LO_zprime1000*/DAOD_EXOT7.*.pool.root.1")
        #,glob.glob("/data/wfedorko/mc15_13TeV.301334.Pythia8EvtGen_A14NNPDF23LO_zprime4000*/DAOD_EXOT7.*.pool.root.1")
        #]
        all_files = [
          #glob.glob("/data/wfedorko/mc15_13TeV.361022.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618436_00/*.root.1")
        glob.glob("/data/wfedorko/mc15_13TeV.361023.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618457_00/*.root.1")
        ,glob.glob("/data/wfedorko/mc15_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618452_00/*.root.1")
        ,glob.glob("/data/wfedorko/mc15_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618479_00/*.root.1")
        ,glob.glob("/data/wfedorko/mc15_13TeV.361026.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6W.merge.DAOD_EXOT7.e3569_s2608_s2183_r7267_r6282_p2495_tid07618523_00/*.root.1")
        ,glob.glob("/data/wfedorko/mc15_13TeV.361027.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ7W.merge.DAOD_EXOT7.e3668_s2608_s2183_r7267_r6282_p2495_tid07618484_00/*.root.1")
        ,glob.glob("/data/wfedorko/mc15_13TeV.361028.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ8W.merge.DAOD_EXOT7.e3569_s2576_s2132_r7267_r6282_p2495_tid07618520_00/*.root.1")
        ,glob.glob("/data/wfedorko/mc15_13TeV.361029.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ9W.merge.DAOD_EXOT7.e3569_s2576_s2132_r7267_r6282_p2495_tid07618506_00/*.root.1")
        ]

        pprint(all_files)
        #files = glob.glob("/data/wfedorko/mc15_13TeV.*zprime*/DAOD_EXOT7*.pool.root.1")
        #/hep300/data/jpearkes/ZvvH125_bb/mc15_13TeV.341101.Pythia8EvtGen_A14NNPDF23LO_ZvvH125_bb.merge.AOD.e3885_s2608_s2183_r6630_r6264_tid05539891_00/AOD.05539891._0000[6-9][0-9].pool.root.1")
    else:
        files =  glob.glob("/data/wfedorko/mc15_13TeV.*.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6W.merge.DAOD_EXOT7*/DAOD_EXOT7.*.pool.root.1")
    #already_processed = glob.glob("/home1s/jpearkes/xAODAanalysis2.1.34/*_5000e_bg.csv")
    #files = [x for x in files if x not in already_processed]
    for files_at_mass_point in all_files:
        print("Number of files: "+str(len(files_at_mass_point)))
        i = 1
        for file in files_at_mass_point: 
            talk = ('qsub -vinput1=\"'+file+'\" batch_extract_info.pbs')
            #talk = 'python skeleton.py file &'
            print(talk)
            subprocess.call(talk, shell = True)
            #time.sleep(1)
            if(i%2 ==0):
                time.sleep(60)
            if(i%20 ==0):
                time.sleep(120)
            i+=1
    print "talking complete" 


if __name__ == '__main__':
    signal = 1
    if len(sys.argv)>1:    
        signal = sys.argv
        print("Using passed parameter: "+str(signal))
    else: 
        print("Using default parameter: "+str(signal))
    run_batches(signal)