# open one csv file
import matplotlib.pyplot as plt
import easygui as eg
from utils.spectrometerdata import readFromFiles, OSAData
from pathlib import Path

if __name__ == "__main__":
    directorypath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and '
                         r'Spectrum Generation\9-21-23 Tunable seed spectrum optimization\OAP\ADHNLF')
    raw_data = readFromFiles(directorypath)
    labels = ('0s, 4A',
              '0s, 3.75A',
              '0s, 3.5A',
              '0s, 3.25A',
              '0s, 3A',
              '1s, 4A',
              '1s, 3.75A',
              '1s, 3.5A',
              '1s, 3.25A',
              '1s, 3A',
              '1s, 2.75A'
              )

    powers_mW = (201,
                 194,
                 185,
                 176,
                 169,
                 196,
                 189,
                 181,
                 173,
                 166,
                 155)

    data = [OSAData(dat, ('nm', 'dBm'), labels[i], powers_mW[i], frep_MHz=60.5) for i, dat in enumerate(raw_data)]

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(20, 8))

    for i, dat in enumerate(data):
        dat.y_axis_units = 'mW/nm'
        ax.plot(dat.x_axis_data, dat.y_axis_data, label=f'#{i}: {dat.label}')
    # Add axis labels and a legend
    ax.set_xlabel(f'Wavelength ({data[0].x_axis_units})')
    ax.set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    # ax.set_ylim([-60, 0])
    ax.legend()
    ax.set_title('ADHNLF Spectra')
    plt.vlines(1300, min(data[0].y_axis_data), max(data[0].y_axis_data), colors='k')
    plt.vlines(1800, min(data[0].y_axis_data), max(data[0].y_axis_data), colors='k')

    # Display the plot
    fig.canvas.manager.window.showMaximized()  # toggle fullscreen mode
    plt.tight_layout()
    plt.show(block=False)

    response = eg.multenterbox(fields=['Plot # (0 indexed)',
                                       'Lower bound [nm]',
                                       'Upper bound [nm]'])
    while response is not None:
        spectrum = data[int(response[0])]
        lower = int(response[1])
        upper = int(response[2])
        eg.msgbox(f'Power: {spectrum.integral(lower_bound=lower, upper_bound=upper)} mW')
        response = eg.multenterbox(fields=['Plot # (0 indexed)',
                                           'Lower bound [nm]',
                                           'Upper bound [nm]'
                                           ])
