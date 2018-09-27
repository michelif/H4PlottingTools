#!/bin/python

import sys
import re
import time
import argparse
import os
import subprocess
import array
import string
import ROOT
import math

from ROOT import std
from optparse import OptionParser

vstring = std.vector(std.string)
vfloat = std.vector(float)

#----function to book histos
def bookHistos(histos,run):
    histos["amp_max_B1"]=ROOT.TH1F("h_amp_max_B1","h_amp_max_B1",10000,0,16000);

#-----main function-----
def main():
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
    ROOT.gSystem.Load("../H4Analysis/CfgManager/lib/libCFGMan.so")
    parser = argparse.ArgumentParser (description = 'Draw plots from ROOT files')
    parser.add_argument("-r", "--run", default='100',metavar='run',type=int,
                      help="run number")
    parser.add_argument("-p", "--prefix", default='',metavar='prefix',type=str,
                      help="prefix")
    parser.add_argument("-i", "--inputDir", default='/eos/cms/store/caf/user/micheli/H2spikes/ntuples_20190926_12314/',metavar='inputDir',type=str,
                      help="prefix")

    args = parser.parse_args()
    run = args.run
    prefix = args.prefix
    inputDir = args.inputDir

    print "opening file ",inputDir+"spikes_"+str(run)+".root"

    file=ROOT.TFile(inputDir+"spikes_"+str(run)+".root")
    tree=file.Get("h4")

    outPath="plots/"+str(run)+"/"

    
    if not os.path.exists(outPath):
        os.mkdir(outPath)

    
    outfile=ROOT.TFile(outPath+"plots_"+prefix+"_"+str(run)+".root","recreate")
#----histo definition---- 
    histos={}
    bookHistos(histos,run)
    
#----loop over entries-----
    for entry in tree:
        if entry.index % 1000 ==0:
            print "Analyzing event:"
            print entry.index
        
        histos["amp_max_B1"].Fill(entry.amp_max[entry.B1])

    

    for x in histos:
        c1 = ROOT.TCanvas()
        histos[x].Draw()
        for format in ".png",".pdf",".C":
            c1.SaveAs(outPath+str(x)+format)
            c1.SetLogy()
            c1.SaveAs(outPath+str(x)+"_log"+format)
            c1.Delete()

    outfile.Write()
    outfile.Close()

### MAIN ###
if __name__ == "__main__":
    main()
