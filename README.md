# MicroPython-localtime
The built-in function `time.localtime` simply duplicates `gmtime` without the expected date & time localisation. This is due to the complexities of time zones and daylight saving time (DST) dates<sup>[1](https://github.com/orgs/micropython/discussions/12378), [2](https://forums.raspberrypi.com/viewtopic.php?t=337259&sid=dc6f7a405e66ee699aa182ff7b802eaf)</sup>.  
The two functions given here, `localtime.py` and `loc_time.py` replace the built-in to provide time localisation with DST correction for all the worldwide regions that have predictable dates for daylight saving changes.
## Details
Methods exist to determine the dates of DST changes for a couple of regions but concise expressions have been given by [Huang for North America and by van Gent for Europe](https://www.webexhibits.org/daylightsaving/i.html) (as proposed by [JumpZero](https://forum.micropython.org/viewtopic.php?f=2&t=4034)). Here, equivalent expressions have been derived for each of the geographical regions listed in the [DST Wiki](https://en.wikipedia.org/wiki/Daylight_saving_time_by_country) (as of January 2025) in order to form the worldwide micropython function.  
`localtime` returns the full 9-tuple as defined in Python 3 [localtime](https://docs.python.org/3/library/time.html) - that is, given a region code and the local time zone, it converts the time `secs` expressed in seconds since the Epoch into a 9-tuple in local time:  
(year, month, mday, hour, minute, second, weekday, yearday, isDST).  
If `secs` is not provided or is `None` then the current time from the RTC is used.  
The simpler, more efficient, version `loc_time` is preferred for general timekeeping applications.
Both functions can be readily simplified for a single location as shown in the example `loc_time_eur`.
## Usage
The RTC is always set to UTC then, after setting the appropriate region code and timezone, the current local date-time will be returned.  
`localtime` contains a test function that can be used to check that the function triggers the DST change on the correct date and time for any given year.  
The methods are valid up to the end of 2099.
