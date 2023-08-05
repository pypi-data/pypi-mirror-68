from sklearn import linear_model
import pandas as pd
import pyslackline.plot as p
import numpy as np
import scipy
import json
import os


class SlackCell:
    def __init__(self, path):
        self.path = path
        self.df = self.read()
        self.start = 0
        self.end = self.df.time.iat[-1]
        self.df_spectrum = pd.DataFrame()
        self.bounce_duration = -1
        self.interval = -1
        self.detensioning_rate = 0
        self.analysed = False

    def read(self):
        """
        Read data of the SlackCell and convert it. Compute time diff
        :return: Data
        :rtype: pd.DataFrame
        """
        df = pd.read_csv(self.path, sep=';')
        # drop invalid columns
        df = df.dropna(axis=1)
        # conversion to seconds
        df.time = df.time / 1000
        # conversion to kN
        df.force = df.force / 1000
        # set start time to zero
        df.time = df.time - df.time.iat[0]
        df = df.reset_index()
        # get scan intervals
        df['interval'] = df.time.diff()
        return df

    def set_start(self, start):
        """
        Set start time in seconds.
        :param start: start time in seconds
        :type start: float
        :return:
        """
        self.start = start
        # filter df
        self.df = self.df[self.df.time > self.start]
        # reset time to zero
        self.df.time = self.df.time - self.df.time.iat[0]
        self.df = self.df.reset_index()

    def set_end(self, end):
        """
        Set end time in seconds.
        :param end: end time in seconds
        :type end: float
        :return:
        """
        self.end = end
        self.df = self.df[self.df.time < self.end]

    def analysis(self):
        """
        Perform complete analysis, including spectrum analysis, linear regression and gradient
        :return:
        """
        if not self.analysed:
            self.spectrum()
            self.linear_regression()
            self.gradient()
            self.analysed = True

    def print(self):
        """
        Print the data analysis
        :return:
        """
        self.analysis()
        print(f"Mean tension: {self.df.force.mean():.2f} [kN]")
        print(f"Min tension: {self.df.force.min():.2f} [kN]")
        print(f"Max tension: {self.df.force.max():.2f} [kN]")

        print(f"Detensioning rate: {self.detensioning_rate * 1000:.2f} [N/s]")
        print(f"Detensioning rate: {self.detensioning_rate * 60:.2f} [kN/min]")

        print(f"Write intervall: {self.interval:.3f} [s]")
        print(f"Write frequency: {1/self.interval:.2f} [Hz]")
        print(f"Nyquist Frequency: {1/self.interval / 2:.2f} [Hz], {self.interval * 2:.2f} [s] ")

        print(f"Bounce duration: {self.bounce_duration:.2f} [s]")

        print(f"Max gradient: {self.df.gradient.abs().max():.2f} [kN/s]")

    def linear_regression(self):
        """
        Perform linear regression on the force data to approximate the detensioning rate
        :return: linear regression of force, detensioning rate
        :rtype: pd.Series, float
        """
        # Create linear regression object
        regr = linear_model.LinearRegression()
        x = self.df.time
        y = self.df.force
        x = x.values.reshape(-1, 1).astype(float)
        y = y.values.reshape(-1, 1)
        regr.fit(x, y)
        self.df['force_lin'] = regr.predict(x)
        self.detensioning_rate = -regr.coef_[0][0]
        # Train the model using the training sets
        return self.df.force_lin, self.detensioning_rate

    def plots(self):
        """
        Create all plots
        :return:
        """
        self.analysis()
        p.timeseries(self.df)
        p.scan_intervall(self.df)
        p.spectrum(self.df_spectrum, self.bounce_duration)
        p.period(self.df_spectrum, self.bounce_duration)

    def detensioning_rate(self):
        """
        Detensioning rate approximated by linear regression
        :return: Detensioning rate
        :rtype: float
        """
        if self.detensioning_rate == 0:
            self.linear_regression()
        return self.detensioning_rate

    def spectrum(self, exclude=1):
        """
        Perform a FFT on force
        :param exclude: excluding first n values of spectrum
        :type exclude: int
        :return: frequency, magnitude
        :rtype: pd.Series, pd.Series
        """
        self.interval = self.df.interval.median()
        frequency = 1 / self.interval
        y_fft = np.fft.fft(self.df.force.values)
        n = int(len(y_fft) / 2 + 1)
        frequency = np.linspace(0, frequency / 2, n, endpoint=True)
        magnitude = 2.0 * np.abs(y_fft[:n]) / n
        start = exclude
        end = n
        magnitude_filtered = scipy.ndimage.gaussian_filter1d(
            magnitude[start:end], sigma=5)
        # Xp = 1.0/X
        iatmax = np.argmax(magnitude_filtered)
        self.bounce_duration = 1 / frequency[start:end][iatmax]
        self.df_spectrum['frequency'] = frequency[start:end]
        self.df_spectrum['period'] = 1/frequency[start:end]
        self.df_spectrum['magnitude'] = magnitude[start:end]
        self.df_spectrum['magnitude_filtered'] = magnitude_filtered
        return self.df_spectrum['frequency'], self.df_spectrum['magnitude']

    def gradient(self):
        """
        Calculate the gradient of the force
        :return: gradient of force
        :rtype: pd.Series
        """
        self.df['gradient'] = np.gradient(self.df.force, self.df.time)
        return self.df.gradient

    def json(self, path='data'):
        """
        Export all data as json to path
        :param path: saving directory
        :type path: str
        :return:
        """
        self.analysis()
        spectrum = {'frequency': self.df_spectrum.frequency.tolist(),
                    'magnitude': self.df_spectrum.magnitude.tolist(),
                    'x_max': 1/self.bounce_duration,
                    'y_max': self.df_spectrum.magnitude.max()
                    }
        interval = {'time': self.df.time[:-1].tolist(),
                    'interval': self.df.interval.tolist()}

        timeseries = {'time': self.df.time.tolist(),
                      'force': self.df.force.tolist(),
                      'force_lin': self.df.force_lin.tolist(),
                      'gradient': self.df.gradient.tolist()}
        os.makedirs(path, exist_ok=True)
        for data, filename in [(spectrum, 'spectrum'), (interval, 'interval'), (timeseries, 'timeseries')]:
            with open(os.path.join(path, filename + ".json"), 'w') as file:
                file.write(json.dumps(data))

    def simple_static_sag_model(self, weight, length):
        """
        Simple sag model for static load on a slackline
        :param weight: weight of the slackliner in kg
        :type weight: float [kg]
        :param length: length of the slackline in m
        :type length: float [m]
        :return: sag for static load on a slackline
        :rtype: float [m]
        """
        weight = weight * 9.81
        # s = F_g*l / 4F_sl
        sag = weight*length / (4*self.df.force*1000)
        # TODO get this right
        # sag2 = (-(length**2)/(4-((self.df.force*1000)/weight)**2))**.5
        self.df['sag'] = sag
        return sag
