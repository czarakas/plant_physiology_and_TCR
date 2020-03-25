################################# SET UPWORKSPACE #########################################
import cftime
import numpy as np

################################################################## 

def reindex_time(startingtimes, yr_adjustment):
    """Reindexes time series to proleptic Gregorian calendar type"""
    newtimes = np.tile([cftime.DatetimeProlepticGregorian(1000, 1, 1)],
                       np.shape(startingtimes.values))
    for i in range(0, len(startingtimes)):
        yr = int(str(startingtimes.values[i])[0:4])
        mon = int(str(startingtimes.values[i])[5:7])
        newdate = cftime.DatetimeProlepticGregorian(yr+yr_adjustment, mon, 15)
        newtimes[i] = newdate
    return newtimes