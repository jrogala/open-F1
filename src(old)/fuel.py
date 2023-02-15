import pandas as pd
import numpy as np
import seaborn as sns
import fastf1
from scipy.optimize import curve_fit

fastf1.Cache.enable_cache('./f1cache')


# Applying fuel penalty to lap time.

def P1(x, a, b):
    return a - abs(b)*x


p0 = [80, 1]  # this is an mandatory initial guess


def estimate_time_lost(session: pd.DataFrame):
    """
    Return the estimated time lost from a dataframe Laps from FastF1
    :param dataframe containing at least ["LapNumber", "Compound", "LapTime"] as columns
    :returns Series containing each lap delta caused by fuel
    """
    laps = session.laps
    amount_laps = int(laps["LapNumber"].max())  # Get amount of laps for later use
    comp_min = (
        laps
        .groupby(["LapNumber", "Compound"])["LapTime"]
        .min().reset_index()
        .groupby("LapNumber").mean()
        .cummin()
    )  # Get the cumulative minimum for each tyre compound and average them.
    # TODO: Make a better approximation using mean and quantile
    opt_lapTime, _ = curve_fit(
        P1,
        comp_min.dropna().index,
        comp_min.dropna()["LapTime"].dt.total_seconds(),
        p0
    )
    fuel_time = pd.Series(
        index=[lap+1 for lap in range(amount_laps)],
        data=P1(np.arange(amount_laps), *opt_lapTime),
        name="LapTime"
    )  # Minimal time for each driver approximated by fuel
    fuel_time_pen = fuel_time - fuel_time.min()  # Fuel penalty time induced
    return fuel_time_pen

    # plotter("Cumulative minimum of time", "Lap", "time (s)")
    # plt.scatter(comp_min.index, comp_min, label="CumMin of time")
    # plt.plot(fuel_time, label="Appoximated time cost by fuel")
    # plt.legend()
    # plt.show()
