# Plots every scope lineout in user-selected folder. Works for Tektronix scopes
import matplotlib.pyplot as plt
from pathlib import Path
from plottingutils import openDirectory, directory_to_dataframes, get_scope_data, normalize_by_maximum, offset


if __name__ == "__main__":
    dirpath = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Polarization '
                                  r'Control\9-5-23 RF Ringing\EO Optimization')
    dfs = directory_to_dataframes(dirpath)
    # labels = ['1111111111111111111',
    #           '1111111111111111110',
    #           '1111111111000000000',
    #           '1010101010101010101',
    #           '1110111001110001110',
    #           '1000000000000000000',
    #           '1000000000100000000',
    #           '1111000000111100000']

    labels = ['Output 2, 0 pass',
              'Output 2, 1 pass',
              'Output 1, 0 pass',
              'Output 1, 1 pass']
    data = get_scope_data(dfs, labels)
    normalize_by_maximum(data, 'voltage_V')
    offset(data, 'voltage_V', 1.1)

    # Create a figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(20, 8))

    for label, df in data.items():
        ax.plot(df['time_s'], df['voltage_V'], label=label)
    # Add axis labels and a legend

    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Voltage [V]')
    ax.legend()
    # ax.set_title('Photodiode output')
    ax.set_title('Normalized and Optimized EO Modulator Outputs')
    # Display the plot
    plt.savefig(dirpath / 'optimized_eo_outputs', dpi=500)
    plt.show()
