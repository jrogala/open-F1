import numpy as np


def grid(session):
    laps = session.laps
    drivers = laps.Driver.unique()
    positions = [session.get_driver(driver)["GridPosition"] for driver in drivers]
    sortedDriversindex = sorted(np.arange(len(drivers)), key=lambda x: positions[x])
    sortedDrivers = np.array(drivers)[sortedDriversindex]
    text = ""
    for i in range(0, len(drivers)-2, 2):
        text += f" {sortedDrivers[i]}    |---|\n|---|    {sortedDrivers[i+1]}\n"
    print("|---|        \n" + text + f" {sortedDrivers[-2]}    |---|\n         {sortedDrivers[-1]}")
