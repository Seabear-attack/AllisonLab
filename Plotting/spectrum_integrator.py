# open one csv file
import pandas as pd
import easygui as eg
import numpy as np
import matplotlib.pyplot as plt
import os


def OpenCSVFiles(dirName):
    directory = eg.diropenbox(default=dirName)
    filenames = os.listdir(directory)
    print('changing the root directory to:\t' + directory)
    print('filenames are:\t', filenames)
    return directory, filenames


def integrate_power(spectrum_intensity, lower_bound,
                    upper_bound, total_pwr):
    # calculate the dispersive wave ratio to the total power
    wavelength = spectrum_intensity[0]
    spectrum_intensity = spectrum_intensity[1]
    section_power = np.sum(spectrum_intensity[((wavelength < upper_bound) & (wavelength > lower_bound))])
    integral_power = np.sum(spectrum_intensity)
    print('Power of the selected section: \t', total_pwr * (section_power / integral_power))
    print('Total power is: \t', total_pwr)
    print('The power ratio between dispersive wave and total power is: \t', section_power / integral_power)
    eg.msgbox(msg = f'Power in range {lower_bound}-{upper_bound}nm: \t {total_pwr * (section_power / integral_power):.1f} mW\n'
                    f'Total power is: \t {total_pwr:.1f} mW\n'
                    f'The power ratio between dispersive wave and total power is: \t {100 * section_power / integral_power:.1f}%')

if __name__ == "__main__":
    directory, filenames = OpenCSVFiles(r'C:\Users\wahlm\Documents\School\Research\Allison')

    # loop through all files in the directory

    dfs = []
    for filename in filenames:
        # check if file ends with .csv or .txt
        if filename.endswith('.csv') or filename.endswith('.txt') or filename.endswith('.CSV'):
            df = pd.read_csv(os.path.join(directory, filename), skiprows = 4)
            dfs.append(df)
        if filename.endswith('.xls') or filename.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(directory, filename), sheet_name=1)
            dfs.append(df)

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(20, 8))

    Label1 = ['4x 1.15A', '4x 1.2A', '4x 1.25A', '4x 1.175A', '4x 1.2A', '4x 1.225A', '4x 1.25A']
    spectra = []
    for i in range(len(dfs)):
        df_new = dfs[i].iloc[:, :2]  # select first two column
        df_new_numeric = df_new.applymap(
            lambda x: pd.to_numeric(x, errors='coerce')).dropna()  # select only numerical rows
        WaveLength = np.array(df_new_numeric.iloc[:, 0].values, dtype='float64')
        SpectrumIntensity = np.array(df_new_numeric.iloc[:, 1].values, dtype='float64')
        if SpectrumIntensity[int(len(SpectrumIntensity)/2)] < 0:
            SpectrumIntensity = np.power(10, SpectrumIntensity/10)
        spectra.append(np.array([WaveLength, SpectrumIntensity]))
        ax.plot(WaveLength, SpectrumIntensity, label=Label1[i])
    # Add axis labels and a legend
    ax.set_xlabel('wavelength (nm)')
    ax.set_ylabel('power')
    ax.legend()
    # ax.set_title()


    # Display the plot
    plt.tight_layout()
    plt.show(block = False)

    response = eg.multenterbox(fields = ['Plot # (0 indexed)',
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