# Plots every spectrum in a user-selected folder. Works for the Yokogawa spectrometer.
import matplotlib.pyplot as plt
from spectrometer_data import SpectrumData, readFromFiles
import re

if __name__ == "__main__":
    raw_data = readFromFiles(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                             r'Control\9-8-23 Spectra by Input Power\Varying pulse energy\Output 1')
    # labels = ('1111111111111111111',
    #           '1111111111000000000',
    #           '1010101010101010101',
    #           '1111100000000000000',
    #           '1010010001000010000',
    #           '0000000000000000000')
    labels = ('2.65 mW', '1.966 mW', '1.676 mW', '1.054 mW')
    powers_mW = (2.65, 1.966, 1.676, 1.054)
    data = [SpectrumData(dat, ('nm', 'dBm'), labels[i], powers_mW[i]) for i, dat in enumerate(raw_data)]

    fig, ax = plt.subplots(figsize=(20, 8))

    for datum in data:
        ax.plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    ax.legend()
    ax.set_title('Varying Input Pulse Power')
    plt.show(block=False)

    fig, ax = plt.subplots(figsize=(20, 8))

    for datum in data:
        datum.y_axis_units = 'nJ/nm'
        ax.plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    ax.legend()
    ax.set_title('Varying Input Pulse Power')
    plt.show()
