import time
import datetime
from Core.leap_seconds import leap_seconds

# time_object = time.struct_time(tm_year=2020, tm_mon=01, tm_mday=01, tm_hour=1, tm_min=1, tm_sec=1, tm_wday=1,
#                              tm_yday=361, tm_isdst=0)


def unix_to_datestring(unixdate_s, type, utc_offset):


    if unixdate_s <= 0:
        result = time.localtime()

    #respect utc
    unixdate_s += utc_offset % 24 * 3600

    result = time.gmtime(unixdate_s)

    # print("result:", result)
    # print("\nyear:", result.tm_year)
    # print("tm_hour:", result.tm_hour)

    if type == 0:  # Standard
        time_string = time.ctime(unixdate_s)

    if type == 1:  # "2020-04-28T18:42:06"  // OpenWeathermap Date/Time Format
        time_string = time.strftime("%Y-%m-%dT%H:%M:%S", result)

    if type == 2:
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", result)




    return time_string


def datestring_to_unix(datestring, type, utc_offset, leaps: bool):
    # https://en.wikipedia.org/wiki/Date_format_by_country
    # UTC-Offsett: unit hours
    Seps = ["/", ".", "-", " ", ":", "T"]
    unixdate_s = 0

    if type == 1:
        # "2020-04-28T18:42:06"  // OpenWeathermap Date/Time Format
        unixdate_s = time.mktime(datetime.datetime.strptime(datestring, "%Y" + Seps[2] + "%m" + Seps[2] + "%d"
                                                            + Seps[5] + "%H" + Seps[4] + "%M" + Seps[4] +
                                                            "%S").timetuple())
    # dummy: other presets to implement
    if type >= 2:
        # "01/12/2011 "
        unixdate_s = -1

    #respect leap seconds?
    if leaps:
        for leap_idx in range(len(leap_seconds) - 1, -1, -1):
            # print(leap_idx, leap_seconds[leap_idx][0], leap_seconds[leap_idx][0] - leap_seconds[0][0], unixdate_s)
            l_abs = leap_seconds[leap_idx][0] - leap_seconds[0][0]  # remove 1972 offset
            # print(leap_idx, leap_seconds[leap_idx][0], l_abs, leap_seconds[leap_idx][1])

            if unixdate_s >= l_abs:
                leaps2add = leap_seconds[leap_idx][1]
                unixdate_s += leaps2add
                print('[TimersDates]: ', unixdate_s, " >= ", l_abs, " ", leap_idx, "Added leaps seconds: ", leaps2add,
                      leap_seconds[leap_idx][0])
                break

    # add utc offset [hrs]
    unixdate_s += utc_offset % 24 * 3600

    return unixdate_s


Date = "1995-08-28T18:42:06"

v1 = datestring_to_unix(Date, 1, 0, False)

print(Date, " -> ", unix_to_datestring(v1, 1, 0))
