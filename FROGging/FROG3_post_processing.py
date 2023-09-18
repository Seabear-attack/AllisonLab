# Given a directory, loops through the .csv files corresponding to FROG Traces.
# Creates a new folder containing files compatible with Frog3.exe retrieval software

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# dirpath = eg.diropenbox(default=r"C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump")
dirpath = r"C:\Users\JT\Documents\FROGs\9-15-23 Tunable seed pulse optimization"
filenames = [filename for filename in os.listdir(dirpath) if filename[-4:] == ".csv"]
show_plots = False

for filename in filenames:
    filepath = os.path.join(dirpath, filename)
    # import data from csv
    FROGRaw = pd.read_csv(filepath, index_col=0,
                          dtype=np.float64)  # read as csv with index being the first column(delay)

    FROGRaw.columns = FROGRaw.columns.astype(float)  # the wavelength used to be in string, change it to float!
    FROGspectrum = FROGRaw.sum(axis=0)  # sum over the horizontal axis to get the whole spectrum

    # Plot original FROG Trace
    print('data opened from:\t' + filepath)

    if show_plots:
        fig, axe = plt.subplots()
        sns.heatmap(data=FROGRaw, ax=axe)
        plt.show(block=False)


    # shifts the FROG spectrum by -4.893nm because the OSA is not measuring spectrum correctly - tested by the HeNe
    def ShiftFrogby5(OriginalFrog):
        ShiftedFROG = OriginalFrog - 4.893
        return ShiftedFROG


    # zoom in on wavelength
    lowWv = 750
    highWv = 810

    # zoom in on time
    lowT = -1000
    highT = 1000


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
    dirname = filepath[
              :-4]  # basename outputs the file name. ex: 4_1.2A 35cm pm1550.csv. basename[:-4] gives 4_1.2A 35cm pm1550
    if not os.path.exists(dirname):
        os.makedirs(dirname)

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

    np.savetxt(os.path.join(dirname, "PostProcessed FROG Trace.csv"), FROGIntensityNmed, delimiter='\t')

    # create a header string
    header = str(numDelay) + '\n' + str(numWvlngth) + '\n' + str(DelayIncre) + '\n' + str(WvLngthIncre) + '\n' + str(
        WvLngthCenter)

    # save the array to a text file with the header
    np.savetxt(os.path.join(dirname, "PostProcessed FROG Trace_with header.csv"), FROGIntensityNmed, delimiter='\t',
               header=header,
               comments='')

    # save the parameters into a info txt file
    info = 'Necessary stuff to add before the data(must be in this order), or to be filled in the software' + '\n' + str(
        numDelay) + '\t\t\t number of delay points' + '\n' + str(
        numWvlngth) + '\t\t\t number of wavelength points' + '\n' + str(
        DelayIncre) + '\t\t\t delay increment in fs' + '\n' + str(
        WvLngthIncre) + '\t\t\t wavelength increment in nm' + '\n' + str(
        WvLngthCenter) + '\t\t\t wavelength of the center pixel'
    np.savetxt(os.path.join(dirname, "PostProcessed FROG parameter.txt"), np.array([]), delimiter='\t', header=info,
               comments='')
