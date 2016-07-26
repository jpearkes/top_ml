import sys
import glob
import subprocess
import time
from pprint import pprint


def run_batches(signal):
    ''' 
    Submits batch jobs for processing events from DAODs 

    Runs over files in groups related to their mass points

    Includes large time delay between submissions so as not to overload the I/O on batch system

    Run in screen 

    '''
    print "beginning to talk"

    all_files = [
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08606957_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301323.Pythia8EvtGen_A14NNPDF23LO_zprime500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08607167_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301324.Pythia8EvtGen_A14NNPDF23LO_zprime750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08607495_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301325.Pythia8EvtGen_A14NNPDF23LO_zprime1000_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08606805_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301326.Pythia8EvtGen_A14NNPDF23LO_zprime1250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08606758_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301327.Pythia8EvtGen_A14NNPDF23LO_zprime1500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08607003_00/DAOD_EXOT7.*.pool.root.1"),
        glob.glob("/data/jpearkes/datasets/mc15_13TeV.301328.Pythia8EvtGen_A14NNPDF23LO_zprime1750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08606910_00/DAOD_EXOT7.*.pool.root.1"),
        glob.glob("/data/jpearkes/datasets/mc15_13TeV.301329.Pythia8EvtGen_A14NNPDF23LO_zprime2000_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08607104_00/DAOD_EXOT7.*.pool.root.1"),
        glob.glob("/data/jpearkes/datasets/mc15_13TeV.301330.Pythia8EvtGen_A14NNPDF23LO_zprime2250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08606993_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301331.Pythia8EvtGen_A14NNPDF23LO_zprime2500_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08607396_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301332.Pythia8EvtGen_A14NNPDF23LO_zprime2750_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7725_r7676_p2669_tid08607117_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301333.Pythia8EvtGen_A14NNPDF23LO_zprime3000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7725_r7676_p2669_tid08607521_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301334.Pythia8EvtGen_A14NNPDF23LO_zprime4000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7725_r7676_p2669_tid08606886_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7725_r7676_p2669_tid08607211_00/DAOD_EXOT7.*.pool.root.1")#,

        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361023.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7725_r7676_p2666_tid08606719_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361023.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7725_r7676_p2666_tid08606728_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7725_r7676_p2666_tid08606264_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7725_r7676_p2666_tid08606272_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7725_r7676_p2666_tid08606484_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7725_r7676_p2666_tid08606493_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361026.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6W.merge.DAOD_EXOT7.e3569_s2608_s2183_r7725_r7676_p2666_tid08606668_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361027.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ7W.merge.DAOD_EXOT7.e3668_s2608_s2183_r7725_r7676_p2666_tid08606556_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361028.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ8W.merge.DAOD_EXOT7.e3569_s2576_s2132_r7772_r7676_p2666_tid08606361_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361029.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ9W.merge.DAOD_EXOT7.e3569_s2576_s2132_r7772_r7676_p2666_tid08606375_00/DAOD_EXOT7.*.pool.root.1"),
        # glob.glob("/data/jpearkes/datasets/mc15_13TeV.361030.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ10W.merge.DAOD_EXOT7.e3569_s2576_s2132_r7772_r7676_p2666_tid08606314_00/DAOD_EXOT7.*.pool.root.1")
    ]
    # Graviton 
    # all_files = [
    #     glob.glob("/data/jpearkes/datasets/mc15_13TeV.305012.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_tt_c10_m0400.merge.DAOD_EXOT4.e4859_s2726_r7772_r7676_p2669_tid08602241_00/DAOD_EXOT4.*.pool.root.1"),
    #     glob.glob("/data/jpearkes/datasets/mc15_13TeV.305013.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_tt_c10_m0500.merge.DAOD_EXOT4.e4859_s2726_r7772_r7676_p2669_tid08601852_00/DAOD_EXOT4.*.pool.root.1"),
    #     glob.glob("/data/jpearkes/datasets/mc15_13TeV.305014.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_tt_c10_m0750.merge.DAOD_EXOT4.e4859_s2726_r7772_r7676_p2669_tid08601861_00/DAOD_EXOT4.*.pool.root.1"),
    #     glob.glob("/data/jpearkes/datasets/mc15_13TeV.305015.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_tt_c10_m1000.merge.DAOD_EXOT4.e4859_s2726_r7772_r7676_p2669_tid08601620_00/DAOD_EXOT4.*.pool.root.1"),
    #     glob.glob("/data/jpearkes/datasets/mc15_13TeV.305016.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_tt_c10_m2000.merge.DAOD_EXOT4.e4859_s2726_r7772_r7676_p2669_tid08601780_00/DAOD_EXOT4.*.pool.root.1"),
    #     glob.glob("/data/jpearkes/datasets/mc15_13TeV.305017.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_tt_c10_m3000.merge.DAOD_EXOT4.e4859_s2726_r7772_r7676_p2669_tid08601740_00/DAOD_EXOT4.*.pool.root.1")
    #     ]
    
    pprint(all_files)
     
    for files_at_mass_point in all_files:
        print("Number of files: " + str(len(files_at_mass_point)))
        i = 1
        for file in files_at_mass_point:
            talk = ('qsub -vinput1=\"' + file + '\" batch_extract_info.pbs')
            print(talk)
            subprocess.call(talk, shell=True)
            time.sleep(60)
            if(i % 20 == 0):
                time.sleep(120)
            i += 1
        time.sleep(5)
    print "talking complete"


if __name__ == '__main__':

    if len(sys.argv) > 1:
        signal = sys.argv
        print("Using passed parameter: " + str(signal))
    else:
        print("Using default parameter: " + str(signal))
    run_batches(signal)
