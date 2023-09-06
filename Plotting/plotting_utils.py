import easygui as eg
import os
import numpy as np


def OpenCSVFiles(dirName):
    directory = eg.diropenbox(default=dirName)
    filenames = os.listdir(directory)
    return directory, filenames


def integrate_power(spectrum_intensity, wl_lower_bound,
                    wl_upper_bound, total_pwr):
    # calculate the dispersive wave ratio to the total power
    wavelength = spectrum_intensity[0]
    spectrum_intensity = spectrum_intensity[1]
    section_power = np.sum(spectrum_intensity[((wavelength < wl_upper_bound) & (wavelength > wl_lower_bound))])
    integral_power = np.sum(spectrum_intensity)
    print('Power of the selected section: \t', total_pwr * (section_power / integral_power))
    print('Total power is: \t', total_pwr)
    print('The power ratio between dispersive wave and total power is: \t', section_power / integral_power)
    eg.msgbox(
        msg=f'Power in range {wl_lower_bound}-{wl_upper_bound}nm: \t {total_pwr * (section_power / integral_power):.1f} mW\n'
            f'Total power is: \t {total_pwr:.1f} mW\n'
            f'The power ratio between dispersive wave and total power is: \t {100 * section_power / integral_power:.1f}%')
