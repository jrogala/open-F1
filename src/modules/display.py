import numpy as np


def grid(session):
    laps = session.laps
    drivers = laps.Driver.unique()
    positions = [session.get_driver(driver)["GridPosition"] for driver in drivers]
    sortedDriversindex = sorted(np.arange(len(drivers)), key=lambda x: positions[x])
    sortedDrivers = np.array(drivers)[sortedDriversindex]
    text = ""
    startingTyre = session.laps.query("LapNumber == 1").loc[:, ["Driver", "Compound"]].set_index("Driver")
    startingTyre["Driver Name"] = [session.get_driver(name)["FullName"] for name in startingTyre.index]
    for i in range(0, len(drivers)-2, 2):
        text += f" {sortedDrivers[i]}    |-{startingTyre.loc[sortedDrivers[i+1]]['Compound'][0]}-|\n|-{startingTyre.loc[sortedDrivers[i+2]]['Compound'][0]}-|    {sortedDrivers[i+1]}\n"
    print(f"|-{startingTyre.loc[sortedDrivers[0]]['Compound'][0]}-|        \n" + text + f" {sortedDrivers[-2]}    |-{startingTyre.loc[sortedDrivers[-1]]['Compound'][0]}-|\n         {sortedDrivers[-1]}")


if __name__ == "__main__":
    import logging
    import fastf1
    session = fastf1.get_session(2022, 'bahrain', 'R')
    session.load(telemetry=False, laps=True, weather=False)
    session.load_telemetry()
    logging.warn("Debug")
    grid(session)
