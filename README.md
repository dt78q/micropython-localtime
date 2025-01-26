# micropython-localtime
Replacement for the, non-functional, built-in.

The built-in function time.localtime() simply duplicates gmtime() without the implied date & time localisation. The function given here replaces the built-in implementing the full Python definition. That is, given a region code and the time zone, it returns the local time, with daylight saving time (DST) correction, for all the worldwide regions (i.e. those that have predictable DST dates). It is only really necessary for regions that use DST.
## Details
Methods exist to determine the dates of DST changes for a couple of regions but a concise expression was given by [Huang and by van Gent](https://www.webexhibits.org/daylightsaving/i.html) for North America and for Europe (as proposed by [JumpZero](https://forum.micropython.org/viewtopic.php?f=2&t=4034)). Here, equivalent expressions have been worked out for each of the geographical regions listed in the [DST Wiki](https://en.wikipedia.org/wiki/Daylight_saving_time_by_country) (as of January 2024) in order to form the universal micropython function.
There is also a simpler, more efficient, version, loc_time(), which should be sufficient for general timekeeping. 
Each returns the time tuple matching the format of gmtime(). Both functions can be readily simplified for a single location as shown in the example loc_time_eur.py.

## Usage
The RTC is always set to UTC then, after setting the region code and timezone, localtime() or loc_time() will return the current local time.
localtime(\[secs\]) converts the time secs expressed in seconds since the Epoch into a date-time 9-tuple in local time which contains: (year, month, mday, hour, minute, second, weekday, yearday, dst) If secs is not provided or None, then the current time from the RTC is used. As [Python3](https://docs.python.org/3/library/time.html).
loc_time() returns the time tuple matching the format of gmtime()
The expressions are valid to the end of 2099.
