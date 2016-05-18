import ROOT
from ROOT import TCanvas, TF1, TLegend
import glob, re
import logging as l 
from pprint import pprint

def plot_histograms():

   def regex_search(file_name, regex):
      search = re.compile(regex) 
      value = search.search(file_name)
      return value

   def parse_file_names(files):
      energies = []
      for file_name in files:
         zprimexxx = regex_search(file_name,'zprime(\d+)')
         if(zprimexxx):
            energies.append(zprimexxx.group(1))
         else:
            l.ERROR("Error files names not consistent")
      l.debug("File names:"+str(files))
      l.debug("Energies: "+str(energies))
      return energies
   
   Files = glob.glob("outputs/zprime*_000000*z_prime.root")
   energies = parse_file_names(Files)
   Colours = [ROOT.kBlack,ROOT.kBlue, ROOT.kViolet, ROOT.kGreen, ROOT.kRed, ROOT.kOrange]
   print(Colours)
   yx = zip(energies, Files)
   yx.sort()
   pprint(yx)
   yz = zip(energies, Colours)
   yz.sort()
   pprint(yz)
   files = [y for x, y in yx]
   colours = [y for x, y in yz]
   print(files)
   #energies.sort()
   print(energies)
   print(colours)
   #[files for (energies,files) in sorted(zip(Energies,Files),key=lambda pair: pair[0])]
    #[x for (y,x) in sorted(zip(Y,X), key=lambda pair: pair[0])] 
   #files = ["outputs/zprime5000_000005delta_r.root","outputs/zprime2250_000010delta_r.root"]#glob.glob("outputs/zprime*delta_r.root")
   #energies = ["5000","2250"]
   
   entries = ["delta_r", "h_delta_r_top_W", "h_delta_r_top_b","h_z_prime_pt","h_z_prime_eta","h_z_prime_phi", "delta_r_top_jet"]
   l.debug("Files: "+str(files))
   l.debug("Files length: "+str(len(files)))
   
   t = [None]*len(files)
   f = [None]*len(files)
   c = [None]*len(entries)
   ROOT.gStyle.SetOptStat(0);
   for j in xrange(len(entries)):
      c[j] = TCanvas( 'c'+str(j), entries[j], 200, 10, 700, 500)
      leg = TLegend(0.7,0.15,0.85,0.35)
      leg.SetBorderSize(0)
      leg.SetHeader("Z' Mass [GeV]");
      #c[j].SetLogy();
      for i in reversed(xrange(len(files))):
         l.debug("File name:"+files[i])
         l.debug("Energy:"+energies[i])
         l.debug("Entry:"+entries[j])
         l.debug("colours:"+str(colours[i]))
         f[i] = ROOT.TFile.Open(files[i])
         t[i] = f[i].Get(entries[j])
         t[i].SetLineColor(colours[i])
         t[i].SetLineWidth(2);
         t[i].SetName(energies[i])
         leg.AddEntry(t[i],energies[i],"l");
         if (i==len(files)):
            t[i].Draw()
            c[j].Update()
         else:
            t[i].Draw("SAME") #this is required to draw on same canvas
            c[j].Update()
      leg.Draw()
      c[j].Print("overlay_"+entries[j]+".root")
      c[j].Print("overlay_"+entries[j]+".png")
   #ATLASLabel(0.13,0.85,"Work in Progress",1);      



if __name__ == '__main__':
    # setup logger 
    l.basicConfig(level=l.DEBUG, format='%(levelname)s - %(message)s')#%(asctime)s - %(levelname)s - %(message)s')
    plot_histograms()


