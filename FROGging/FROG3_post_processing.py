# Given a directory, loops through the .csv files corresponding to FROG Traces.
# Creates a new folder containing files compatible with Frog3.exe retrieval software
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path

from matplotlib import ticker
from natsort import natsorted


def readRawFrog(filepath):
    FROGRaw = pd.read_csv(filepath, index_col=0, header=0, dtype=np.float64)  # read as csv with index being the first column(delay)

    FROGRaw.columns = FROGRaw.columns.astype(float)  # the wavelength used to be in string, change it to float!
    return FROGRaw


# shifts the FROG spectrum by -4.893nm because the OSA is not measuring spectrum correctly - tested by the HeNe
def ShiftFrogby5(OriginalFrog):
    ShiftedFROG = OriginalFrog - 4.893
    return ShiftedFROG


if __name__ == "__main__":
    dirpath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization Control\10-4-23 frep over 1000 FROG')
    filepaths = natsorted(dirpath.glob('*[!background].csv'), key=lambda filepath: str(filepath.name))
    show_plots = False
    background_filename = list(dirpath.glob('*background.csv'))[0]
    # background_filename = None
    background_scalefactor = 999/1000
    # zoom in on wavelength
    lowWv = 750
    highWv = 820
    # zoom in on time
    lowT = -1000
    highT = 1000

    if background_filename is not None:
        FROGbackground = readRawFrog(dirpath / background_filename)

    for filepath in filepaths:
        # import data from csv
        FROGRaw = readRawFrog(filepath)
        FROGspectrum = FROGRaw.sum(axis=0)  # sum over the horizontal axis to get the whole spectrum

        if background_filename is not None:
            FROGRaw = FROGRaw - background_scalefactor * FROGbackground

        # Plot original FROG Trace
        print('data opened from:\t' + str(filepath.name))

        if show_plots:
            fig, axe = plt.subplots()
            sns.heatmap(data=FROGRaw, ax=axe)
            plt.show(block=False)

        if show_plots:
            # Plot Spectrum of the original FROG data --> to find the correct range to truncate the data
            fig, axe = plt.subplots()
            p = sns.lineplot(data=FROGspectrum, ax=axe)
            p.set(xlim=(lowWv, highWv))  # change this to zoom in or out on the wavelength axis.
            plt.show(block=False)

        # Plot truncated data
        FROGTrunc = FROGRaw.truncate(before=lowWv, after=highWv, axis="columns")
        FROGTrunc = FROGTrunc.truncate(before=lowT, after=highT, axis="rows")
        FROGspectrumTrunc = FROGTrunc.sum(axis=0)  # truncated spectrum

        if show_plots:
            fig, axe = plt.subplots()
            sns.heatmap(data=FROGTrunc, cmap="viridis", ax=axe)
            plt.show(block=False)

        # truncated FROG intensity, delayFs, wavelengthnm
        FROGIntensity = FROGTrunc.to_numpy()  # intensity data as 2d numpy array float
        FROGdelayFs = FROGTrunc.index.to_numpy()  # delayFs from index to 1d np float
        FROGwaveLengthnm = FROGTrunc.columns.to_numpy()  # wavelength as FROGTrunc.columns 1d np to float
        FROGwaveLengthnm = ShiftFrogby5(FROGwaveLengthnm)

        # saving files for data processing using Frog3.exe from Weinacht's group
        FROGIntensityNmed = FROGIntensity / FROGIntensity.max()  # normalized to 1

        # create a new folder that's identical to the filename to save the post processed frog data and
        dirname = filepath.stem  # basename outputs the file name. ex: 4_1.2A 35cm pm1550.csv. basename[:-4] gives 4_1.2A 35cm pm1550
        if not (dirpath / dirname).exists():
            (dirpath / dirname).mkdir()

        if show_plots:
            fig, axe = plt.subplots()
            sns.heatmap(data=FROGIntensityNmed, ax=axe)
            plt.show(block=True)

        numDelay = len(FROGdelayFs)
        numWvlngth = len(FROGwaveLengthnm)

        DelayIncre = FROGdelayFs[1] - FROGdelayFs[0]
        WvLngthIncre = FROGwaveLengthnm[1] - FROGwaveLengthnm[0]
        WvLngthCenter = (FROGwaveLengthnm[0] + FROGwaveLengthnm[-1]) / 2

        print('Necessary stuff to add before the data(must be in this order), or to be filled in the software')
        print(len(FROGdelayFs), '\t # number of delay points')
        print(len(FROGwaveLengthnm), '\t # number of wavelength points')
        print(FROGdelayFs[1] - FROGdelayFs[0], '\t #delay increment in fs')
        print(FROGwaveLengthnm[1] - FROGwaveLengthnm[0], '\t #wavelength increment in nm')
        print((FROGwaveLengthnm[0] + FROGwaveLengthnm[-1]) / 2, '\t #wavelength of the center pixel')

        np.savetxt(dirpath / dirname / "PostProcessed FROG Trace.csv",FROGIntensityNmed, delimiter='\t')

        # create a header string
        header = str(numDelay) + '\n' + str(numWvlngth) + '\n' + str(DelayIncre) + '\n' + str(
            WvLngthIncre) + '\n' + str(
            WvLngthCenter)

        # save the array to a text file with the header
        np.savetxt(dirpath / dirname / "PostProcessed FROG Trace_with header.csv", FROGIntensityNmed, delimiter='\t',
                   header=header,
                   comments='')

        # save the parameters into a info txt file
        info = 'Necessary stuff to add before the data(must be in this order), or to be filled in the software' + '\n' + str(
            numDelay) + '\t\t\t number of delay points' + '\n' + str(
            numWvlngth) + '\t\t\t number of wavelength points' + '\n' + str(
            DelayIncre) + '\t\t\t delay increment in fs' + '\n' + str(
            WvLngthIncre) + '\t\t\t wavelength increment in nm' + '\n' + str(
            WvLngthCenter) + '\t\t\t wavelength of the center pixel'
        np.savetxt(dirpath / dirname / "PostProcessed FROG parameter.txt", np.array([]), delimiter='\t', header=info,
                   comments='')
