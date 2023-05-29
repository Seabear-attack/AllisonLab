# Plots every scope lineout in user-selected folder.
import os
import easygui as eg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def OpenCSVFiles(dirName):
    directory = eg.diropenbox('Open me', 'this one', dirName)
    filenames = os.listdir(directory)
    print('changing the root directory to:\t' + directory)
    print('filenames are:\t', filenames)
    return directory, filenames


if __name__ == "__main__":
    directory, filenames = OpenCSVFiles(r'C:\Users\wahlm\Documents\School\Research\Allison')

    # loop through all files in the directory

    dfs = []
    for filename in filenames:
        # check if file ends with .csv or .txt
        if filename.endswith('.csv') or filename.endswith('.txt') or filename.endswith('.CSV'):
            # read the data from the file into a pandas dataframe
            # print('reading:',os.path.join(directory, filename))
            df = pd.read_csv(os.path.join(directory, filename), header = None, usecols = [0, 1, 3, 4])
            dfs.append(df)
        if filename.endswith('.xls') or filename.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(directory, filename), sheet_name=1)
            dfs.append(df)

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(20, 8))

    # Label1 = ['All 1.2A','3*1.2A+800mA','3*1.2A+700mA','3*1.2A+650mA','3*1.2A+500mA']
    Label1 = ['All 1.2A', '3*1.2A+1A', '3*1.2A+0.9A', '3*1.2A+0.8A', '3*1.2A+0.7A', '3*1.2A+0.54A', '???', 'NA2']

    for i in range(len(dfs)):
        df_new = dfs[i].iloc[:, 2:]  # select the data columns
        df_new_numeric = df_new.applymap(
            lambda x: pd.to_numeric(x, errors='coerce')).dropna()  # select only numerical rows
        # df_new_numeric = df_new_numeric[df_new_numeric.iloc[:,0]>1600]
        time = np.array(df_new_numeric.iloc[:, 0].values, dtype='float64')
        voltage = np.array(df_new_numeric.iloc[:, 1].values, dtype='float64')
        ax.plot(time, voltage, label=Label1[i])
        # ax.semilogy(WaveLength, SpectrumIntensity, label=Label1[i % len(Label1)]+' '+Label2[i//len(Label1)], linestyle = Linestyle[i//len(Label1)],color = LineColor[i%len(Label1)])
    # Add axis labels and a legend
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Voltage [V]')
    ax.legend()
    ax.set_title(
        'Spectrum of 44.5cm of pm1550 +4cm of 2.2ps/nm/km HNLF for different EDFA powers - 28.5cm pm1550 + 4cm HNLF splice')

    # plt.ylim(-50,1)
    # Display the plot
    plt.show()
