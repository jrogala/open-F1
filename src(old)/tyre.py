import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import enum


# Applying tyre penalty to lap time.
def PX(x, a, b, c, d, x0, x1, x2):
    return (
        a -
        abs(b)*np.maximum(x0, x) +
        abs(c)*np.maximum(x1, x) +
        abs(np.maximum(d, 1)) * np.maximum(x2, x)
    )


def P1(x, a, b):
    return a - abs(b)*x


p0_X = [80, 1, 1, 1, 5, 10, 50]  # this is an mandatory initial guess
p0_1 = [80, 1]  # this is an mandatory initial guess


class Tyre(enum.Enum):
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    SOFT = "SOFT"
    INTERMEDIATE = "INTERMEDIATE"
    WET = "WET"


tyreColor = {
    Tyre.MEDIUM: "yellow",
    Tyre.HARD: "black",
    Tyre.SOFT: "red",
    Tyre.INTERMEDIATE: "green",
    Tyre.WET: "blue"
}


def estimate_wear(session: pd.DataFrame):
    laps = session.laps
    tyreWear = {}
    amount_laps = int(laps["LapNumber"].max())
    for tyreCompound in tyreColor:
        comp = laps.query(f"Compound == '{tyreCompound}'").reset_index()
        if len(comp):
            comp_min = comp.groupby("TyreLife")["LapTime_s"].min()
            filtered_time = comp_min[comp_min < comp_min.quantile(0.8)]
            try:
                opt_lapTime, _ = curve_fit(
                    PX,
                    filtered_time.dropna().index,
                    filtered_time.dropna(),
                    p0_X,
                    maxfev=80000
                )
                tyreWear[tyreCompound] = PX(np.arange(amount_laps), *opt_lapTime)
            except TypeError:
                print(f"Error for compound {tyreCompound}")
                opt_lapTime, _ = curve_fit(
                    P1,
                    filtered_time.dropna().index,
                    filtered_time.dropna(),
                    p0_1,
                    maxfef=80000
                )
                tyreWear[tyreCompound] = P1(np.arange(amount_laps), *opt_lapTime)
