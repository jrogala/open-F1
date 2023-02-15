import pandas as pd


def clean_laps(session: pd.DataFrame):
    """
    Working on laps to remove any pitstop/safety car/begin
    """
    laps = session.laps
    laps_clean = laps.loc[
            laps["PitOutTime"].isna() &
            laps["PitInTime"].isna() &
            (laps["TrackStatus"].astype(int) == 1)
    ].reset_index(drop=True)
    return laps_clean


def average(session: pd.DataFrame):
    """
    Get time relative to the average lap time
    """
    laps = session.laps
    amount_laps_per_driver = laps.groupby("Driver")["LapNumber"].max()
    total_time_per_driver = session.set_index("Driver").results["Time"].dt.total_seconds()
    
    for driver in laps["Driver"].unique():
        laps.loc[laps["Driver"] == driver, "LapTime_average"] = session.results["Time"].dt.total_seconds()
