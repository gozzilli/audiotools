import numpy as np
from matplotlib import pyplot as plt
plt.style.use("ggplot")
plt.rcParams["axes.grid"] = False

from .utils import open_audio, downscale    # utilities to open and manipulate audio files
from . import config


def waveform(signal, fs, ax=None, figsize=None, color=None):

    if not ax:
        fig, ax = plt.subplots(figsize=figsize)

    color = config.COLOR if not color else color

    ### PLOT 1 - Waveform
    t = np.linspace(0, len(signal) / float(fs), len(signal))

    # if necessary, downscale the waveform
    if len(signal) > 500000:
        print("downscaling signal")
        d_data, d_time = downscale(signal, t)
    else:
        d_data, d_time = signal, t

    # ax.tick_params(labelleft='off')
    ax.autoscale(tight=True)
    ax.set_ylabel("Amplitude", labelpad=22)
    ax.plot(d_time, d_data, color=color, rasterized=True)
    ax.set_xlabel("Time (s)")

    return ax


def spectrogram(data, fs, ax=None, colorbar=False, figsize=None, vmin=None, vmax=None):

    if not ax:
        fig, ax = plt.subplots(figsize=figsize)

    _, _, _, im = ax.specgram(data, Fs=fs, # cmap='PiYG',
                              rasterized=True, vmin=vmin, vmax=vmax)

    if colorbar:
        plt.colorbar(im)

    ax.autoscale(tight=True)  # no space between plot an axes
    # ax.get_xaxis().set_visible(False) # remove the x tick for top plot
    yticks = np.arange(0, fs / 2 + 1, 1000) .astype('i')
    ax.set_yticks(yticks)
    ax.set_yticklabels((yticks / 1000).astype('i'))
    ax.set_ylabel("Frequency (kHz)")  # |> change Hz to kHz

    return ax


def spectr_wave(sound, figsize=None, color=None, colorbar=False, vmin=None, vmax=None):
    """
    Plot a spectrogram and a waveform of a given sound file

    Parameters
    ----------
    sound       sound file path
    figsize
    color       color for the waveform
    colorbar    (bool) show a color bar on the spectrogram?
    vmin        min value of spectrogram
    vmax        max value of spectrogram

    Returns
    -------

    pyplot figure

    """

    (data, fs, _) = open_audio(sound)
    # data = data[fs*15:fs*58]


    figsize = config.FIG_SIZE if not figsize else figsize
    color = config.COLOR if not color else color

    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace=0.2, )

    ax1 = plt.subplot2grid((6, 1), (4, 0), rowspan=2)
    ax2 = plt.subplot2grid((6, 1), (0, 0), rowspan=4)

    ### PLOT 1 - Waveform
    waveform(data, fs, ax=ax1, color=color)

    ### PLOT 2 - Spectrogram
    ax2 = spectrogram(data, fs, ax=ax2, colorbar=colorbar, vmin=vmin, vmax=vmax)
    ax2.tick_params(labelbottom='off')  # labels along the bottom edge are off

    return fig
