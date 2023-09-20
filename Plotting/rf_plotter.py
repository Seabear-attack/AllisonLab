from spectrometerdata import readFromFiles, SpectrumData
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from plottingutils import offset

if __name__ == "__main__":
    raw_data = readFromFiles(Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                                  r'Control\9-19-23 Pre, Post EDFA Pulses\Rigol RF Spectrum Analyzer'),
                             device='rigol_rfsa')
    labels = ('Background',
              'f_rep, vertical',
              'f_rep/2, vertical',
              'f_rep/4, vertical',
              'f_rep, horizontal',
              'f_rep/2, horizontal',
              'f_rep/4, horizontal')
    data = [SpectrumData(np.array([dat[:, 0], dat[:, 2]]).transpose(), ('Hz', 'dBm'), data_label=labels[i], frep_MHz=60.5) for i, dat in enumerate(raw_data)]
    fig, axs = plt.subplots()

    for datum in data:
        axs.plot(datum.axes[0].data, datum.axes[1].data)
    axs.set_xlabel(f'Frequency ({data[0].axes[0].label})')
    axs.set_ylabel(f'Spectral Power ({data[0].axes[1].label})')
    axs.legend()
    axs.set_title('Varying Input Pulse Pattern, Output 1')
    plt.show()
    #
    # for datum in data[:-1]:
    #     datum.y_axis_units = 'nJ/nm'
    #     axs[1, 0].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    # axs[1, 0].set_xlabel('Wavelength (nm)')
    # axs[1, 0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
