'''In a typical clock application, fwd & back need to be calculated on
startup (when the RTC is first set) and then just when the year changes.
RTC, fwd & back are always UTC.

Location codes:
(see: https://en.wikipedia.org/wiki/Daylight_saving_time_by_country)
Spring{month,f1,f2,time of shift/hr (in local time)},
Autumn{month,f1,f2,time of shift/hr (in local time)},
shift/min,SH=0/NH=1/Eur=2
(3,14,1,2, 11,7,1,2, 60,1)      # N. America group
(3,14,1,0, 11,7,1,1, 60,1)      # Cuba
(3,31,4,1, 10,31,1,2, 60,2)     # Europe group
(3,31,4,2, 10,31,1,3, 60,1)     # Moldova
(3,31,4,0, 10,31,1,0, 60,1)     # Lebanon
(3,29,4,2, 10,31,1,2, 60,1)     # Israel
(?,?,?,2, 10,30,1,2, 60,1)      # Palestine
(4,30,1,0, 10,31,4,24, 60,1)    # Egypt
(9,7,4,24, 4,7,5,24, 60,0)      # Chile
(10,7,5,0, 3,28,1,0, 60,0)      # Paraguay (from 2025 doesn't observe DST)
(10,7,5,2, 4,7,4,3, 60,0)       # S. Australia
(10,7,5,2, 4,7,4,2, 30,0)       # Aus.LHI
(9,30,5,2, 4,7,4,3, 60,0)       # New Zealand
'''
#### Settings ####
# your location code
ts = (3,31,4,1, 10,31,1,2, 60,2)     # Europe group
# time zone in hours, -12 <= timezone <= 14:
timezone = 0

from machine import RTC # type: ignore
from time import time, gmtime, mktime
rtc = RTC()

# find datetime for shifts
# run these six lines when the RTC is set or when a new year begins:
year = gmtime()[0]
tz = int(timezone * 3600)
dt = ts[8] * 60
qtz = int(timezone * 3600) if ts[9]!=2 else 0
fwd = mktime((year, ts[0], ts[1]-(5*year//4+ts[2])%7, int(ts[3]), 0,0,0,0,0)) -qtz
back = mktime((year, ts[4], ts[5]-(5*year//4+ts[6])%7, int(ts[7]), 0,0,0,0,0)) -qtz -dt

def loc_time(secs=None):
    if not secs:
        secs = time()
    if ts[9] != 0:
        dst = 1 if fwd<=secs<back else 0
    else:  # Southern hemisphere
        dst = 1 if not back<=secs<fwd else 0
    return gmtime(secs + dt*dst +tz) + (dst,)

print(loc_time())