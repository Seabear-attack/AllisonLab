# Runs with python ver. 2.7

import numpy as np
import matplotlib.pyplot as plt
import pynlo

def dB(num):
    return 10 * np.log10(np.abs(num) ** 2)

# Fundamental constants
c_nm_per_ps = 300000

# Pulse characteristics
pulse_at_file_in = np.genfromtxt(r"C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\1565 +- 3 nm BPF\7-9-23  Pulse duration optimization (1565 BPF)\with_modulator\all_pulses_1.2A_all_+51cm_PM1550_short_EDFA_port\Ek.dat")
pulse_al_file_in = np.genfromtxt(r"C:\Users\wahlm\Documents\School\Research\Allison\Tunable Pump\1565 +- 3 nm BPF\7-9-23  Pulse duration optimization (1565 BPF)\with_modulator\all_pulses_1.2A_all_+51cm_PM1550_short_EDFA_port\Speck.dat")
pulse_time_ps = .001 * pulse_at_file_in[:, 0]
pulse_amp = pulse_at_file_in[:, 3] + 1j * pulse_at_file_in[:, 4]
pulse_wavelength_nm = pulse_al_file_in[:, 0]
pulse_freq_THz = np.linspace(max(pulse_wavelength_nm)/c_nm_per_ps, min(pulse_wavelength_nm)/c_nm_per_ps,
                             len(pulse_wavelength_nm))
pulseWL = 1565  # pulse central wavelength (nm)
rep_rate = 61   # MHz
EPP = (4e-9)/1  # Energy per pulse (J) + fudge factor
GDD = 0.0  # Group delay dispersion (ps^2)
TOD = 0.0  # Third order dispersion (ps^3)

# Simulation constants
Window = 2.0  # simulation window (ps)
Steps = 100  # simulation steps
# Points = 2 ** 13  # simulation points
pad_factor = 2
Raman = True  # Enable Raman effect?
Steep = True  # Enable self steepening?

# Plot options
wavelength_axis = True  # True: wavelength axis, False: frequency axis

font = {'size': 14}
plt.rc('font', **font)

# Fiber 1 (OFS PM ND-HNLF)
Length = 50  # length in mm
Alpha = 0.8 * 10 ** (-5)  # attenuation coefficient (dB/cm)
Gamma = 10.5  # Gamma (1/(W km))
fibWL = 1550  # Center WL of fiber (nm)
D = -2.6  # (ps/(nm*km))
D_slope = .026  # (ps/(nm^2*km))
if D == 0:
    beta2 = -7.5  # (ps^2/km)
    beta3 = 0.00  # (ps^3/km)
else:
    beta2 = -D * fibWL ** 2 / (2 * np.pi * c_nm_per_ps)
    beta3 = fibWL ** 3 / (2 * np.pi ** 2 * c_nm_per_ps ** 2) * (fibWL / 2 * D_slope + D)
beta4 = 0.00  # (ps^4/km)
alpha = np.log((10 ** (Alpha * 0.1))) * 100  # convert from dB/cm to 1/m
fiber1 = pynlo.media.fibers.fiber.FiberInstance()  # create the fiber!
fiber1.generate_fiber(Length * 1e-3, center_wl_nm=fibWL, betas=(beta2, beta3, beta4),
                      gamma_W_m=Gamma * 1e-3, gvd_units='ps^n/km', gain=-alpha)

# Fiber 2 (PM1550)
# Length = 1000  # length in mm
# Alpha = 1 * 10 ** (-5)  # attenuation coefficient (dB/cm)
# Gamma = 1  # Gamma (1/(W km)) *****guess******
# fibWL = 1550  # Center WL of fiber (nm)
# D = 18  # (ps/(nm*km))
# D_slope = .06  # (ps/(nm^2*km))
# if D == 0:
#     beta2 = -7.5  # (ps^2/km)
#     beta3 = 0.00  # (ps^3/km)
# else:
#     beta2 = -D * fibWL ** 2 / (2 * np.pi * c_nm_per_ps)
#     beta3 = fibWL ** 3 / (2 * np.pi ** 2 * c_nm_per_ps ** 2) * (fibWL / 2 * D_slope + D)
# beta4 = 0.00  # (ps^4/km)
# alpha = np.log((10 ** (Alpha * 0.1))) * 100  # convert from dB/cm to 1/m
# fiber2 = pynlo.media.fibers.fiber.FiberInstance()  # create the fiber!
# fiber2.generate_fiber(Length * 1e-3, center_wl_nm=fibWL, betas=(beta2, beta3, beta4),
#                       gamma_W_m=Gamma * 1e-3, gvd_units='ps^n/km', gain=-alpha)



######## This is where the PyNLO magic happens! ############################

# create the pulse!
# pulse = pynlo.light.DerivedPulses.SechPulse(1, FWHM/1.76, pulseWL, time_window_ps=Window,
#                   GDD=GDD, TOD=TOD, NPTS=Points, frep_MHz=100, power_is_avg=False)
# pulse = pynlo.light.DerivedPulses.GaussianPulse(1, FWHM / 1.76, pulseWL, time_window_ps=Window,
#                                             GDD=GDD, TOD=TOD, NPTS=Points, frep_MHz=61, power_is_avg=False)

pulse = pynlo.light.PulseBase.Pulse()
pulse.set_NPTS(len(pulse_time_ps))
pulse.set_center_wavelength_nm(1565)
pulse.set_time_window_ps(max(pulse_time_ps) - min(pulse_time_ps))
pulse.set_AT(pulse_amp)
# pulse.set_frequency_window_THz(max(pulse_freq_THz) - min(pulse_freq_THz))
pulse.set_frep_MHz(rep_rate)
pulse.set_epp(EPP)  # set the pulse energy
pulse.expand_time_window(pad_factor, "even")
dict = pulse.get_pulse_dict()
# Propagation
evol = pynlo.interactions.FourWaveMixing.SSFM.SSFM(local_error=0.001, USE_SIMPLE_RAMAN=True,
                                                   disable_Raman=np.logical_not(Raman),
                                                   disable_self_steepening=np.logical_not(Steep))

y, AW, AT, pulse_out = evol.propagate(pulse_in=pulse, fiber=fiber1, n_steps=Steps)

########## That's it! Physic done. Just boring plots from here! ################


F = pulse.W_mks / (2 * np.pi) * 1e-12  # convert to THz




F_plus = F[F > 0]
Lambda = c_nm_per_ps / F_plus
zW = np.power(np.abs(np.transpose(AW)[:, (F > 0)]), 2)
zT = np.power(np.abs(np.transpose(AT)), 2)
zL = zW * np.power(F_plus, 2) / c_nm_per_ps

zW_dB = dB(zW)
zT_dB = dB(zT)
zL_dB = dB(zL)

y = y * 1e3  # convert distance to mm

# set up plots for the results:
fig = plt.figure(figsize=(10, 10))
ax0 = plt.subplot2grid((4, 1), (0, 0))
# ax1 = plt.subplot2grid((4, 1), (0, 1))
ax2 = plt.subplot2grid((4, 1), (1, 0), sharex=ax0)
# ax3 = plt.subplot2grid((4, 1), (1, 1), sharex=ax1)
ax4 = plt.subplot2grid((4, 1), (2, 0), rowspan=2, sharex=ax0)
# ax5 = plt.subplot2grid((4, 1), (2, 1), rowspan=2, sharex=ax1)


if wavelength_axis:
    ax0.plot(Lambda, zL[-1], color='r')
    # ax1.plot(pulse.T_ps, zT[-1], color='r')

    ax0.plot(Lambda, zL[0], color='b')
    # ax1.plot(pulse.T_ps, zT[0], color='b')

    ax2.plot(Lambda, zL_dB[-1], color='r')
    # ax3.plot(pulse.T_ps, zT_dB[-1], color='r')

    ax2.plot(Lambda, zL_dB[0], color='b')
    # ax3.plot(pulse.T_ps, zT_dB[0], color='b')
    extent = (1200, 1900, 0, Length)
    ax4.imshow(zL_dB, extent=extent, vmin=np.max(zL_dB) - 60.0,
               vmax=np.max(zL_dB), aspect='auto', origin='lower')

    extent = (np.min(pulse.T_ps), np.max(pulse.T_ps), np.min(y), Length)
    # ax5.imshow(zT_dB, extent=extent, vmin=np.max(zT_dB) - 60.0,
    #            vmax=np.max(zT_dB), aspect='auto', origin='lower')

    ax0.set_ylabel('Intensity (dB)')
    ax2.set_ylabel('Intensity (arb.)')

    ax4.set_xlabel('Wavelength (nm)')

    # ax5.set_xlabel('Time (ps)')

    ax4.set_ylabel('Propagation distance (mm)')

    ax0.set_xlim(1200, 1900)
    # ax1.set_xlim(-1, 1)
    ax2.set_ylim(-60, 20)
    # ax3.set_ylim(30, 100)
else:
    ax0.plot(F_plus, zW[-1], color='r')
    ax1.plot(pulse.T_ps, zT[-1], color='r')

    ax0.plot(F_plus, zW[0], color='b')
    ax1.plot(pulse.T_ps, zT[0], color='b')

    ax2.plot(F_plus, zW_dB[-1], color='r')
    ax3.plot(pulse.T_ps, zT_dB[-1], color='r')

    ax2.plot(F_plus, zW_dB[0], color='b')
    ax3.plot(pulse.T_ps, zT_dB[0], color='b')

    extent = (np.min(F_plus), np.max(F_plus), 0, Length)
    ax4.imshow(zW_dB, extent=extent, vmin=np.max(zW_dB) - 60.0,
               vmax=np.max(zW_dB), aspect='auto', origin='lower')

    extent = (np.min(pulse.T_ps), np.max(pulse.T_ps), np.min(y), Length)
    ax5.imshow(zT_dB, extent=extent, vmin=np.max(zT_dB) - 60.0,
               vmax=np.max(zT_dB), aspect='auto', origin='lower')

    ax0.set_ylabel('Intensity (arb.)')
    ax2.set_ylabel('Intensity (dB)')

    ax4.set_xlabel('Frequency (THz)')

    ax5.set_xlabel('Time (ps)')

    ax4.set_ylabel('Propagation distance (mm)')

    ax4.set_xlim(0, 400)

    ax2.set_ylim(-50, 20)
    ax1.set_ylim(-40, 60)
    ax0.set_xlim(1200, 1900)
    ax1.set_xlim(-1, 1)

plt.show()
plt.tight_layout(pad=.2)
