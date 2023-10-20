# Plots every spectrum in a user-selected folder. Works for the Yokogawa spectrometer.
import matplotlib.pyplot as plt
from utils.spectrometerdata import OSAData, readFromFiles
from pathlib import Path

if __name__ == "__main__":
    directorypath = Path(
        r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and Spectrum Generation\10-20-23 ADHNLF Spectra\Slow axis')
    raw_data = readFromFiles(directorypath)
    labels = ('7cm LD-ADHNLF 4A',
              '7cm LD-ADHNLF 3.3A'
              )
    powers_mW = [200,
                    178]

    data = [OSAData(dat, ('nm', 'dBm/nm'), labels[i], powers_mW[i], frep_MHz=60.5) for i, dat in enumerate(raw_data)]

    fig, axs = plt.subplots(2, 1, sharex=True)

    for datum in data:
        datum.y_axis_units = 'dBm/nm'
        axs[0].plot(datum._x_axis_data, datum.y_axis_data, label=datum.label)
    axs[0].set_xlabel('Wavelength (nm)')
    axs[0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    axs[0].legend()
    # axs[0, 0].set_title('ADHNLF Spectra')

    for datum in data:
        datum.y_axis_units = 'mW/nm'
        axs[1].plot(datum._x_axis_data, datum.y_axis_data, label=datum.label)
    axs[1].set_xlabel('Wavelength (nm)')
    axs[1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    # axs[1].set_title('Varying Input Pulse Power')

    directorypath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Data for Papers\Tunable seed\Spectrum vs. pulse pattern\4cm NDHNLF + 42cm PM1550')
    raw_data = readFromFiles(directorypath)

    labels = (r'4cm NDHNLF 4A',
            r'$f_{rep}/10$',
            r'$f_{rep}/100$',
            'background')
    frep_frac = [1, 1/10, 1/100, 0]
    is_background = (False, False, False, True)   
    powers_mW = [191, 33, 15.37, 13.9]

    data = [OSAData(dat, ('nm', 'dBm/nm'), labels[i], powers_mW[i], frep_MHz=frep_frac[i] * 60.56, is_background=is_background[i]) for i, dat in enumerate(raw_data)]
    data = data[:-1]

    for datum in data[0:1]:
        datum.y_axis_units = 'dBm/nm'
        axs[0].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[0].set_xlabel('Wavelength (nm)')
    axs[0].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    # axs[0, 1].set_title('NDHNLF Spectrum')
    axs[0].legend()
    
    for datum in data[0:1]:
        datum.y_axis_units = 'mW/nm'
        axs[1].plot(datum.x_axis_data, datum.y_axis_data, label=datum.label)
    axs[1].set_xlabel('Wavelength (nm)')
    axs[1].set_ylabel(f'Spectral Power ({data[0].y_axis_units})')

    for ax in axs.flatten():
        ax.set_xlim([1000, 2000])
    axs[0].set_ylim([-45, 10])
    axs[0].set_ylim([-45, 10])
    # axs[1, 0].set_ylim([-.05, .5])
    # axs[1, 1].set_ylim([-.05, .5])
    fig.canvas.manager.window.showMaximized()  # toggle fullscreen mode
    plt.tight_layout()
    plt.show()
