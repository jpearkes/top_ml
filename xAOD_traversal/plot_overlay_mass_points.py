import ROOT
from ROOT import TCanvas, TF1

c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )

# Create a one dimensional function and draw it
f = ROOT.TFile.Open("outputs/zprime5000_000005delta_r.root")
f.ls()
#for entry in t.GetEntries())
t = f.Get("h_delta_r_top_W")
t.SetLineColor(ROOT.kRed)
t.SetName("test")
t.Draw()#"uniform")
#fun1 = TF1( 'fun1', 'abs(sin(x)/x)', 0, 10 )
#c1.SetGrid()
#fun1.Draw()
c1.BuildLegend(0.55,0.32,0.88,0.12,"Legend Name")
c1.Print("hello.pdf")
'''
import ROOT
from ROOT import TCanvas, TNtuple, TH1F, TH2F, TF1, TLegend, TFile, TTree, THStack
from ROOT import TLatex, TAxis, TPaveText, TGaxis
from ROOT import gROOT, gSystem, gStyle, gPad, gEnv, gRandom

def superTest():

   c1 = TCanvas("c1","c1",600,400)
   # create/fill draw h1
   # -------------------
   gStyle.SetOptStat(ROOT.kFALSE)
   h1 = TH1F("h1","Superimposing two histograms with different scales",100,-3,3)
   
   for i in range(10000):
       h1.Fill(gRandom.Gaus(0,1))
   h1.Draw()
   c1.Update()

   # create hint1 filled with the bins integral of h1
   # ------------------------------------------------
   hint1 = TH1F("hint1","h1 bins integral",100,-3,3)
   sum = 0.0;
   for i in range(100):
      sum = sum + h1.GetBinContent(i)
      hint1.SetBinContent(i,sum)

   # scale hint1 to the pad coordinates
   # ----------------------------------
   rightmax = 1.1*hint1.GetMaximum()
   scale = gPad.GetUymax()/rightmax
   hint1.SetLineColor(ROOT.kRed)
   hint1.Scale(scale)
   hint1.Draw("same")

   # draw an axis on the right side
   # ------------------------------
   axis = TGaxis(gPad.GetUxmax(), gPad.GetUymin(),
                 gPad.GetUxmax(), gPad.GetUymax(),0,rightmax,510,"+L")
   axis.SetLineColor(ROOT.kRed)
   axis.SetTextColor(ROOT.kRed)
   axis.Draw()
   return c1
'''


