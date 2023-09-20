# Plots every scope lineout in user-selected folder. Works for Tektronix scopes
from Plotting.utils.plotting_utils import directory_to_dataframes, get_scope_data, normalize_by_maximum
import matplotlib.pyplot as plt
from Plotting.utils.spectrometerdata import RFSAData, readFromFiles
import numpy as np
from pathlib import Path

if __name__ == "__main__":
    dfs = directory_to_dataframes(Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                                       r'Control\9-19-23 Pre, Post EDFA Pulses\Tektronix Scope'))
    labels = ('Background',
              'f_rep horizontal',
              'f_rep/2 horizontal',
              'f_rep/4 horizontal',
              'f_rep vertical',
              'f_rep/2 vertical',
              'f_rep/4 vertical')
    data = get_scope_data(dfs, labels)
    normalize_by_maximum(data, 'voltage_V')
    plot_order = [0, 1, 3, 5, 2, 4, 6]

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(1, 2, figsize=(20, 8))

    for i, tup in enumerate(sorted(data.items(), key=lambda x: plot_order[labels.index(x[0])])):
        ax[0].plot(tup[1]['time_s'], tup[1]['voltage_V'] - i * 1.1, label=tup[0])
    # Add axis labels and a legend
    ax[0].set_xlabel('Time [s]')
    ax[0].set_ylabel('Voltage [V]')
    ax[0].legend()
    ax[0].set_title('Scope Trace of Pulse Selection, 1.1 V Offset')

    raw_data = readFromFiles(Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                                  r'Control\9-19-23 Pre, Post EDFA Pulses\Rigol RF Spectrum Analyzer'), skip_header=2)
    labels = ('Background',
              'f_rep vertical',
              'f_rep/2 vertical',
              'f_rep/4 vertical',
              'f_rep horizontal',
              'f_rep/2 horizontal',
              'f_rep/4 horizontal')

    data = [RFSAData(np.array([dat[:, 0], dat[:, 2]]).transpose(), ('Hz', 'dBm'), labels[i], frep_MHz=60.5) for i, dat
            in enumerate(raw_data)]
    plot_order = [0, 2, 4, 6, 1, 3, 5]

    for i, datum in enumerate(sorted(data, key=lambda data: plot_order[labels.index(data.label)])):
        ax[1].plot(datum.x_axis_data, datum.y_axis_data - i * 25, label=datum.label)
    ax[1].set_xlim([0, 2.5e8])
    ax[1].set_ylim([-210, -30])
    ax[1].set_xlabel(f'Frequency ({data[0].x_axis_units})')
    ax[1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    ax[1].legend()
    ax[1].set_title('RF Spectrum of Pulse Selection, 25 dB Offset')
    fig.canvas.manager.window.showMaximized()  # toggle fullscreen mode
    plt.tight_layout()
    plt.show()
