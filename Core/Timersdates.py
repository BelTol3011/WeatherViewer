import time
import datetime
from Core.leap_seconds import leap_seconds


def datestring_to_unix(datestring, type, utc_offsett, leaps: bool):
    # https://en.wikipedia.org/wiki/Date_format_by_country
    # UTC-Offsett: unit hours
    Seps = ["/", ".", "-", " ", ":", "T"]
    unixdate_s = 0

    if type == 1:
        # "2020-04-28T18:42:06"  // OpenWeathermap Date/Time Format
        unixdate_s = time.mktime(datetime.datetime.strptime(datestring, "%Y" + Seps[2] + "%m" + Seps[2] + "%d"
                                                            + Seps[5] + "%H" + Seps[4] + "%M" + Seps[4] +
                                                            "%S").timetuple())
    #dummy: other presets to implement
    if type >= 2:
        # "01/12/2011 "
        unixdate_s = -1

    if leaps:
        for leap_idx in range(len(leap_seconds) - 1, -1, -1):
            l_abs = leap_seconds[leap_idx][0] - leap_seconds[0][0]  # remove 1972 offset

            if unixdate_s >= l_abs:
                print(unixdate_s, " >= ", l_abs, " ", leap_idx)
                unixdate_s += leap_seconds[leap_idx][1]
                print("Added leaps seconds: ", leap_seconds[leap_idx][1], " -> ", unixdate_s )
                break

    # add utc offsett [hrs]
    unixdate_s += utc_offsett * 3600

    return unixdate_s


# teststring_type1 = "2009-04-28T18:42:06"
# print(datestring_to_unix(teststring_type1, 1, 0, False))
teststring_type1 = "1977-08-28T18:42:06"
print(datestring_to_unix(teststring_type1, 1, 0, True))
# print(datestring_to_unix(teststring_type1, 1, -4, False))
