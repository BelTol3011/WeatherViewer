import time
import datetime
from Core.leap_seconds import leap_seconds

# Time Conversion with respect to leap seconds and local time zones

# Notes:
# time_object = time.struct_time(tm_year=2020, tm_mon=01, tm_mday=01, tm_hour=1, tm_min=1, tm_sec=1, tm_wday=1,
#                              tm_yday=361, tm_isdst=0)
# .tm_isdst: 1=Sommerzeit, 0=Winterzeit
# .tm_gmtoff: local system general mean time offset [sec]


def unix_to_datestring(unixdate_s, type, utc_offset_manual, respect_local_utc: bool):
    result_check = time.localtime()  # tmp to check local time zone settings

    unixdate_s += utc_offset_manual % 24 * 3600

    if unixdate_s <= 0:
        result = result_check  # no seconds given -> report local time
    else:
        if respect_local_utc:
            unixdate_s += result_check.tm_gmtoff
        result = time.gmtime(unixdate_s)

        # print(result)
        # print(result.tm_isdst, result.tm_gmtoff, result.tm_zone)
        # print(result_check.tm_isdst, result_check.tm_gmtoff, result_check.tm_zone)
        # print("result:", result) / # print("\nyear:", result.tm_year) /  # print("tm_hour:", result.tm_hour)

    if type == 0:  # Standard
        time_string = time.asctime(result)
        # zeitzone (lokal): print(time.strftime("%Z %z", result))

    if type == 1:  # "2020-04-28T18:42:06"  // OpenWeathermap Date/Time Format
        time_string = time.strftime("%Y-%m-%dT%H:%M:%S", result)

    if type == 2:  # "2020-04-28 18:42:06"
        time_string = time.strftime("%Y-%m-%d %H:%M:%S", result)

    if type == 3:
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", result)

    return time_string


def datestring_to_unix(datestring, type, utc_offset_manual, leaps: bool):
    # https://en.wikipedia.org/wiki/Date_format_by_country
    # UTC-Offset [hours]
    #Converts time to GMT (minus local time zone offsets)

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

    # respect leap seconds?
    if leaps:
        for leap_idx in range(len(leap_seconds) - 1, -1, -1):
            # print(leap_idx, leap_seconds[leap_idx][0], leap_seconds[leap_idx][0] - leap_seconds[0][0], unixdate_s)
            # print(leap_idx, leap_seconds[leap_idx][0], l_abs, leap_seconds[leap_idx][1])

            l_abs = leap_seconds[leap_idx][0] - leap_seconds[0][0]  # remove 1972 offset

            if unixdate_s >= l_abs:
                leaps2add = leap_seconds[leap_idx][1]
                unixdate_s += leaps2add
                #print('[TimersDates]: ', unixdate_s, " >= ", l_abs, " ", leap_idx, "Added leaps seconds: ", leaps2add,
                #      leap_seconds[leap_idx][0])
                break

    # add utc offset [hrs]
    unixdate_s += utc_offset_manual % 24 * 3600

    return unixdate_s



#usage:
#Date = "1995-08-28T18:42:06"
#Date2 = "2020-05-01T22:15:00"

#v1 = datestring_to_unix(Date, 1, 0, False)
#v2 = datestring_to_unix(Date2, 1, 0, False)
#print(Date, " -> ", unix_to_datestring(v1, 0, 0, True))
#print(Date, " -> ", unix_to_datestring(v1, 1, 0, True))
#print(Date, " -> ", unix_to_datestring(v1, 2, 0, True))
#print(Date, " -> ", unix_to_datestring(v1, 3, 0, True))

#print('----')
#print(Date2, " -> ", unix_to_datestring(v2, 0, 0, True))
#print(Date2, " -> ", unix_to_datestring(v2, 1, 0, True))
#print(Date2, " -> ", unix_to_datestring(v2, 2, 0, True))
#print(Date2, " -> ", unix_to_datestring(v2, 3, 0, True))

#print('----')
#print("no seconds given: ", unix_to_datestring(0, 0, 0, True))
