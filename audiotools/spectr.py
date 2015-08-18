import argparse
import os                       # for directory and file manipulation. Not always needed

import scipy                    # mathematical library
import numpy as np              # other mathematical library
# from scikits import audiolab  # read audio files
from scipy.io import wavfile  # wave file support
from utils import open_audio, downscale    # utilities to open and manipulate audio files


def __init__():
    
    global matplotlib, plt
    
    import matplotlib
    if not _show:
        matplotlib.use('agg')
        
    from matplotlib import pyplot as plt
    
    from matplotlib import rc, font_manager, rcParams
    
    if _use_latex:
        rc('text', usetex=True)
        rc('font', family='serif')
        
    #rc('font', family='Times New Roman')
    rc('font', family='Helvetica Neue')
    # rc('font', family='Segoe UI')
    # rcParams['font.family'] = "FreightSans"
    # 
    # rc('font', weight='light')
    # rc('font', size='50.0')
    matplotlib.rcParams.update({
        "savefig.bbox" : "tight",
    })
    
_use_latex = False
_dpi       = 150
_color     = '#005c84'
_show      = False

def spectr_wave(sound):
    ''' 
    Same as `audiolab_test2`, except that also:
    
    * improved version
    '''
    
    (data, fs, enc) = open_audio(sound)
#     data = data[fs*15:fs*58]

    
    fig = plt.figure(figsize=(10,8))
    fig.subplots_adjust(hspace=0.2,)
    
    ax1 = plt.subplot2grid((6,1), (4,0), rowspan=2)    
    ax2 = plt.subplot2grid((6,1), (0,0), rowspan=4)
    
    ### PLOT 1 - Waveform      
    t = np.linspace(0, len(data)/float(fs), len(data))
    
    # if necessary, downscale the waveform
    ax = ax1
    d_data, d_time = downscale(data, t)
    #d_data, d_time = data, t

    ax.tick_params(labelleft='off')
    ax.autoscale(tight=True)
    ax.set_ylabel("Amplitude", labelpad=22)
    ax.plot(d_time, d_data, color=_color, rasterized=True)
    ax.set_xlabel("Time (s)")

    ### PLOT 2 - Spectrogram
    ax = ax2
    specgram = ax.specgram(data, Fs = fs,
                           #cmap='PiYG',
                           rasterized=True)
    
    ax.autoscale(tight=True)           # no space between plot an axes
    #ax.get_xaxis().set_visible(False) # remove the x tick for top plot
    yticks = np.arange(0,fs/2,5000)    # |
    ax.set_yticks(yticks)              # |
    ax.set_yticklabels(yticks/1000)    # |
    ax.set_ylabel("Frequency (kHz)")        # |> change Hz to kHz
    ax.tick_params(labelbottom='off') # labels along the bottom edge are off        


    if _show:
        plt.show()
    else:
        plt.savefig(_pdffilename, dpi=_dpi)
        print "output in {}".format(_pdffilename)
    
def main():
    
    parser = argparse.ArgumentParser(
        description='Plot a spectrogram and a waveform')
    
    parser.add_argument('soundfile', metavar='filename', type=str,
                       help='the sound file to plot')
    parser.add_argument('--latex', action='store_true', help='use latex')
    parser.add_argument('-o', '--output', action='store',
                        help='output file')
    parser.add_argument('-d', '--dpi', action='store',
                        help='dpi (default 150)')
    parser.add_argument('-c', '--color', action='store',
                        help='waveform color')
    parser.add_argument('--show', action='store_true',
                        help='open a window instead of saving to file')
    parser.add_argument('--format', action='store', choices=['png', 'pdf', 'svg'],
                        default="png",
                        help='output plot format')
    
    
    args = parser.parse_args()
    
    global _dpi, _color, _show, _pdffilename, _format

    _use_latex = args.latex
    
    
    _format      = args.format
    _pdffilename = args.output if args.output else 'spectr-wave-%s.%s' % (os.path.basename(args.soundfile)[0:-4], _format)
    _dpi         = args.dpi    if args.dpi    else _dpi
    _color       = args.color  if args.color  else _color
    _show        = args.show
    
    __init__()
    
    spectr_wave(args.soundfile)
    
if __name__ == "__main__":
    
    main()