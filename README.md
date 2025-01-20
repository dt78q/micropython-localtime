# micropython-localtime
Replaces the, non-functional, built-in and aims to implement the full Python definition

The built-in function time.localtime() simply duplicates gmtime() without the implied date & time localisation. The function given here replaces the built-in and aims to implement the full Python definition. That is, given a region code and the local time zone, it gives the local time, including daylight saving changes (DST), for all the worldwide regions (i.e. those that have predictable DST dates). It is only really necessary for regions that use DST.
Methods exist to determine the dates of DST changes for a couple of regions but a concise expression was given by Huang and by van Gent for North America and for Europe (as proposed by JumpZero). Here, equivalent expressions have been worked out for each of the geographical regions listed in the Wikipedia entry on DST (as of January 2024) in order to form the universal micropython function.  Valid to the end of 2099.
There is also a simpler, more efficient, version, loc_time(), which should be sufficient for general clock applications. 
Each returns the time tuple matching the format of gmtime(). Both functions can be readily simplified for a single location, e.g. loc_time_eur.py.
#Usage
The RTC is always set to UTC then, after setting the region code and timezone, localtime() or loc_time() will return the current local time.
