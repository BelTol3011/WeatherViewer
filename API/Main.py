import requests
import xml.etree.ElementTree as ET

openweather_main_url = "https://api.openweathermap.org/data/2.5/weather?"
openweather_appID = "75a90db613d4fa920dd60f4bb3be02ef"


def build_request_string(bodystring: str, appid: str, cityname: str, country: str, XML: bool):
    # country: de, uk, us  ...

    # api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={your api key}
    # api.openweathermap.org/data/2.5/weather?id={city id}&appid={your api key}
    # api.openweathermap.org/data/2.5/find?q=London&units=metric&appid=75a90db613d4fa920dd60f4bb3be02ef
    # http://api.openweathermap.org/data/2.5/find?q=Frankfurt&units=metric&appid=75a90db613d4fa920dd60f4bb3be02ef&mode=xml
    # http://api.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&units=metric&appid=75a90db613d4fa920dd60f4bb3be02ef&mode=xml
    # https://openweathermap.org/current#data

    get_string = bodystring + "q=" + cityname + "," + country + "&appid=" + appid
    get_string = get_string + "&units=metric"  # hardcoded
    get_string = get_string + "&lang=de"  # hardcoded

    if XML:
        get_string = get_string + "&mode=xml"
    # debug
    # print(get_string)
    # back = requests.get(get_string)
    # print(back.text)
    return get_string


def decode_xmlstring(xmlstring):
    root = ET.fromstring(xmlstring)
    # print(root)
    # print(root.tag, " ", root.attrib)
    for child in root:
        print(child.tag, child.attrib)

    return root


requ_string = build_request_string(openweather_main_url, openweather_appID, "Berlin", "de", True)
# print(back)
xmlback = requests.get(requ_string)
print(xmlback.text)
root = decode_xmlstring(xmlback.text)
