import matplotlib.pyplot as plt
import frogdata
from pathlib import Path
import re

if __name__ == "__main__":
    # Sample time delay and wavelength arrays
    frog_path = Path(r'C:\Users\JT\Documents\FROGs\9-15-23 Tunable seed pulse optimization')
    pattern = r'.*cm_4A'
    frogs = frogdata.read_frog_directory(frog_path, pattern=pattern)

    for i, frog in enumerate(frogs):
        # # Plot the FROG trace
        if i % 3 == 0:
            f = plt.figure(figsize=(10, 20))
        ax1 = f.add_subplot(3, 3, (3 * i) % 9 + 1)
        ax1.imshow(frog.trace, aspect='auto', extent=[min(frog.delays), max(frog.delays), min(frog.wavelengths),
                                                      max(frog.wavelengths)])
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Wavelength [nm]')
        plt.title(f'{frog.label} Measured FROG Trace, FROG error: {frog.frog_error: 1.3f}')

        # Plot the autocorrelation
        # ax2 = f.add_subplot(3, 3, (3 * i + 1) % 9 + 1, sharex=ax1)
        # ax2.plot(frog.delays, frog.autocorrelation())
        # plt.xlabel('Time Delay [fs]')
        # plt.ylabel('Intensity')
        # plt.title('Autocorrelation')

        # Plot the reconstructed trace

        ax2 = f.add_subplot(3, 3, (3 * i + 1) % 9 + 1, sharex=ax1)
        ax2.imshow(frog.trace_recon, aspect='auto', extent=[min(frog.delays), max(frog.delays), min(frog.wavelengths),
                                                      max(frog.wavelengths)])
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Wavelength [nm]')
        plt.title(f'{frog.label} Reconstructed FROG Trace')

        # Plot the pulse
        ax3 = f.add_subplot(3, 3, (3 * i + 2) % 9 + 1, sharex=ax2)
        ax3.plot(frog.pulse_time, frog.pulse_intensity, label=f'FWHM: {frog.t_FWHM: 1.1f} fs')
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Intensity')
        plt.title('Reconstructed Pulse')
        plt.legend()
        f.canvas.manager.window.showMaximized() #toggle fullscreen mode
        plt.tight_layout()
        plt.show(block=False)
    plt.show()