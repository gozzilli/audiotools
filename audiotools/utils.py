FORMAT = 'pgf' ## please only set 'pgf' or 'pdf'
DEPLOY = True
DPI    = 150
OUTPUT_DIR = 'generated'

FORCE_HILBERT = False

import sys
import struct

import os.path
from   scipy.io import wavfile       # wave file support
import scipy.signal                  # filters and what not
import numpy as np                   # other mathematical library
#from matplotlib import pyplot as plt # plotting
import pickle                        # avoid running results a million times
import shutil, glob
import wavio

def open_audio_simple(filename):
    '''
    open audio file with scipy or audiolab, depending on what is available.
    Return data, fs, enc
    '''
    
    fs, data = wavfile.read(filename)
    enc = None
    #data, fs, enc = audiolab.wavread(sound) # same with audiolab
        
    # if the audio sample is stereo, take only one channel. May not work as
    # desired if the two channels are considerably different.
    
    if len(data.shape) > 1:
        data = data[:,1] 
    
    return (data, fs, enc)


class NotAWaveFileError(Exception):
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return "%s is not a WAVE file" % self.filename
    
def open_audio(filename):
    '''
    open audio file with scipy or audiolab, depending on what is available.
    Return data, fs, enc
    '''
    
    if not filename.lower().endswith(".wav"):
        raise NotAWaveFileError(filename)
    try:
        fs, data = wavfile.read(filename)
    except:
        fs, sampwidth, data = wavio.readwav(filename)
        print "\t%s is a %dbit audio file" % (os.path.basename(filename), 8*sampwidth)
        
    enc = None
    #data, fs, enc = audiolab.wavread(sound) # same with audiolab
        
    # if the audio sample is stereo, take only one channel. May not work as
    # desired if the two channels are considerably different.
    
    if len(data.shape) > 1:
        data = data[:,-1]
    
    return (data, fs, enc)

def downscale(data, time):
    data2 = []
    t2 = []
    q = 500
    r = 2*q
    for i in range(0,len(data),r):
        data2.append(max(data[i:i+r]))
        data2.append(min(data[i:i+r]))
        try:
            t2.append(time[i+int(0.25*r)])
            t2.append(time[i+int(0.75*r)])
        except:
            #print i+int(0.75*r)
            pass
    #plt.gca().get_xaxis().set_visible(False)
    data2 = data2[:len(t2)]
    return data2, t2

def savefig(filename, dpi=DPI):

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    plt.savefig(os.path.join(OUTPUT_DIR, 
                             "%s.%s" %(filename,FORMAT)
                ), dpi=dpi)


def hilbert(sound, data):
    if not FORCE_HILBERT:
        hilbert = pickle.load( open( sound+'-envelope.data', 'rb' ) )
        print "hilbert loaded from pickle"
    else:
        print "starting hilbert"
        hilbert = abs(scipy.signal.hilbert(data))
        print "done hilbert"
        pickle.dump( hilbert, open(sound+'-envelope.data', 'wb') )
        print "hilbert pickled to file"
    return hilbert

def mkdir(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)
        