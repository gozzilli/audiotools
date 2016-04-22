import argparse
import os                       # for directory and file manipulation. Not always needed
import numpy as np              # other mathematical library
# from scikits import audiolab  # read audio files
from utils import open_audio, downscale    # utilities to open and manipulate audio files

_is_initialised = False
_use_latex   = False
_dpi         = 150
_color       = '#005c84'
_show        = False
_size        = "10x6"
_vmax        = None
_vmin        = None
_colorbar    = False
_pdffilename = None

def __init__():
    
    global matplotlib, plt, _is_initialised
    
    import matplotlib
    if not _show:
        matplotlib.use('pdf')
        
    from matplotlib import pyplot as plt  # @UnusedImport
    from matplotlib import rc
    
    if _use_latex:
        rc('text', usetex=True)
        rc('font', family='serif')
        
    ## more parameters in comments below
    rc('font', family='Helvetica Neue')
    
    matplotlib.rcParams.update({
        "savefig.bbox" : "tight",
    })
    
    _is_initialised = True


def spectr_wave(sound):
    ''' 
    Same as `audiolab_test2`, except that also:
    
    * improved version
    '''
    
    if not _is_initialised:
        ## not coming from main()
        global _show
        _show = True
        __init__()
    
    (data, fs, _) = open_audio(sound)
    # data = data[fs*15:fs*58]

    figsize = tuple([int(x) for x in _size.split("x")])
    
    fig = plt.figure(figsize=figsize)
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
    
    _, _, _, im = ax.specgram(data, Fs = fs,
                           #cmap='PiYG',
                           rasterized=True,
                           vmin=_vmin, vmax=_vmax)
    
    if _colorbar:
        plt.colorbar(im)
    
    ax.autoscale(tight=True)           # no space between plot an axes
    #ax.get_xaxis().set_visible(False) # remove the x tick for top plot
    yticks = np.arange(0,fs/2,1000)    # |
    ax.set_yticks(yticks)              # |
    ax.set_yticklabels(yticks/1000)    # |
    ax.set_ylabel("Frequency (kHz)")        # |> change Hz to kHz
    ax.tick_params(labelbottom='off') # labels along the bottom edge are off        


    if _show:
        plt.show()
    else:
        if _pdffilename:
            fig.savefig(_pdffilename, dpi=_dpi)
            print "output in {}".format(_pdffilename)
        else:
            print "Warning: output filename not specified and figure.show() disabled."
     
    plt.clf()   
    plt.close(fig)
    
    del fig
    
    
def parse():
    
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
    parser.add_argument('--vmin', action='store', type=int,
                        help='min value for spectrogram')
    parser.add_argument('--vmax', action='store', type=int,
                        help='max value for spectrogram')
    parser.add_argument('-s', '--size', action='store',
                        help='image size in inches WxH (e.g. 12x7)')
    parser.add_argument('--show', action='store_true',
                        help='open a window instead of saving to file')
    parser.add_argument('--colorbar', action='store_true',
                        help='add colorbar to spectrogram')
    
    parser.add_argument('-f', '--format', action='store', choices=['png', 'pdf', 'svg'],
                        default="png",
                        help='output plot format')
    
    
    args = parser.parse_args()
        
    global _dpi, _color, _show, _pdffilename, _format, _size, _vmin, _vmax, _colorbar

    _use_latex = args.latex
    
    _format      = args.format
    _pdffilename = args.output if args.output else 'spectr-wave-%s.%s' % (os.path.basename(args.soundfile)[0:-4], _format)
    _dpi         = args.dpi    if args.dpi    else _dpi
    _color       = args.color  if args.color  else _color
    _show        = args.show   if args.show   else _show
    _size        = args.size   if args.size else _size
    _vmin        = args.vmin  
    _vmax        = args.vmax 
    _colorbar    = args.colorbar
    
    if len(_size.split('x')) != 2:
        raise ValueError("size much be in inches in the format WxH (e.g. 12x7)")
    
    __init__()
    
    return args.soundfile

def main():

    soundfile = parse()
    spectr_wave(soundfile)
    
    #import gc
    #gc.collect()  # don't care about stuff that would be garbage collected properly
    #import objgraph
    #print "objgraph"
    #objgraph.show_most_common_types()
    

if __name__ == "__main__":
    
    main()
    
    
# rc('font', family='Times New Roman')
# rc('font', family='Segoe UI')
# rcParams['font.family'] = "FreightSans"
# 
# rc('font', weight='light')
# rc('font', size='50.0')