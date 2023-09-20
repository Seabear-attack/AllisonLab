# Plots every spectrum in a user-selected folder. Works for the Yokogawa spectrometer.
import matplotlib.pyplot as plt
from spectrometer_data import SpectrumData, readFromFiles
import numpy as np

if __name__ == "__main__":
    raw_data = readFromFiles(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                             r'Control\9-8-23 Spectra by Input Power\Varying pulse pattern\Output 1')
    labels = ('1111111111111111111',
              '1111111111000000000',
              '1010101010101010101',
              '1111100000000000000',
              '1010010001000010000',
              '0000000000000000000')
    # labels = ('2.65 mW', '1.966 mW', '1.676 mW', '1.054 mW')
    # powers_mW = [281,
    #              297,
    #              301,
    #              309]
    #
    # powers_mW = powers_mW[::-1]

    powers_mW = 303

    # frep = 60.5 * np.array([1, 10 / 19, 10 / 19, 5 / 19, 5 / 19, 0])
    data = [SpectrumData(dat, ('nm', 'dBm'), labels[i], powers_mW, frep_MHz=60.5) for i, dat in enumerate(raw_data)]

    fig, axs = plt.subplots(2, 2)

    for datum in data[:-1]:
        datum.y_axis_units = 'dBnJ/nm'
        axs[0, 0].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[0, 0].set_xlabel('Wavelength (nm)')
    axs[0, 0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    axs[0, 0].legend()
    axs[0, 0].set_title('Varying Input Pulse Pattern, Output 1')

    for datum in data[:-1]:
        datum.y_axis_units = 'nJ/nm'
        axs[1, 0].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[1, 0].set_xlabel('Wavelength (nm)')
    axs[1, 0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    # axs[1].set_title('Varying Input Pulse Power')

    raw_data = readFromFiles(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                             r'Control\9-8-23 Spectra by Input Power\Varying pulse pattern\Output 2')
    # labels = ('1111111111111111111',
    #           '1111111111000000000',
    #           '1010101010101010101',
    #           '1111100000000000000',
    #           '1010010001000010000',
    #           '0000000000000000000')

    #     powers_mW = [312,
    # 312,
    # 307,
    # 291]
    #     labels = ['2.756 mW',
    #                  '2.485 mW',
    #                  '1.69 mW',
    #                  '0.749 mW']
    powers_mW = 311

    data = [SpectrumData(dat, ('nm', 'dBm'), labels[i], powers_mW, frep_MHz=60.5) for i, dat in
            enumerate(raw_data)]

    for datum in data[:-1]:
        datum.y_axis_units = 'dBnJ/nm'
        axs[0, 1].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[0, 1].set_xlabel('Wavelength (nm)')
    axs[0, 1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    axs[0, 1].set_title('Varying Input Pulse Pattern, Output 2')
    axs[0, 1].legend()

    for datum in data[:-1]:
        datum.y_axis_units = 'nJ/nm'
        axs[1, 1].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[1, 1].set_xlabel('Wavelength (nm)')
    axs[1, 1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')

    for ax in axs.flatten():
        ax.set_xlim([1450, 1700])
    axs[0, 0].set_ylim([-50, 5])
    axs[0, 1].set_ylim([-50, 5])
    plt.show()
