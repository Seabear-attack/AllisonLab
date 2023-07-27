import numpy as np
import matplotlib.pyplot as plt

def read_frog(filename):
    # Replace this function with your actual FROG trace data generation
    input_file = np.genfromtxt(filename, usecols = (0))
    num_bins = int(input_file[0])
    wavelengths = input_file[2:2 + num_bins]
    delays = input_file[2 + num_bins:2 + 2 * num_bins]
    print(len(input_file[2 + 2 * num_bins:]))
    trace = input_file[2 + 2 * num_bins:]
    trace = np.flipud(np.reshape(trace, (num_bins, num_bins)))
    return delays, wavelengths, trace

def read_pulse(filename):
    # Replace this function with your actual FROG trace data generation
    input_file = np.genfromtxt(filename)
    time = input_file[:, 0]
    intensity = input_file[:, 1]

    return time, intensity

def calculate_autocorrelation(frog_trace):
    # Replace this function with your actual autocorrelation calculation
    return np.sum(frog_trace, axis=0)

def main():
    # Sample time delay and wavelength arrays
    time_delay, wavelength, frog_trace = read_frog(r"C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\1565 +- 3 nm BPF\7-9-23  Pulse duration optimization (1565 BPF)\with_modulator\all_pulses_1.2A_all_+51cm_PM1550_short_EDFA_port\a.dat")
    time, intensity = read_pulse(r"C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\1565 +- 3 nm BPF\7-9-23  Pulse duration optimization (1565 BPF)\with_modulator\all_pulses_1.2A_all_+51cm_PM1550_short_EDFA_port\Ek.dat")
    # Calculate the autocorrelation
    autocorrelation = calculate_autocorrelation(frog_trace)

    # # Plot the FROG trace
    f = plt.figure(figsize=(10, 20))
    # ax1 = f.add_subplot(211)
    # ax1.imshow(np.abs(frog_trace), aspect='auto', extent=[time_delay.min(), time_delay.max(), wavelength.min(), wavelength.max()])
    # plt.xlabel('Time Delay [fs]')
    # plt.ylabel('Wavelength [nm]')
    # plt.title('FROG Trace')
    # # plt.colorbar()

    # Plot the autocorrelation
    ax2 = f.add_subplot(211)
    ax2.plot(time_delay, autocorrelation)
    plt.xlabel('Time Delay [fs]')
    plt.ylabel('Intensity')
    plt.title('Autocorrelation')

    # Plot the pulse
    ax3 = f.add_subplot(212, sharex = ax2)
    ax3.plot(time, intensity)
    plt.xlabel('Time Delay [fs]')
    plt.ylabel('Intensity')
    plt.title('Reconstructed Pulse')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
