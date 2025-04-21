'''From the docs:
https://docs.micropython.org/en/latest/library/time.html#time.localtime
    time.localtime([secs])
    Convert the time [secs] expressed in seconds since the Epoch into an 8-tuple:
    (year, month, mday, hour, minute, second, weekday, yearday) 
    If secs is not provided or None, then the current time from the RTC is used.
    localtime() returns a date-time tuple in local time."

Although the docs specify:
"time.mktime() is inverse function of localtime - its argument is a full 8-tuple"
the function argument is "time_tuple: _TimeTuple | struct_time" which accepts
either an 8- or 9-tuple (the 9th argument is the unused 'isDST' flag).
Here the full 9-tuple is used (which prevents pylance from reporting a type error)
with the "isDST" flag ('0'or'1') appended to the tuple returned to be compatible with:
https://docs.python.org/3/library/time.html

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
ts = (9,30,5,2, 4,7,4,3, 60,0)       # New Zealand
# time zone in hours, -12 <= timezone <= 14:
timezone = 12

from machine import RTC # type: ignore
from time import time, gmtime, mktime, sleep
rtc = RTC()

tz = int(timezone * 3600)
dt = ts[8] * 60
qtz = int(timezone * 3600) if ts[9]!=2 else 0

def localtime(secs=None):
    if not secs:
        secs = time()
    year = gmtime(secs)[0]
    fwd = mktime((year, ts[0], ts[1]-(5*year//4+ts[2])%7, int(ts[3]), 0,0,0,0,0)) -qtz
    back = mktime((year, ts[4], ts[5]-(5*year//4+ts[6])%7, int(ts[7]), 0,0,0,0,0)) -qtz -dt
    if ts[9] != 0:
        dst = 1 if fwd<=secs<back else 0
    else:  # Southern hemisphere
        dst = 1 if not back<=secs<fwd else 0
    return gmtime(secs + dt*dst +tz) + (dst,)

############ the following is just testing #################
# compare to e.g. https://www.timeanddate.com/time/change/
# set the date & time (e.g. to test when the switch occurs)
year, month, day = 2025, 4, 6
hr, min, sec = 1, 59, 55  # Sets local standard time - not local DST!
# recalculate fwd & back for current year
fwd = mktime((year, ts[0], ts[1]-(5*year//4+ts[2])%7, int(ts[3]), 0,0,0,0,0)) -qtz
back = mktime((year, ts[4], ts[5]-(5*year//4+ts[6])%7, int(ts[7]), 0,0,0,0,0)) -qtz -dt
# print('forward =',gmtime(fwd))
# print('back =',gmtime(back))
# set RTC keeping the different tuples in order
utc = mktime((year, month, day, hr, min, sec, 0,0,0)) -tz
rtc.datetime((gmtime(utc)[0], gmtime(utc)[1], gmtime(utc)[2], 0,
               gmtime(utc)[3], gmtime(utc)[4], gmtime(utc)[5], 0))

months = ("", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December")
if ts[9] == 2:
    print(f"{months[ts[0]]} {ts[1]-(year*5//4+ts[2])%7} at 0{ts[3]}:00 +{timezone} hrs")
    print(f"{months[ts[4]]} {ts[5]-(year*5//4+ts[6])%7} at 0{ts[7]}:00 +{timezone} hrs")
else:
    print(f"{months[ts[0]]} {ts[1]-(year*5//4+ts[2])%7} at 0{ts[3]}:00")
    print(f"{months[ts[4]]} {ts[5]-(year*5//4+ts[6])%7} at 0{ts[7]}:00")
UTC = gmtime()
d_t = "UTC is {2} {1} {0}, {3:02n}:{4:02n}:{5:02n}"
print(d_t.format(UTC[0], months[UTC[1]], UTC[2], UTC[3], UTC[4], UTC[5]))
start_time = time()
print('start time =',localtime(time())[:5])
for _ in range(8):
    now = localtime()
    d_t = "{2} {1} {0}, {3:02n}:{4:02n}:{5:02n}"
    if ts[9] != 0:
        msg = 'DST' if fwd<=time()<back else ''
    else:
        msg = 'DST' if not back<=time()<fwd else ''
    print(d_t.format(now[0], months[now[1]], now[2], now[3], now[4], now[5]), msg)
    sleep(1)
print('end time =',localtime(time())[:5])

#### end of testing ####
