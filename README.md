# micropython-localtime
From the built-in module `time`, `localtime` simply duplicates `gmtime` without the expected date & time localisation. This is due to the complexities of time zones and daylight saving time (DST) dates, see [here](https://github.com/orgs/micropython/discussions/12378) and [here](https://forums.raspberrypi.com/viewtopic.php?t=337259&sid=dc6f7a405e66ee699aa182ff7b802eaf).

The two functions given here in localtime.py and loc_time.py replace the built-in to provide time localisation with DST correction for the worldwide regions that have predictable dates for daylight saving changes.
## Details
Methods exist to determine the dates of DST changes for a couple of regions but a concise expression was given by [Huang and by van Gent](https://www.webexhibits.org/daylightsaving/i.html) for North America and for Europe (as proposed by [JumpZero](https://forum.micropython.org/viewtopic.php?f=2&t=4034)). Here, equivalent expressions are provided for each of the geographical regions listed in the [DST Wiki](https://en.wikipedia.org/wiki/Daylight_saving_time_by_country) (as of January 2025) in order to form the universal micropython function.
`localtime` returns the full 9-tuple as defined in Python 3 [localtime](https://docs.python.org/3/library/time.html) - that is, given a region code and the local time zone, it converts the time [secs] expressed in seconds since the Epoch into a 9-tuple: (year, month, mday, hour, minute, second, weekday, yearday, isDST) in local time including DST changes. If secs is not provided or is None, then the current time from the RTC is used. It is only really useful for regions that use DST and is valid to the end of 2099.
The simpler, more efficient, version, `loc_time`, returns the 8-tuple matching the format of `gmtime` and should be sufficient for general timekeeping.
Both functions can be readily simplified for a single location as shown in the example loc_time_eur.py.
## Usage
The RTC is always set to UTC then, after editing the function to set the appropriate region code and timezone, `localtime` or `loc_time` will return the current local date-time. 

The reliability is dependent on regions adhering to the defined dates; there is no provision for unexpected date changes. The expressions are valid to the end of 2099.

localtime() contains a test function that can be used to check that the function triggers the DST change on the correct date and time for any given year.
