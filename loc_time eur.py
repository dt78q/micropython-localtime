'''Simplified version of loc_time.py for Europe
just gives local time from the RTC in an 8-tuple
In a typical clock application, fwd & back need to be calculated on
startup (when the RTC is first set) and then just when the year changes.
RTC, fwd & back are always UTC.
'''

#### Settings ####
# time zone in hours, -12 <= timezone <= 14:
timezone = +1
#### end of settings ####

from machine import RTC # type: ignore
from time import time, gmtime, mktime, sleep
rtc = RTC()

# run these four lines when the RTC is set or when a new year begins:
year = gmtime()[0]
tz = int(timezone * 3600)
fwd = mktime((year, 3, 31-(5*year//4+4)%7, 1, 0,0,0,0,0)) 
back = mktime((year, 10, 31-(5*year//4+1)%7, 1, 0,0,0,0,0))
#   == mktime((year, 10, 31-(5*year//4+1)%7, 2, 0,0,0,0,0)) -3600
def loc_time():
    return gmtime(time() +(3600 if fwd<=time()<back else 0) +tz)

############ the following is just testing #################
# Set the date & time (e.g. to test when the switch occurs)
# compare to e.g. https://www.timeanddate.com/time/change/moldova
year, month, day = 2027, 10, 31
hr, min, sec = 1, 59, 55  # Sets local standard time - not local DST!
# recalculate fwd & back for current year
fwd = mktime((year, 3, 31-(5*year//4+4)%7, 1, 0,0,0,0,0))
back = mktime((year, 10, 31-(5*year//4+1)%7, 1, 0,0,0,0,0))
# print('forward =',gmtime(fwd))
# print('back =',gmtime(back))
# set RTC keeping the different tuples in order
utc = mktime((year, month, day, hr, min, sec, 0,0,0)) -tz
rtc.datetime((gmtime(utc)[0], gmtime(utc)[1], gmtime(utc)[2], 0,
               gmtime(utc)[3], gmtime(utc)[4], gmtime(utc)[5], 0))

months = ("", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December")
print(f"{months[3]} {31-(year*5//4+4)%7} at 01:00 +{timezone} hrs")
print(f"{months[10]} {31-(year*5//4+1)%7} at 02:00 +{timezone} hrs")

UTC = gmtime()
d_t = "UTC is {2} {1} {0}, {3:02n}:{4:02n}:{5:02n}"
print(d_t.format(UTC[0], months[UTC[1]], UTC[2], UTC[3], UTC[4], UTC[5]))

for _ in range(8):
    now = loc_time()
    d_t = "{2} {1} {0}, {3:02n}:{4:02n}:{5:02n}"
    if 2 != 0:
        msg = 'DST' if fwd<=time()<back else ''
    else:
        msg = 'DST' if not back<=time()<fwd else ''
    print(d_t.format(now[0], months[now[1]], now[2], now[3], now[4], now[5]), msg)
    sleep(1)