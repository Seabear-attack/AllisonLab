# Plots every spectrum in a user-selected folder. Works for the Yokogawa spectrometer.
import matplotlib.pyplot as plt
from Plotting.utils.spectrometerdata import OSAData, readFromFiles
from pathlib import Path

if __name__ == "__main__":
    directorypath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and '
                         r'Spectrum Generation\9-21-23 Tunable seed spectrum optimization\Lens\NDHNLF\Yokogawa OSA')
    raw_data = readFromFiles(directorypath)
    labels = ('1s, 4A',
              '0s, 4A'
              )
    powers_mW = [208,
                 204]

    data = [OSAData(dat, ('nm', 'dBm'), labels[i], powers_mW[i], frep_MHz=60.5) for i, dat in enumerate(raw_data)]

    fig, axs = plt.subplots(2, 2)

    for datum in data[:1]:
        datum.y_axis_units = 'dBnJ/nm'
        axs[0, 0].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[0, 0].set_xlabel('Wavelength (nm)')
    axs[0, 0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    axs[0, 0].legend()
    axs[0, 0].set_title('NDHNLF Lens Spectra')

    for datum in data[:1]:
        datum.y_axis_units = 'nJ/nm'
        axs[1, 0].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[1, 0].set_xlabel('Wavelength (nm)')
    axs[1, 0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    # axs[1].set_title('Varying Input Pulse Power')

    directorypath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and '
                         r'Spectrum Generation\9-21-23 Tunable seed spectrum optimization\OAP\NDHNLF')
    raw_data = readFromFiles(directorypath)
    powers_mW = [181,
                 174,
                 166,
                 158,
                 151,
                 138,
                 127,
                 183,
                 175,
                 168,
                 159,
                 150]
    labels = ('0s 4A',
              '0s 3.75A',
              '0s 3.5A',
              '0s 3.25A',
              '0s 3A',
              '0s 2.75A',
              '0s 2.5A',
              '1s 4A',
              '1s 3.75A',
              '1s 3.5A',
              '1s 3.25A',
              '1s 3A')

    data = [OSAData(dat, ('nm', 'dBm'), labels[i], powers_mW[i], frep_MHz=60.5) for i, dat in
            enumerate(raw_data)]

    for datum in data[7:8]:
        datum.y_axis_units = 'dBnJ/nm'
        axs[0, 1].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[0, 1].set_xlabel('Wavelength (nm)')
    axs[0, 1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    axs[0, 1].set_title('NDHNLF OAP Spectra')
    axs[0, 1].legend()

    for datum in data[7:8]:
        datum.y_axis_units = 'nJ/nm'
        axs[1, 1].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[1, 1].set_xlabel('Wavelength (nm)')
    axs[1, 1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')

    for ax in axs.flatten():
        ax.set_xlim([1000, 2000])
    axs[0, 0].set_ylim([-45, -5])
    axs[0, 1].set_ylim([-45, -5])
    fig.canvas.manager.window.showMaximized()  # toggle fullscreen mode
    plt.tight_layout()
    plt.show()
