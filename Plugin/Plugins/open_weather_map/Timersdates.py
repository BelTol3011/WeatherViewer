import time
import datetime

def datestring_to_unix(datestring, type, utc_offsett):
    #https://en.wikipedia.org/wiki/Date_format_by_country
    #UTC-Offsett: unit hours
    Seps = ["/", ".", "-", " ", ":", "T"]

    if type == 1:
         # "2020-04-28T18:42:06"
         unixdate_s = time.mktime(datetime.datetime.strptime(datestring, "%Y"+Seps[2]+"%m"+Seps[2]+"%d"+Seps[5]+"%H"+Seps[4]+"%M"+Seps[4]+"%S").timetuple())
    if type == 2:
        #"01/12/2011 "
        unixdate_s = 0

    #add utc offsett [hrs]
    unixdate_s = unixdate_s + (utc_offsett * 3600)

    return unixdate_s



#teststring_type1 = "2020-04-28T18:42:06"
#print(datestring_to_unix(teststring_type1, 1, 0))
#print(datestring_to_unix(teststring_type1, 1, -4))


