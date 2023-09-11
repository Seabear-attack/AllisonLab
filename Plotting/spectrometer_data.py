import numpy as np
from os import listdir
from os.path import join


class SpectrumData:
    def __init__(self, data, axis_units, data_label, spectrum_power_mW, frep_MHz=60.5):
        self._x_axis_units = axis_units[0]
        self._y_axis_units = axis_units[1]
        self.x_axis_data = data[:, 0]
        self.y_axis_data = data[:, 1]
        self.total_power = spectrum_power_mW
        self.label = data_label
        self._frep_MHz = frep_MHz
        self._pulse_energy_nJ = self.total_power / self._frep_MHz

        self.y_axis_units = axis_units[1]

    @property
    def x_axis_units(self):
        return self._x_axis_units

    @x_axis_units.setter
    def x_axis_units(self, units):
        if units == 'nm':
            self._x_axis_units = units

    @property
    def y_axis_units(self):
        return self._y_axis_units

    @y_axis_units.setter
    def y_axis_units(self, units):
        if self._y_axis_units[:2] == 'dB':
            self.y_axis_data = np.power(10, self.y_axis_data / 10)
        self._y_axis_units = units
        self.__normalize()

    def __normalize(self):
        integral = sum(self.y_axis_data)
        delta_lambda = self.x_axis_data[1] - self.x_axis_data[0]

        if self._y_axis_units == 'mW':
            self.y_axis_data = self.y_axis_data * self.total_power / integral

        elif self._y_axis_units == 'mW/nm':
            self.y_axis_data = self.y_axis_data * self.total_power / integral / delta_lambda

        elif self._y_axis_units == 'dBm':
            self.y_axis_data = 10 * np.log10(self.y_axis_data * self.total_power / integral)

        elif self._y_axis_units == 'dBm/nm':
            self.y_axis_data = 10 * np.log10(self.y_axis_data * self.total_power / integral / delta_lambda)

        elif self._y_axis_units == 'nJ':
            self.y_axis_data = self.y_axis_data * self._pulse_energy_nJ / integral

        elif self._y_axis_units == 'dBnJ':
            self.y_axis_data = 10 * np.log10(self.y_axis_data * self._pulse_energy_nJ / integral)

        elif self._y_axis_units == 'nJ/nm':
            self.y_axis_data = self.y_axis_data * self._pulse_energy_nJ / integral / delta_lambda

        elif self._y_axis_units == 'dBnJ/nm':
            self.y_axis_data = 10 * np.log10(self.y_axis_data * self._pulse_energy_nJ / integral / delta_lambda)


def readFromFiles(path):
    data_list = []
    filenames = listdir(path)
    for filename in filenames:
        data_list.append(np.genfromtxt(join(path, filename), invalid_raise=False, skip_header=40,
                                       delimiter=',', comments='"'))
    return data_list
