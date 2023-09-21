# open one csv file
import matplotlib.pyplot as plt
import easygui as eg
from utils.spectrometerdata import readFromFiles, OSAData
from pathlib import Path

if __name__ == "__main__":
    directorypath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and '
                             r'Spectrum Generation\9-21-23 Tunable seed spectrum optimization\Yokogawa OSA')
    raw_data = readFromFiles(directorypath)
    labels = ('1s',
              '0s')

    powers_mW = (208, 204)

    data = [OSAData(dat, ('nm', 'dBm'), labels[i], powers_mW[i], frep_MHz=60.5) for i, dat in enumerate(raw_data)]

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(20, 8))

    for dat in data:
        dat.y_axis_units = 'mW'
        ax.plot(dat.x_axis_data, dat.y_axis_data, label=dat.label)
    # Add axis labels and a legend
    ax.set_xlabel(f'Wavelength ({data[0].x_axis_units})')
    ax.set_ylabel(f'Spectral Power ({data[0].y_axis_units})')
    # ax.set_ylim([-60, 0])
    ax.legend()
    # ax.set_title()

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
