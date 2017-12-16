from __future__ import print_function
import os
import argparse

# from scikits import audiolab  # read audio files
from audiotools import utils
from . import config

_is_initialised = False

def matplotlib_init(show=False, use_latex=False):

    global matplotlib, plt, _is_initialised
    
    import matplotlib
    if not show:
        matplotlib.use('pdf')
        
    from matplotlib import pyplot as plt  # @UnusedImport
    from matplotlib import rc
    
    if use_latex:
        rc('text', usetex=True)
        rc('font', family='serif')
        
    ## more parameters in comments below
    rc('font', family='Helvetica Neue')
    
    matplotlib.rcParams.update({
        "savefig.bbox" : "tight",
    })
    
    _is_initialised = True


    
def parse():
    
    parser = argparse.ArgumentParser(
        description='Plot a spectrogram and a waveform')
    
    parser.add_argument('soundfiles', metavar='filename', type=str, nargs='+',
                       help='the sound file to plot')
    parser.add_argument('--latex', action='store_true', help='use latex')
    parser.add_argument('-o', '--output', action='store',
                        help='output file')
    parser.add_argument('-O', '--output-dir', action='store',
                        help='output directory')
    parser.add_argument('-of', '--output-format', action='store',
                        help='output file name format (use {{FN}} for input file name)')
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

    global _dpi, _color, _show, _pdffilename, _pdffileformat, _format, _size, _vmin, _vmax, _colorbar, _outdir

    _use_latex = args.latex
    
    _format      = args.format
    _outdir      = args.output_dir
    _pdffilename = args.output if args.output else ""
    _pdffileformat = args.output_format if args.output_format else None
    _dpi         = args.dpi    if args.dpi    else config.DPI
    _color       = args.color  if args.color  else config.COLOR
    _show        = args.show   if args.show   else config.SHOW
    if args.size and len(args.size.split('x')) != 2:
        parser.error("size much be in inches in the format WxH (e.g. 12x7)")
    _size        = tuple([int(x) for x in args.size.split("x")])   if args.size   else config.FIG_SIZE
    _vmin        = args.vmin
    _vmax        = args.vmax
    _colorbar    = args.colorbar
    
    if _pdffilename and os.path.isabs(_pdffilename) and _outdir:
        parser.error("Output directory specified but output file is an absolute path.")
    
    matplotlib_init(show=_show, use_latex=_use_latex)
    
    return args.soundfiles


def spectr_wave():

    soundfiles = parse()
    from . import spectr  # needs to be after a call to matplotlib_init()

    global _size, _pdffilename, _pdffileformat

    for sf in soundfiles:
        fig = spectr.spectr_wave(sf, figsize=_size, colorbar=_colorbar)

        if _show:
            _be = matplotlib.get_backend()
            if _be in ["pdf", "agg"]:
                raise IOError("Backend '%s' does not support `show()`" % _be)
            plt.show()

        else:
            if _pdffileformat:
                _pdffilename = _pdffileformat.replace("{{FN}}", os.path.basename(sf)[0:-4])
                if not _pdffilename.endswith(_format):
                    _pdffilename += ("."+_format)
            if not _pdffilename:
                _pdffilename = 'spectr-wave-%s.%s' % (os.path.basename(sf)[0:-4], _format)
            if _outdir and _outdir not in _pdffilename:
                utils.mkdir_p(_outdir)
                _pdffilename = os.path.join(_outdir, os.path.basename(_pdffilename))
            fig.savefig(_pdffilename, dpi=_dpi)
            print("output in {}".format(_pdffilename))

            _pdffilename = None # reset at each iteration
            plt.clf()
            plt.close(fig)



if __name__ == "__main__":
    
    parse()