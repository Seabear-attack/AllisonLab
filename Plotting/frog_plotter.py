import matplotlib.pyplot as plt
import frogdata
from pathlib import Path
import re

if __name__ == "__main__":
    # Sample time delay and wavelength arrays
    frog_path = Path(r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and Spectrum '
                     r'Generation\9-12-23 Pulse Optimization\Correct Axis\Polarized')
    pattern = r'.*cm'
    frogs = frogdata.read_frog_directory(frog_path, pattern=pattern)

    for frog in frogs:
        # # Plot the FROG trace
        f = plt.figure(figsize=(10, 20))
        ax1 = f.add_subplot(311)
        # ax1.imshow(frog.trace, aspect='auto', extent=[min(frog.delays), max(frog.delays), min(frog.wavelengths),
        #                                               max(frog.wavelengths)])
        ax1.imshow(frog.trace, aspect='auto', extent=[min(frog.delays), max(frog.delays), min(frog.wavelengths),
                                                      max(frog.wavelengths)])
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Wavelength [nm]')
        plt.title(f'{frog.label} FROG Trace, FROG error: {frog.frog_error: 1.3f}')

        # Plot the autocorrelation
        ax2 = f.add_subplot(312, sharex=ax1)
        ax2.plot(frog.delays, frog.autocorrelation())
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Intensity')
        plt.title('Autocorrelation')

        # Plot the pulse
        ax3 = f.add_subplot(313, sharex=ax2)
        ax3.plot(frog.pulse_time, frog.pulse_intensity, label=f'FWHM: {frog.t_FWHM: 1.1f} fs')
        ax3.set_xlim([-1000, 1000])
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Intensity')
        plt.title('Reconstructed Pulse')
        plt.legend()
        f.canvas.manager.window.showMaximized() #toggle fullscreen mode
        plt.tight_layout()
        plt.show(block=False)
    plt.show()