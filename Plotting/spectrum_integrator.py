# open one csv file
import pandas as pd
import easygui as eg
import numpy as np
import matplotlib.pyplot as plt
import os

import spectrometerdata as sd

if __name__ == "__main__":

    arrays = sd.readFromFiles(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                                  r'Control\9-8-23 Spectra by Input Power\Varying pulse energy\Output 1')
    labels = ('1.054 mW',
              '1.676 mW',
              '1.966 mW',
              '2.65 mW')

    spectrum_powers()
    data = []
    for datum in arrays:
        data.append(sd.OSAData(datum, ('nm', 'dBm', labels,)))
    # loop through all files in the directory

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(20, 8))


    # Add axis labels and a legend
    ax.set_xlabel('wavelength (nm)')
    ax.set_ylabel('power')
    ax.legend()
    # ax.set_title()

    # Display the plot
    plt.tight_layout()
    plt.show(block=False)

    response = eg.multenterbox(fields=['Plot # (0 indexed)',
                                       'Lower bound [nm]',
                                       'Upper bound [nm]',
                                       'Total power [mW]'])
    while response is not None:
        spectrum = spectra[int(response[0])]
        lower = int(response[1])
        upper = int(response[2])
        power = int(response[3])
        integrate_power(spectrum, lower, upper, power)
        response = eg.multenterbox(fields=['Plot # (0 indexed)',
                                           'Lower bound [nm]',
                                           'Upper bound [nm]',
                                           'Total power [mW]'])
