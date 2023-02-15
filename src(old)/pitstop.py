import pandas as pd


def get_pitstops(session: pd.DataFrame, driver: str):
    # Find pit time
    laps = session.laps
    laps_pitstop = laps.loc[
        (~laps["PitOutTime"].isna()) |
        (~laps["PitInTime"].isna())
    ].loc[:, ["Driver", "Compound", "LapNumber", "PitInTime", "PitOutTime"]]
    laps_pitstop["PitInTime_shifted"] = laps_pitstop.groupby("Driver")["PitInTime"].shift(1)
    laps_pitstop["PitStopTime"] = (
        laps_pitstop["PitOutTime"] - laps_pitstop["PitInTime_shifted"]
    ).dt.total_seconds()
    laps_pitstop.loc[laps_pitstop["LapNumber"] == 1, "PitStopTime"] = 0
    laps_pitstop = laps_pitstop.loc[
        laps_pitstop["PitStopTime"].notna(), ["Driver", "Compound", "LapNumber", "PitStopTime"]
    ].reset_index(drop=True)
    laps_pitstop.query(f"Driver == '{driver}'")
    return laps_pitstop
