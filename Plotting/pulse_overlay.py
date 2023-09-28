import matplotlib.pyplot as plt
from Plotting.utils import frogdata
from pathlib import Path
import re

if __name__ == "__main__":
    # Sample time delay and wavelength arrays
    frog_path = Path(
        r'C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\Pulse Optimization and Spectrum Generation\9-18-23 Tunable seed pulse pattern\43cm_4A')
    pattern = r'\d{19}'
    cmap = 'rainbow'
    save_files = False
    frogs = frogdata.read_frog_directory(frog_path, pattern=pattern)
    frogs = sorted(frogs, key=lambda frog: len(re.findall(r'1', frog.label)))
    f, ax = plt.subplots(figsize=(12, 8))
    for i, frog in enumerate(frogs):
        # Fix the phase signs to all be the same (pulse maximum on the left of the plot)
        if frog.pulse_time[frog.pulse_intensity == max(frog.pulse_intensity)] > frog.pulse_time[
                                                                    int(len(frog.pulse_time) / 2)]:
            frog.pulse_intensity = frog.pulse_intensity[::-1]

        # Have all the maxima overlap one another in time
        frog.pulse_time = frog.pulse_time - (frog.pulse_time[frog.pulse_intensity == max(frog.pulse_intensity)] -
                                             frogs[0].pulse_time[frogs[0].pulse_intensity == max(frogs[0].pulse_intensity)])

        # Plot the pulse
        ax.plot(frog.pulse_time, frog.pulse_intensity, label=f'{frog.label}')
        plt.xlabel('Time Delay [fs]')
        plt.ylabel('Intensity')
        plt.title('Reconstructed Pulse')
        plt.legend()
        f.canvas.manager.window.showMaximized()  # toggle fullscreen mode
        plt.tight_layout()
        if save_files:
            plt.savefig(frog_path / frog.label, dpi=500)
        plt.show(block=False)
    plt.show()
