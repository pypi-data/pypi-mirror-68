import matplotlib.pyplot as plt
import os

path = "plots"

os.makedirs(path, exist_ok=True)


def timeseries(df):
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 7.15)
    ax.plot(df.time, df.force)
    if 'force_lin' in df.keys():
        ax.plot(df.time, df.force_lin)
    ax.set(title="Longline Bouncing", xlabel="time [s]", ylabel="force [kN]")
    plt.show()
    fig.savefig(os.path.join(path, "longline_bouncing.png"))
    return fig, ax


def scan_intervall(df):
    fig, ax = plt.subplots()
    ax.plot(df.time[1:], df.interval[1:]*1000)
    ax.set(title="Scan Interval", xlabel="time [s]", ylabel="interval [ms]")
    plt.show()
    fig.savefig(os.path.join(path, "scan_interval.png"))
    return fig, ax


def spectrum(df, bounce_duration):
    fig, ax = plt.subplots()
    ax.plot(df.frequency, df.magnitude_filtered)
    ax.annotate(f"{bounce_duration:.2f}s bounce duration",
                (1/bounce_duration + .02, df.magnitude_filtered.max()), fontsize=12)
    ax.set(title="Magnitude Spectrum", xlabel="frequency [Hz]", ylabel="magnitude [kN]")
    plt.show()
    fig.savefig(os.path.join(path, "frequency_analysis.png"))
    return fig, ax


def period(df, bounce_duration):
    df = df[df.period < 3*bounce_duration]
    fig, ax = plt.subplots()
    ax.plot(df.period, df.magnitude_filtered)
    ax.annotate(f"{bounce_duration:.2f}s bounce duration",
                (bounce_duration + .02, df.magnitude_filtered.max()), fontsize=12)
    ax.set(title="Magnitude Spectrum", xlabel="Period [s]", ylabel="magnitude [kN]")
    plt.show()
    fig.savefig(os.path.join(path, "period_analysis.png"))
    return fig, ax


def gradient(df):
    fig, ax = plt.subplots()
    ax.plot(df.time, df.gradient)
    ax.set(title="Gradient", xlabel="time [s]", ylabel="force gradient [kN/s]")
    plt.show()
    fig.savefig(os.path.join(path, "gradient.png"))
    return fig, ax


def sag(df):
    fig, ax = plt.subplots()
    ax.plot(df.time, df.sag)
    ax.set(title="Sag", xlabel="Time [s]", ylabel="Sag [m]")
    plt.show()
    fig.savefig(os.path.join(path, "sag.png"))
    return fig, ax
