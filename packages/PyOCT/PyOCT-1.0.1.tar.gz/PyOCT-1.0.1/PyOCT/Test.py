import os 
import numpy as np 
import xml.etree.ElementTree as ET
import time
from scipy.linalg import dft
import numpy.matlib 
import matplotlib.pyplot as plt 
import matplotlib 
from PyOCT import PyOCTRecon 
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

def OCTReconTest():
    root = tk.Tk()
    root_dir = filedialog.askdirectory(parent = root,initialdir="/",title='Please select a directory to load and save data...')
    sampleID_full =  askopenfilename(filetypes=[("Binary files", "*.bin")],title="Please select your data file")
    sampleID = os.path.basename(sampleID_full)
    sampleID = sampleID[0:-8]
    bkgndID_full = askopenfilename(filetypes=[("Binary files", "*.bin")],title="Please select your Background file") 
    bkgndID = os.path.basename(bkgndID_full)
    root.destroy()
    OCTRe = OCTImagingProcessing(root_dir,sampleID,bkgndID,frames=3,alpha2=-50,alpha3=-12,saveOption=False)  
    OCTRe.ShowXZ(OCTRe.OCTData) 
    plt.show() 