# open one csv file
import pandas as pd
import easygui as eg
import numpy as np
import matplotlib.pyplot as plt
import os


def OpenCSVFiles(dirName):
    directory = eg.diropenbox(default=dirName)
    filenames = os.listdir(directory)
    return directory, filenames


if __name__ == "__main__":
    home_path = r'C:\Users\wahlm\Documents\School\Research\Allison'
    directory, filenames = OpenCSVFiles(home_path)
    # curve_labels = ['4x 1.15A', '4x 1.2A', '4x 1.25A', '4x 1.175A', '4x 1.2A', '4x 1.225A', '4x 1.25A']
    curve_labels = ['11111111111111111110', '10101010101010101010',
                    '10000000000000000000', '10100100010000100000',
                    '11111111110000000000', '10001000100010001000']
    # curve_powers_mW = [237, 248, 253, 250, 250, 250, 250, 250]
    # curve_powers_mW = [240, 240, 240, 240, 240, 240, 240]
    # curve_powers_nJ = [4, 4, 4, 4, 4, 4]

    while directory is not None:
        title, pulse_energy_nj = eg.multenterbox(fields = ["Title", "Pulse energy (nJ)"])
        pulse_energy_nj = float(pulse_energy_nj)
        # loop through all files in the directory

        dfs = []
        for filename in filenames:
            # check if file ends with .csv or .txt
            if filename.endswith('.csv') or filename.endswith('.txt') or filename.endswith('.CSV'):
                df = pd.read_csv(os.path.join(directory, filename), skiprows=4)
                dfs.append(df)
            if filename.endswith('.xls') or filename.endswith('.xlsx'):
                df = pd.read_excel(os.path.join(directory, filename), sheet_name=1)
                dfs.append(df)

        # Create a figure and axis object using matplotlib
        fig, ax = plt.subplots(figsize=(20, 8))

        spectra = []
        top = 0
        for i in range(len(dfs)):
            df_new = dfs[i].iloc[:, :2]  # select first two column
            df_new_numeric = df_new.applymap(
                lambda x: pd.to_numeric(x, errors='coerce')).dropna()  # select only numerical rows
            WaveLength = np.array(df_new_numeric.iloc[:, 0].values, dtype='float64')
            SpectrumIntensity = np.array(df_new_numeric.iloc[:, 1].values, dtype='float64')
            if SpectrumIntensity[int(len(SpectrumIntensity) / 2)] < 0:
                SpectrumIntensity = np.power(10, SpectrumIntensity / 10)
            # Normalize, assume even sample spacing
            delta_lambda = WaveLength[1] - WaveLength[0]
            integral = np.sum(SpectrumIntensity)
            # SpectrumIntensity = SpectrumIntensity / integral * curve_powers_mW[i] / delta_lambda
            SpectrumIntensity = SpectrumIntensity / integral * pulse_energy_nj / delta_lambda
            if max(SpectrumIntensity) > top:
                top = max(SpectrumIntensity)

            spectra.append(np.array([WaveLength, SpectrumIntensity]))
            ax.plot(WaveLength, SpectrumIntensity, label=curve_labels[i])
        # Add axis labels and a legend
        ax.set_xlabel('wavelength (nm)')
        ax.set_ylabel('Spectral Energy per Pulse (nJ/nm)')
        ax.legend()
        ax.set_title(title)
        plt.semilogy()
        plt.ylim(top * 10 ** (-4), top)
        # Display the plot
        plt.show(block=False)
        plt.tight_layout()
        # response = eg.multenterbox(fields = ['Plot # (0 indexed)',
        #                            'Lower bound [nm]',
        #                            'Upper bound [nm]',
        #                            'Total power [mW]'])
        # while response is not None:
        #     spectrum = spectra[int(response[0])]
        #     lower = int(response[1])
        #     upper = int(response[2])
        #     power = int(response[3])
        #     integrate_power(spectrum, lower, upper, power)
        #     response = eg.multenterbox(fields=['Plot # (0 indexed)',
        #                                        'Lower bound [nm]',
        #                                        'Upper bound [nm]',
        #                                        'Total power [mW]'])
        directory, filenames = OpenCSVFiles(os.path.split(home_path))
